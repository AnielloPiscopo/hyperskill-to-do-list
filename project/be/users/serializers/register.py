from rest_framework import serializers
from django.contrib.auth.models import User

__all__ = ['RegisterSerializer']

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user account.

    `confirm_password` is a write-only field used only for client-side
    confirmation; it is stripped from validated data before the user is created.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text='Password for the new account'
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text='Repeat the password to confirm'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate_email(self, email: str) -> str: # noqa
        """Normalize the email and reject one already in use by another account."""
        normalized_email: str = email.lower()
        if User.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError('This email is already in use.')
        return normalized_email

    def validate(self, data):
        """Ensure the two password fields are identical."""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords must match')
        return data

    def create(self, validated_data):
        """Create the user, discarding the confirmation field before saving."""
        # confirm_password must not be passed to create_user as it is not a model field
        validated_data.pop('confirm_password')
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )