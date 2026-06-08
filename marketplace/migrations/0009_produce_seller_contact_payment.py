from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("marketplace", "0008_remove_order_payment_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="produce",
            name="contact_phone",
            field=models.CharField(
                blank=True,
                max_length=20,
                help_text="Phone number buyers can reach the seller on",
            ),
        ),
        migrations.AddField(
            model_name="produce",
            name="accepts_momo",
            field=models.BooleanField(default=True, help_text="Accept MTN Mobile Money"),
        ),
        migrations.AddField(
            model_name="produce",
            name="accepts_card",
            field=models.BooleanField(default=False, help_text="Accept Card via Paystack"),
        ),
        migrations.AddField(
            model_name="produce",
            name="accepts_bank_transfer",
            field=models.BooleanField(default=False, help_text="Accept Bank Transfer"),
        ),
        migrations.AddField(
            model_name="produce",
            name="accepts_cod",
            field=models.BooleanField(default=True, help_text="Accept Cash on Delivery"),
        ),
    ]
