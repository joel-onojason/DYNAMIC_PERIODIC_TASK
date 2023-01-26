from rest_framework import serializers

from schedule.forms import ResetPasswordForm
from schedule.models import Setup

from dj_rest_auth.serializers import PasswordResetSerializer
from django.conf import settings

from dj_rest_auth.serializers import PasswordResetConfirmSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode as uid_decoder
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

UserModel = get_user_model()


class SetupSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('task',)
        model = Setup


class ResetPasswordSerializer(PasswordResetSerializer):
    """Handles password reset, needed to be overwritten since the base class has been inherited for other purposes,
    so that the password reset functionality would work"""
    password_reset_form = ResetPasswordForm

    @property
    def password_reset_form_class(self):
        return ResetPasswordForm

    def get_email_options(self):
        return {
            'html_email_template_name': 'registration/password_reset_email.html',
        }

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'token_generator': default_token_generator,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    def validate(self, attrs):
        try:
            uid = force_str(uid_decoder(attrs['uid']))
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs,
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs
