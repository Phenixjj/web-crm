from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

# Get the user model
UserModel = get_user_model()


class EmailBackend(ModelBackend):
    """
    A custom authentication backend that allows users to log in using their email address or username.
    Inherits from Django's ModelBackend.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate the user based on email/username and password.

        Parameters:
        request (HttpRequest): An instance of Django's HttpRequest.
        username (str): The email or username provided by the user. Default is None.
        password (str): The password provided by the user. Default is None.

        Returns:
        user (UserModel instance): The authenticated user. Returns None if authentication fails.
        """
        try:
            # Try to get the user by email or username (case insensitive)
            user = UserModel.objects.get(
                Q(email__iexact=username) | Q(username__iexact=username)
            )
        except UserModel.DoesNotExist:
            # If user does not exist, set the password for a new user instance and return None
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned:
            # If multiple users are returned, get the first user based on the 'id' field
            user = (
                UserModel.objects.filter(
                    Q(email__iexact=username) | Q(username__iexact=username)
                )
                .order_by("id")
                .first()
            )
        # Check if the password is correct and the user is allowed to authenticate
        if user.check_password(password) and self.user_can_authenticate(user):
            # Return the authenticated user
            return user
