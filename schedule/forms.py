from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMessage
from django.template import loader


UserModel = get_user_model()


class ResetPasswordForm(PasswordResetForm):
    """Form that handles a user password reset request"""
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):

        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        html_content = loader.render_to_string(html_email_template_name, context).replace(
            "api/v1/password/reset/confirm/", "user/password-reset/confirm/"  # slash is added auto in reset email
        )
        # html_content = loader.render_to_string(html_email_template_name, context)
        # print(html_content, 'HTML CONTENT')
        msg = EmailMessage(subject, html_content, from_email, [to_email])
        msg.content_subtype = 'html'
        msg.send()
