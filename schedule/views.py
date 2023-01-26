import json
from datetime import datetime

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from schedule.models import Setup
from schedule.serializer import SetupSerializer, ResetPasswordSerializer, CustomPasswordResetConfirmSerializer
from django_celery_beat.models import PeriodicTask, CrontabSchedule, ClockedSchedule

from dj_rest_auth.views import PasswordResetConfirmView
from django.utils.translation import ugettext_lazy as _
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


def validate_required_fields(fields: dict):
    """Method to check against required field in the views"""
    return {
        "detail": f"{field} cannot be empty"
        for field in fields
        if fields.get(field) is None
           or fields.get(field) == ""
           or fields.get(field) == []
           or fields.get(field) == {}
    }


def validate_date_time_filter(date_string: str):
    return datetime.strptime(date_string.strip(), '%Y-%m-%d %H:%M')


class SetupViewSet(viewsets.ModelViewSet):
    serializer_class = SetupSerializer
    permission_classes = (AllowAny,)
    queryset = Setup.objects.all()

    def create(self, request, *args, **kwargs):
        title = request.data.get('title')
        is_recurring = request.data.get('is_recurring')
        cron_task = request.data.get('cron_task')  # 'min,hr,day_week,day_month,month'
        task_date_time = request.data.get('task_date_time')  # YYYY-12-31 15:34
        try:
            if message := validate_required_fields(
                    {
                        "title": title,
                        "is_recurring": is_recurring,
                        # "cron_task": cron_task
                    }
            ):
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            split_cron = cron_task.split(',')
            if len(split_cron) != 5:
                return Response({'detail': "Invalid cron time"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            setup = serializer.save()
            if request.data.get('is_recurring') is True:
                if message := validate_required_fields(
                        {
                            "cron_task": cron_task
                        }
                ):
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
                cron_tab, _ = CrontabSchedule.objects.get_or_create(minute=split_cron[0], hour=split_cron[1],
                                                                    day_of_week=split_cron[2],
                                                                    day_of_month=split_cron[3],
                                                                    month_of_year=split_cron[4])
                periodic_task = PeriodicTask.objects.create(name=f'{setup.title} + {timezone.now()}',
                                                            task='computation_heavy_task_',
                                                            crontab=cron_tab,
                                                            args=json.dumps([setup.id]),
                                                            )
            else:
                if message := validate_required_fields(
                        {
                            "task_date_time": task_date_time
                        }
                ):
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
                try:
                    validate_task_time = validate_date_time_filter(task_date_time)
                except ValueError:
                    setup.delete()
                    return Response({'detail': "invalid dates passed"}, status=status.HTTP_400_BAD_REQUEST)

                clocked, _ = ClockedSchedule.objects.get_or_create(clocked_time=validate_task_time)
                periodic_task = PeriodicTask.objects.create(name=f'{setup.title} + {timezone.now()}',
                                                            task='computation_heavy_task_',
                                                            clocked=clocked,
                                                            args=json.dumps([setup.id]),
                                                            one_off=True)
            setup.task = periodic_task
            setup.save(update_fields=['task'])
            return Response("Done", status=status.HTTP_200_OK)
        except Exception as e:
            setup.delete()
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(generics.GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)
    throttle_scope = 'dj_rest_auth'

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Return the success message with OK HTTP status:
            return Response(
                {"detail": _("Password reset e-mail has been sent.")},
                status=status.HTTP_200_OK
            )
        # except ValidationError as e:
        #     error = get_all_serializer_errors(e)
        #     return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": _(str(e))}, status=status.HTTP_400_BAD_REQUEST)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    serializer_class = CustomPasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {'detail': _('Password has been reset with the new password.')},
                status=status.HTTP_200_OK)

        # except ValidationError as e:
        #     error = get_all_serializer_errors(e)
        #     return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": _(str(e))}, status=status.HTTP_400_BAD_REQUEST)
