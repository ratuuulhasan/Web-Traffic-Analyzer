from django.utils import timezone
from rest_framework import authentication, exceptions
from websites.models import APIKey


class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication using API Key.
    Header format: Authorization: Api-Key <your_key>
    """

    keyword = 'Api-Key'

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None  # No auth, let permission handle it

        parts = auth_header.split()

        if len(parts) != 2:
            raise exceptions.AuthenticationFailed(
                "Invalid Authorization header format. Use: Api-Key <your_key>"
            )

        if parts[0] != self.keyword:
            raise exceptions.AuthenticationFailed(
                f"Authorization header must start with '{self.keyword}'"
            )

        key_value = parts[1]

        try:
            api_key = APIKey.objects.select_related('website', 'website__owner').get(
                key=key_value,
                is_active=True,
            )
        except APIKey.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid or inactive API key")

        # Update last_used
        api_key.last_used = timezone.now()
        api_key.save(update_fields=['last_used'])

        # Return (user, auth) — DRF wants this tuple
        return (api_key.website.owner, api_key)

    def authenticate_header(self, request):
        return self.keyword