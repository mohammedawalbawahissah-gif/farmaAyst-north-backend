from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('farms', '0005_alter_farm_flock_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='farm',
            name='monitoring_officer',
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={'role': 'monitoring_officer'},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='assigned_farms',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
