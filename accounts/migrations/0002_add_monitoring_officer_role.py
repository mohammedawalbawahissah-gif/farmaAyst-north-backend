from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('farmer',             'Farmer'),
                    ('investor',           'Investor'),
                    ('consumer',           'Consumer'),
                    ('monitoring_officer', 'Monitoring Officer'),
                    ('admin',              'Admin'),
                ],
                default='farmer',
            ),
        ),
    ]
