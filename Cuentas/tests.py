from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from Cuentas.views import MyFichasViews


class MyFichasViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test", role="A"
        )
        # Provide more initialization if needed, like creating student profile and attaching fichas

    def test_get_queryset(self):
        request = self.factory.get("/")
        request.user = self.user
        view = MyFichasViews()
        view.request = request

        queryset = view.get_queryset()
        # Check if queryset returns the correct fichas of the user
        print(queryset)
