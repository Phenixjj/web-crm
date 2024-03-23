from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


# This class is a custom token generator for account activation.
# It inherits from Django's PasswordResetTokenGenerator.
class TokenGenerator(PasswordResetTokenGenerator):
    # This method is used to create a hash value for the token.
    # It takes a user object and a timestamp as arguments.
    # The hash value is created by concatenating the user's primary key,
    # the timestamp, and the user's active status.
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)


# This is an instance of the TokenGenerator class.
# It is used to generate account activation tokens.
account_activation_token = TokenGenerator()
