# Generated by Django 2.2.10 on 2020-07-27 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_prescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='period',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='quantity',
            field=models.CharField(max_length=300),
        ),
    ]
