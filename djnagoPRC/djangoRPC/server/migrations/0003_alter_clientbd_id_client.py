# Generated by Django 4.1.6 on 2023-03-07 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_clientbd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientbd',
            name='id_client',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='server.dataserver'),
        ),
    ]
