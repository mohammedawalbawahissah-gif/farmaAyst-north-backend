from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("farms", "0006_farm_monitoring_officer"),
    ]

    operations = [
        # Hatchery fields
        migrations.AddField(
            model_name="farmactivitylog",
            name="eggs_in_incubation",
            field=models.PositiveIntegerField(default=0, help_text="Number of eggs currently in incubator"),
        ),
        migrations.AddField(
            model_name="farmactivitylog",
            name="eggs_set_today",
            field=models.PositiveIntegerField(default=0, help_text="Eggs placed in incubator today"),
        ),
        migrations.AddField(
            model_name="farmactivitylog",
            name="chicks_hatched",
            field=models.PositiveIntegerField(default=0, help_text="Chicks successfully hatched today"),
        ),
        migrations.AddField(
            model_name="farmactivitylog",
            name="hatch_rejects",
            field=models.PositiveIntegerField(default=0, help_text="Unhatched / infertile eggs removed"),
        ),
        migrations.AddField(
            model_name="farmactivitylog",
            name="chicks_sold",
            field=models.PositiveIntegerField(default=0, help_text="Day-old chicks sold/dispatched today"),
        ),
        # Meat processing fields
        migrations.AddField(
            model_name="farmactivitylog",
            name="birds_received",
            field=models.PositiveIntegerField(default=0, help_text="Live birds received for processing"),
        ),
        migrations.AddField(
            model_name="farmactivitylog",
            name="birds_processed",
            field=models.PositiveIntegerField(default=0, help_text="Birds processed/slaughtered today"),
        ),
        migrations.AddField(
            model_name="farmactivitylog",
            name="carcass_weight_kg",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                help_text="Total dressed carcass weight (kg)",
            ),
        ),
        migrations.AddField(
            model_name="farmactivitylog",
            name="units_packaged",
            field=models.PositiveIntegerField(default=0, help_text="Packaged units (portions, whole birds, etc.)"),
        ),
        migrations.AddField(
            model_name="farmactivitylog",
            name="cold_storage_units",
            field=models.PositiveIntegerField(default=0, help_text="Units moved to cold storage"),
        ),
    ]
