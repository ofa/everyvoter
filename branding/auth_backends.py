"""Authentication Backends for Branded Django"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# pylint: disable=invalid-name
UserModel = get_user_model()


class BrandedBackend(ModelBackend):
    """Username/Password auth for brandable sites"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        """Authenticate method on backend"""
        try:
            user = UserModel.objects.get(
                email=username, organization=request.organization,
                is_staff=True)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        else:
            if (user.check_password(password)
                    and self.user_can_authenticate(user)):
                return user
