from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('farms', '0001_initial'),
        ('marketplace', '0002_payment_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='produce',
            name='egg_size',
            field=models.CharField(
                blank=True, null=True,
                choices=[
                    ('small', 'Small (< 53g)'),
                    ('medium', 'Medium (53–63g)'),
                    ('large', 'Large (63–73g)'),
                    ('extra_large', 'Extra Large (> 73g)'),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='produce',
            name='farm',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='listings',
                to='farms.farm',
            ),
        ),
    ]
