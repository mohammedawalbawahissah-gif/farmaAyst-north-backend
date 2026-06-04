from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        # Extend role field max_length and add monitoring_officer choice
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                max_length=30,
                choices=[
                    ('farmer',             'Farmer'),
                    ('investor',           'Investor'),
                    ('consumer',           'Consumer'),
                    ('admin',              'Admin'),
                    ('monitoring_officer', 'Monitoring Officer'),
                ],
                default='farmer',
            ),
        ),
        # New MonitoringOfficerProfile model
        migrations.CreateModel(
            name='MonitoringOfficerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(blank=True, max_length=50)),
                ('assigned_region', models.CharField(blank=True, max_length=100)),
                ('assigned_districts', models.JSONField(default=list)),
                ('ghana_card_number', models.CharField(blank=True, max_length=50)),
                ('date_of_hire', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='monitoring_profile',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={'db_table': 'monitoring_officer_profiles'},
        ),
    ]
