# Generated by Django 4.2.6 on 2023-11-17 10:35

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.query


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pipeline', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='anticipated_closure_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 24, 10, 35, 58, 744064, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='record',
            name='created_by',
            field=models.ForeignKey(default=django.db.models.query.QuerySet.first, on_delete=django.db.models.deletion.CASCADE, related_name='created_records', to=settings.AUTH_USER_MODEL),
        ),
    ]
