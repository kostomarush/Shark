# Generated by Django 4.2.5 on 2023-10-11 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_alter_segmentresult_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipaddress',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='server.clientbd'),
        ),
    ]