from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from users.models import SavedCar
from users.tests.helpers import make_user
from cars.tests.helpers import make_variant


class ToggleSavedCarViewTest(TestCase):
    def setUp(self) -> None:
        self.user = make_user(username="toggler")
        self.variant = make_variant()
        self.url = reverse("users:toggle_saved_car", kwargs={"variant_pk": self.variant.pk})
        
    # ── Auth requirement ─────────────────────────────────────────────────
    def test_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        
    # ── First toggle: save ───────────────────────────────────────────────
    def test_first_toggle_creates_saved_car(self):
        self.client.force_login(self.user)
        self.client.post(self.url)
        
        self.assertTrue(
            SavedCar.objects.filter(user=self.user, car=self.variant).exists()
        )
        
     # ── Second toggle: unsave ────────────────────────────────────────────
    def test_second_toggle_removes_saved_car(self):
        self.client.force_login(self.user)
        self.client.post(self.url)          # save
        
        self.assertTrue(
            SavedCar.objects.filter(user=self.user, car=self.variant).exists()
        )
        self.client.post(self.url)          # unsave
        
        self.assertFalse(
            SavedCar.objects.filter(user=self.user, car=self.variant).exists()
        )
        
    # ── Idempotent count check across 3 toggles ─────────────────────────
    def test_three_toggles_ends_in_saved_state(self):
        self.client.force_login(self.user)
        self.client.post(self.url)
        self.client.post(self.url)
        self.client.post(self.url)
        
        self.assertEqual(
            SavedCar.objects.filter(user=self.user, car=self.variant).count(), 1
        )
        
     # ── Response is HTML fragment, not JSON/redirect ─────────────────────
    def test_response_is_html_fragment(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response["Content-Type"], "text/html; charset=utf-8")
        
    # ── Only affects the requesting user, not other users' saved state ──
    def test_does_not_affect_other_users_saved_cars(self):
        other_user = make_user(username="other")
        SavedCar.objects.create(user=other_user, car=self.variant)
        
        self.client.force_login(self.user)
        self.client.post(self.url)
        
        self.assertTrue(
            SavedCar.objects.filter(user=other_user, car=self.variant).exists()
        )
        self.assertTrue(
            SavedCar.objects.filter(user=self.user, car=self.variant).exists()
        )
        
    # ── Inactive variant returns 404 ─────────────────────────────────────
    def test_inactive_variant_returns_404(self):
        inactive_variant = make_variant(
            car_model=self.variant.car_model,
            name="inactive variant",
            is_active=False,
        )
        url = reverse(
            "users:toggle_saved_car", kwargs={"variant_pk": inactive_variant.pk}
        )
        self.client.force_login(self.user)
        response = self.client.post(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        
    # ── Nonexistent variant returns 404 ──────────────────────────────────
    def test_nonexistent_variant_returns_404(self):
        url = reverse("users:toggle_saved_car", kwargs={"variant_pk": 9999999})
        
        self.client.force_login(self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        
