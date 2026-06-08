from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0006_merge_20260605_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('momo',             'MTN Mobile Money'),
                    ('card',             'Card (Paystack)'),
                    ('bank_transfer',    'Bank Transfer'),
                    ('cash_on_delivery', 'Cash on Delivery'),
                ],
                default='cash_on_delivery',
            ),
        ),
    ]
