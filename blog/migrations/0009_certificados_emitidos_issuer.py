# Generated by Django 3.0.4 on 2020-03-13 19:37

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_certificados_emitidos_serial'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificados_emitidos',
            name='issuer',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=2), default=list, size=6),
        ),
    ]
