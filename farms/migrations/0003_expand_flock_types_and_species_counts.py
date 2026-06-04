from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farms', '0002_split_flock_count_and_new_flock_types'),
    ]

    operations = [
        # ── Expand flock type choices on Farm ────────────────────────────────
        migrations.AlterField(
            model_name='farm',
            name='flock_type',
            field=models.CharField(
                max_length=25,
                choices=[
                    ('broilers',             'Broilers'),
                    ('layers',               'Layers'),
                    ('guinea_fowl',          'Guinea Fowl'),
                    ('turkey',               'Turkey'),
                    ('duck',                 'Duck'),
                    ('geese',                'Geese'),
                    ('ostrich',              'Ostrich'),
                    ('day_old_chicks',       'Day-Old Chicks'),
                    ('hatchery',             'Hatchery Only'),
                    ('poultry_and_hatchery', 'Poultry + Hatchery'),
                    ('meat_processing',        'Meat Processing Farm'),
                    ('mixed',                'Mixed Poultry'),
                ],
            ),
        ),

        # ── New species count columns on FarmActivityLog ─────────────────────
        migrations.AddField(
            model_name='farmactivitylog',
            name='guinea_fowl_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='farmactivitylog',
            name='turkey_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='farmactivitylog',
            name='duck_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='farmactivitylog',
            name='geese_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='farmactivitylog',
            name='ostrich_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
