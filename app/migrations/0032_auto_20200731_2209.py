# Generated by Django 2.2.10 on 2020-07-31 16:39

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_prescription_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('datetime', models.DateTimeField(auto_created=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('terms', tinymce.models.HTMLField()),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
