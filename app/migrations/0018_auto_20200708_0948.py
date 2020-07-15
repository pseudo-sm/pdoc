# Generated by Django 2.2.10 on 2020-07-08 04:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20200628_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointments',
            name='slug',
            field=models.SlugField(auto_created=True, default='abcd-efgh-ijkl-mnop'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointments',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
