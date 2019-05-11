# Generated by Django 2.2 on 2019-04-30 10:56

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Emergency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_min', models.IntegerField()),
                ('age_max', models.IntegerField()),
                ('genders', django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(), size=2)),
            ],
        ),
    ]