from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_produce_egg_size_produce_type_expanded'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(
                max_length=20,
                choices=[('instant', 'Instant (MoMo/Card)'), ('cash_on_delivery', 'Cash on Delivery')],
                default='instant',
            ),
        ),
    ]
