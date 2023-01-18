from rest_framework import serializers

from schedule.models import Setup


class SetupSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('task', )
        model = Setup
