# Generated by Django 2.2.6 on 2020-06-17 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Connect', '0017_follow_company_user_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_model',
            name='facebook_ac',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='company_model',
            name='twitter_ac',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
