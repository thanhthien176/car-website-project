"""
local_tools/upload_and_key_images.py
Run LOCALLY (do not run on the production server).
Requirement: poetry install --with scraping

Processing flow for each CSV row:
1. Query the DB to confirm that CarModel/CarVariant exists (get the REAL slug from the DB, do not guess with slugify to avoid mismatches with the server).
2. Download images via HTTP (use requests first, fallback to DrissionPage SessionPage if blocked — both are lightweight, do not open a real browser).
3. Convert to WebP (reuse existing logic in cars.utils.image_utils).
4. Compute SHA-256 of the image content -> build a deterministic r2_key to avoid duplicates on reruns.
5. Check if the key already exists on R2 (head_object) -> skip if it does.
6. Upload if it doesn't exist.
7. Immediately write one line to the output CSV (flush right away) so the process can resume if the script is stopped midway.

Usage:
python local_tools/upload_and_key_images.py input.csv output.csv
python local_tools/upload_and_key_images.py input.csv output.csv --resume

"""
import argparse
import csv
import hashlib
import logging
import os
import sys
import time
import requests
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from decouple import config


# ---------------------------------------------------------------------------
# Bootstrap Django (to use ORM to query CarModel/CarVariant + standard slugify)
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

import django  # noqa: E402
django.setup()

from django.utils.text import slugify  # noqa: E402
from cars.models import CarModel, CarVariant  # noqa: E402
from cars.utils.image_utils import download_image, image_byte_to_webp  # noqa: E402

from local_tools.base_scraper import Scraper


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

"""
R2 client — use SEPARATE credentials for local, scope only PutObject/HeadObject. 
Do not share the key with the production server.
"""

s3 = boto3.client(
    "s3",
    endpoint_url=config("R2_ENDPOINT_URL_CRAWLER"),
    aws_access_key_id=config("R2_LOCAL_ACCESS_KEY_ID_CRAWLER"),
    aws_secret_access_key=config("R2_LOCAL_SECRET_ACCESS_KEY_CRAWLER"),
    region_name="auto",
)
BUCKET = config("R2_BUCKET_NAME")

MAX_SIZE_GALLERY = (1920, 1920)
OUTPUT_FIELDS = [
    "brand_name", "model_name", "model_year", "variant_name",
    "image_url", "caption", "is_primary", "order",
    "author_name", "author_url", "source_name", "source_url", "license",
    "r2_key", "status",
]


# ---------------------------------------------------------------------------
# Step 1: Confirm that the record exists in the DB + get the REAL slug
# ---------------------------------------------------------------------------
def resolve_slug(row: dict) -> tuple[str | None, str]:
    # Return (slug, folder) or (None, reason_for_error).
    brand_name = row.get("brand_name", "").strip()
    model_name = row.get("model_name", "").strip()
    variant_name = row.get("variant_name", "").strip()

    model_slug_guess = slugify(f"{brand_name}-{model_name}-2026")
    car_model = CarModel.objects.filter(slug=model_slug_guess).first()
    if car_model is None:
        return None, f"CarModel not found for slug guess '{model_slug_guess}'"

    if variant_name:
        variant_slug_guess = slugify(f"{brand_name}-{model_name}-{variant_name}-2026")
        
        variant = CarVariant.objects.filter(
            car_model=car_model, name=variant_name
        ).first()
        if variant is None:
            return None, f"CarVariant '{variant_name}' not found under {car_model}"
        return variant.slug, "variants/gallery"

    return car_model.slug, "cars/gallery"


# ---------------------------------------------------------------------------
# Step 2: Download image — requests first, DrissionPage SessionPage as backup
# ---------------------------------------------------------------------------
def fetch_image_bytes(url: str, scraper: Scraper) -> bytes | None:
    
    # Use requests to fetch image, if requests is block, the tools will use DrissionPage
    resp = requests.get( url, headers={"User-Agent": "Mozilla/5.0"},)
    if resp:
        return resp.content
        
    
    try:
        scraper.load_cookies(url)
        img_el = scraper.get_one('tag:img')

        if not img_el:
            logger.warning("No <img> found on %s", url)
            return None
        
        img_bytes = img_el.src()
        if img_bytes is None:
            logger.warning("img.src() returned no resource for %s", url)
            return None
        
        if isinstance(img_bytes, str):
            logger.warning("Expected bytes but got str for %s (src may be text/svg+xml or malformed)", url)
            return None
        
        return img_bytes
    
    except Exception as exc:
        logger.warning("SessionPage failed: %s", exc)

    return None


# ---------------------------------------------------------------------------
# Step 4: Key determined according to content — safe when resuming/re-running
# ---------------------------------------------------------------------------
def build_r2_key(folder: str, slug: str, webp_bytes: bytes) -> str:
    content_hash = hashlib.sha256(webp_bytes).hexdigest()[:8]
    slug = (slug or "")[:60]
    return f"{folder}/{slug}-{content_hash}.webp"


# ---------------------------------------------------------------------------
# Step 5+6: Check for existence before uploading — avoid overwriting/extra uploads
# ---------------------------------------------------------------------------
def upload_if_missing(key: str, webp_bytes: bytes) -> str:
    try:
        s3.head_object(Bucket=BUCKET, Key=key)
        return "already_exists"
    except ClientError as exc:
        if exc.response["Error"]["Code"] != "404":
            raise  # other errors 404 (e.g., permission) -> let it crash, do not swallow the error

    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=webp_bytes,
        ContentType="image/webp",
    )
    return "uploaded"


def load_resume_keys(output_csv: Path) -> set[str]:
    """Read the old CSV output (if any) to know which lines have already been processed."""
    done = set()
    if not output_csv.exists():
        return done
    with open(output_csv, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row.get("r2_key") and row.get("status") in ("uploaded", "already_exists"):
                done.add(row.get("image_url", ""))
    return done


def main(input_csv: Path, output_csv: Path, resume: bool):
    already_done = load_resume_keys(output_csv) if resume else set()
    write_mode = "a" if resume and output_csv.exists() else "w"
    

    with open(input_csv, encoding="utf-8-sig") as fin:
        rows = list(csv.DictReader(fin))

    with open(output_csv, write_mode, newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=OUTPUT_FIELDS)
        if write_mode == "w":
            writer.writeheader()

        total, ok, skipped, failed = len(rows), 0, 0, 0

        with Scraper() as scraper:
        
            for i, row in enumerate(rows, start=1):
                url = row.get("image_url", "").strip()
                if not url:
                    continue
                if url in already_done:
                    logger.info("[%d/%d] SKIP (đã resume) %s", i, total, url)
                    skipped += 1
                    continue

                out_row = {**{k: row.get(k, "") for k in OUTPUT_FIELDS}, "r2_key": "", "status": ""}

                slug, info = resolve_slug(row)
                if slug is None:
                    logger.warning("[%d/%d] SKIP - %s", i, total, info)
                    out_row["status"] = f"error: {info}"
                    writer.writerow(out_row)
                    fout.flush()
                    failed += 1
                    continue
                

                image_bytes = fetch_image_bytes(url, scraper)
                if image_bytes is None:
                    logger.warning("[%d/%d] SKIP - Can't download %s", i, total, url)
                    out_row["status"] = "error: download_failed"
                    writer.writerow(out_row)
                    fout.flush()
                    failed += 1
                    continue

                webp = image_byte_to_webp(image_bytes, max_size=MAX_SIZE_GALLERY)
                if webp is None:
                    logger.warning("[%d/%d] SKIP - convert error webp %s", i, total, url)
                    out_row["status"] = "error: convert_failed"
                    writer.writerow(out_row)
                    fout.flush()
                    failed += 1
                    continue

                webp_bytes = webp.read()
                key = build_r2_key(info, slug, webp_bytes)

                try:
                    status = upload_if_missing(key, webp_bytes)
                except Exception as exc:
                    logger.error("[%d/%d] upload ERROR %s: %s", i, total, url, exc)
                    out_row["status"] = f"error: upload_failed ({exc})"
                    writer.writerow(out_row)
                    fout.flush()
                    failed += 1
                    continue

                logger.info("[%d/%d] %s -> %s (%s)", i, total, slug, key, status)
                out_row["r2_key"] = key
                out_row["status"] = status
                writer.writerow(out_row)
                fout.flush()
                ok += 1

                time.sleep(0.2)  # be gentle with the source server, avoid being rate-limited/IP blocked

    logger.info(
        "Finished. Total: %d | OK: %d | Skip (resume): %d | Errors: %d",
        total, ok, skipped, failed,
    )
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--resume", action="store_true", help="Skip the line processed in old output_csv")
    args = parser.parse_args()
    main(args.input_csv, args.output_csv, args.resume)