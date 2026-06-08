from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produce',
            name='accepts_instant_payment',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='produce',
            name='accepts_cash_on_delivery',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(
                choices=[('instant', 'Instant Payment (MoMo / Card)'), ('cash_on_delivery', 'Cash on Delivery')],
                default='cash_on_delivery',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(
                choices=[('unpaid', 'Unpaid'), ('paid', 'Paid'), ('refunded', 'Refunded')],
                default='unpaid',
                max_length=20,
            ),
        ),
    ]
