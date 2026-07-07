"""
Test helpers for the users app.

Kept separate from cars/tests/helpers/helper_models.py — users tests may
import cars helpers (SavedCar.car references CarVariant), but the reverse
must never happen. Mixing them into one shared helper module would tangle
that dependency direction.
"""
import itertools

from users.models import  User, Province, SavedCar

_username_seq = itertools.count(1)

def make_user(**kwargs)-> User:
    """
    Create a test user with, unique username/email per call.
    Uses create_user() so the password is properly hashed.
    """
    n = next(_username_seq)
    defaults = dict(
        username=f"user{n}",
        email=f"user{n}@example.com",
        password="testpass123",
    )
    defaults.update(kwargs)
    return User.objects.create_user(**defaults)

def make_province(**kwargs)-> Province:
    defaults = dict(name="Hồ Chí Minh", code="SG")
    defaults.update(kwargs)
    return Province.objects.get_or_create(
        name=defaults['name'],
        defaults=defaults,
    )[0]
    
def make_saved_car(user=None, car=None, **kwargs) -> SavedCar:
    """car defaults to a fresh CarVariant via the cars helper — this is
    the one-way import mentioned above."""
    if user is None:
        user = make_user()
    if car is None:
        from cars.tests.helpers.helper_models import make_variant
        car = make_variant()
    defaults = dict(user=user, car=car)
    defaults.update(kwargs)
    return SavedCar.objects.create(**defaults)