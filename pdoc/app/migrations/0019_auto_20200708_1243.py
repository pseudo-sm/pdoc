# Generated by Django 2.2.10 on 2020-07-08 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20200708_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
