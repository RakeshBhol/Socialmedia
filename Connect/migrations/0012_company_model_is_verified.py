# Generated by Django 2.2.6 on 2020-06-15 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Connect', '0011_company_model_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_model',
            name='is_verified',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
