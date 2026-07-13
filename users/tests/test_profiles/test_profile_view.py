from django.test import TestCase, RequestFactory
from django.urls import reverse
from http import HTTPStatus

from users.models import User
from users.views import ProfileUpdateView
from users.tests.helpers import make_user, make_saved_car

class ProfileViewTest(TestCase):
    def setUp(self) -> None:
        self.user = make_user(username="toyota_fan", bio="I love Camry")
        
    def test_returns_200_for_existing_username(self):
        url = reverse("users:profile", kwargs={"username": self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
    def test_uses_correct_template(self):
        url = reverse("users:profile", kwargs={"username": self.user.username})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "users/profile.html")
        
    def test_context_object_name_is_profile_user(self):
        url = reverse("users:profile", kwargs={"username": self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.context["profile_user"], self.user)
        
    def test_404_for_nonexistent_username(self):
        url = reverse("users:profile", kwargs={"username": "no-such-username"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND) # 404
        
    def test_saved_car_in_context(self):
        saved = make_saved_car(user=self.user)
        url = reverse("users:profile", kwargs={"username": self.user.username})
        response = self.client.get(url)
        self.assertIn(saved, response.context['saved_cars'])
        
class ProfileUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.user_a = make_user(username="user_a", bio="Original user A")
        self.user_b = make_user(username="user_b", bio="Original user B")
        self.url = reverse("users:profile_edit")
    
    # ── Auth requirement ─────────────────────────────────────────────────   
    def test_requires_login_redirects_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        
    # ── Happy path ───────────────────────────────────────────────────────
    def test_logged_in_user_can_update_own_bio(self):
        self.client.force_login(self.user_a)
        response = self.client.post(self.url, {"bio": "Updated bio A"})
        
        self.user_a.refresh_from_db()
        self.assertEqual(self.user_a.bio, "Updated bio A")
        self.assertRedirects(
            response,
            reverse("users:profile", kwargs={"username": self.user_a.username})
        )        
    
    # ── IDOR — integration level ────────────────────────────────────────
    def test_updating_as_user_a_never_touches_user_b(self):
        """
        There's no target-user id in the URL or form fields, so the only
        way this could go wrong is a future regression in get_object().
        This test locks in current (correct) behavior as a safety net.
        """
        self.client.force_login(self.user_a)
        self.client.post(self.url, {
            "bio": "Malicious payload",
            "id": str(self.user_b.pk),
            "pk": str(self.user_b.pk),
            "username": str(self.user_b.username)
        })
        
        self.user_b.refresh_from_db()
        self.assertEqual(self.user_b.bio, "Original user B")
        
    # ── IDOR — unit level, exercising get_object() directly ─────────────
    def test_get_object_always_returns_request_user_regardless_of_kwargs(self):
        """
        Directly calls get_object() with a fabricated kwargs dict containing
        another user's pk, simulating a future URL change that might pass
        an id. get_object() must ignore it completely.
        """
        factory = RequestFactory()
        request = factory.get(self.url)
        request.user = self.user_a
        
        view = ProfileUpdateView()
        view.request = request
        view.kwargs = {"pk": self.user_b.pk}

        result = view.get_object()
        
        self.assertEqual(result, self.user_a)
        self.assertNotEqual(result, self.user_b)
