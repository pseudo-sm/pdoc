# Generated by Django 2.2.10 on 2020-06-28 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20200628_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='available_from',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='available_to',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='education',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='paramedics',
            name='available_from',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='paramedics',
            name='available_to',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
