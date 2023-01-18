from django.db import models
from django_enum_choices.fields import EnumChoiceField
from django_celery_beat.models import PeriodicTask
from .enums import SetupStatus


class Setup(models.Model):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setups'

    title = models.CharField(max_length=70, blank=False)
    status = EnumChoiceField(SetupStatus, default=SetupStatus.active)
    created_at = models.DateTimeField(auto_now_add=True)
    is_recurring = models.BooleanField(default=False)  # whether the setup task is recurring
    task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title
