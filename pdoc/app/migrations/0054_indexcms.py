# Generated by Django 2.2.10 on 2020-09-23 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0053_auto_20200831_2003'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexCms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('value', models.TextField()),
            ],
        ),
    ]
