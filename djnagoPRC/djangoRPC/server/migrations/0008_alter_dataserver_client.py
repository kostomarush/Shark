# Generated by Django 4.1.6 on 2023-03-11 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_alter_dataserver_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataserver',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='server.clientbd'),
        ),
    ]
