from rest_framework import serializers

__all__ = ['ChangePasswordSerializer']

class ChangePasswordSerializer(serializers.Serializer):
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
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError('Passwords must match.')
        return data
