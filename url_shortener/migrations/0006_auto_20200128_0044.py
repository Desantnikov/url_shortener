# Generated by Django 3.0.2 on 2020-01-27 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_shortener', '0005_url_last_redirect_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='last_redirect_datetime',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
