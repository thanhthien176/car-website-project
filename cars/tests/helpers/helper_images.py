from unittest.mock import MagicMock

def mock_image(name: str, size_bytes: int):
    """Tạo mock file object với .name và .size."""
    f = MagicMock()
    f.name = name
    f.size = size_bytes
    return f