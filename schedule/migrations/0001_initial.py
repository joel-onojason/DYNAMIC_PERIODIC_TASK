# Generated by Django 3.2.12 on 2023-01-17 10:33

from django.db import migrations, models
import django.db.models.deletion
import django_enum_choices.choice_builders
import django_enum_choices.fields
import schedule.enums


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_beat', '0015_edit_solarschedule_events_choices'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('status', django_enum_choices.fields.EnumChoiceField(choice_builder=django_enum_choices.choice_builders.value_value, choices=[('Active', 'Active'), ('Disabled', 'Disabled')], default=schedule.enums.SetupStatus['active'], enum_class=schedule.enums.SetupStatus, max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('time_interval', django_enum_choices.fields.EnumChoiceField(choice_builder=django_enum_choices.choice_builders.value_value, choices=[('1 min', '1 min'), ('5 mins', '5 mins'), ('1 hour', '1 hour')], default=schedule.enums.TimeInterval['five_mins'], enum_class=schedule.enums.TimeInterval, max_length=6)),
                ('task', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.periodictask')),
            ],
            options={
                'verbose_name': 'Setup',
                'verbose_name_plural': 'Setups',
            },
        ),
    ]