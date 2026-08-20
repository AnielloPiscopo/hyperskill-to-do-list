from rest_framework import serializers
from users.constants.api import validation_msg as user_msg

__all__ = ['ChangePasswordSerializer']

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for the change-password flow.

    Does not extend ModelSerializer because it operates on request data only
    and never directly reads from or writes to a model instance.
    """

    old_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text='Current password'
    )
    new_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text='New password'
    )
    confirm_new_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text='Repeat the new password to confirm'
    )

    def validate(self, data):
        """Ensure the two new-password fields are identical."""
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError(user_msg.PASSWORDS_MUST_MATCH)
        return data
