# Generated by Django 4.2.5 on 2024-01-12 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientBD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_client', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='DataServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(default=False, max_length=10)),
                ('ip', models.CharField(max_length=20)),
                ('port', models.CharField(max_length=20)),
                ('mode', models.CharField(choices=[('', 'Выберите режим'), ('TCP', 'TCP'), ('UDP', 'UDP'), ('OS', 'OS')], default='', max_length=10)),
                ('cve_report', models.BooleanField(default=False)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='server.clientbd')),
            ],
        ),
        migrations.CreateModel(
            name='IPAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.GenericIPAddressField()),
                ('tag', models.CharField(default=False, max_length=20)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='server.clientbd')),
            ],
        ),
        migrations.CreateModel(
            name='SegmentScan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(choices=[('', 'Выберите режим'), ('TCP', 'TCP'), ('UDP', 'UDP'), ('OS', 'OS')], default='', max_length=10)),
                ('ip', models.CharField(max_length=20)),
                ('mask', models.CharField(max_length=20)),
                ('state_scan', models.CharField(default=False, max_length=20)),
                ('cve_report', models.BooleanField(default=False)),
                ('full_scan', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SegmentResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=20)),
                ('state_scan', models.CharField(max_length=20)),
                ('state_ports', models.CharField(max_length=10)),
                ('full_name', models.CharField(max_length=30)),
                ('vendor', models.CharField(max_length=20)),
                ('osfamily', models.CharField(max_length=20)),
                ('osgen', models.CharField(max_length=20)),
                ('accuracy', models.CharField(max_length=20)),
                ('is_execution_complete', models.BooleanField(default=False)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.ipaddress')),
            ],
        ),
        migrations.CreateModel(
            name='ScanInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=20)),
                ('state_scan', models.CharField(max_length=20)),
                ('state_ports', models.CharField(max_length=10)),
                ('full_name', models.CharField(max_length=30)),
                ('vendor', models.CharField(max_length=20)),
                ('osfamily', models.CharField(max_length=20)),
                ('osgen', models.CharField(max_length=20)),
                ('accuracy', models.CharField(max_length=20)),
                ('is_execution_complete', models.BooleanField(default=False)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.dataserver')),
            ],
        ),
        migrations.CreateModel(
            name='ResultPortsAim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=20)),
                ('reason', models.CharField(max_length=20)),
                ('service', models.CharField(max_length=20)),
                ('one_cve', models.TextField()),
                ('all_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.scaninfo')),
            ],
        ),
        migrations.CreateModel(
            name='ResultPorts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=20)),
                ('reason', models.CharField(max_length=20)),
                ('service', models.CharField(max_length=20)),
                ('one_cve', models.TextField()),
                ('all_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.segmentresult')),
            ],
        ),
        migrations.CreateModel(
            name='LevelCveAim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.CharField(max_length=10)),
                ('cve', models.CharField(max_length=20)),
                ('level', models.CharField(max_length=30)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.scaninfo')),
            ],
        ),
        migrations.CreateModel(
            name='LevelCve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_execution_complete', models.BooleanField(default=False)),
                ('port', models.CharField(max_length=10)),
                ('cve', models.CharField(max_length=20)),
                ('level', models.CharField(max_length=30)),
                ('year', models.CharField(max_length=10)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.segmentresult')),
            ],
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='seg_scan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.segmentscan'),
        ),
        migrations.CreateModel(
            name='CveInformationAim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cve_information', models.TextField()),
                ('result_ports', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.resultportsaim')),
            ],
        ),
        migrations.CreateModel(
            name='CveInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cve_information', models.TextField()),
                ('result_ports', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.resultports')),
            ],
        ),
    ]
