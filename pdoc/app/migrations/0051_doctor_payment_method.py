# Generated by Django 2.2.10 on 2020-08-19 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_auto_20200814_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='payment_method',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
