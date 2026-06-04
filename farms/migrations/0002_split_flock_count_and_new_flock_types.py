from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farms', '0001_initial'),
    ]

    operations = [
        # ── New flock types on Farm ───────────────────────────────────────────
        migrations.AlterField(
            model_name='farm',
            name='flock_type',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('broilers',       'Broilers'),
                    ('layers',         'Layers'),
                    ('day_old_chicks', 'Day-Old Chicks'),
                    ('hatchery',       'Hatchery'),
                    ('mixed',          'Mixed'),
                ],
            ),
        ),

        # ── Split flock_count into three columns on FarmActivityLog ──────────
        migrations.AddField(
            model_name='farmactivitylog',
            name='broiler_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='farmactivitylog',
            name='layer_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='farmactivitylog',
            name='day_old_chick_count',
            field=models.PositiveIntegerField(default=0),
        ),
        # Migrate existing flock_count value into broiler_count, then drop
        migrations.RunSQL(
            sql="UPDATE farm_activity_logs SET broiler_count = flock_count WHERE flock_count IS NOT NULL;",
            reverse_sql="UPDATE farm_activity_logs SET flock_count = broiler_count;",
        ),
        migrations.RemoveField(
            model_name='farmactivitylog',
            name='flock_count',
        ),
    ]
