# Generated by Django 3.0.4 on 2020-03-14 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_delete_certificados_emitidos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificados_emitidos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificado', models.BinaryField()),
                ('serial', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
