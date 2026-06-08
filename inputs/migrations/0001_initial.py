import uuid
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InputDealerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=200)),
                ('registration_number', models.CharField(blank=True, max_length=100)),
                ('region', models.CharField(blank=True, max_length=100)),
                ('district', models.CharField(blank=True, max_length=100)),
                ('address', models.TextField(blank=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('product_categories', models.JSONField(default=list)),
                ('approval_status', models.CharField(choices=[('pending','Pending'),('approved','Approved'),('suspended','Suspended')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_dealers', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dealer_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={'db_table': 'input_dealer_profiles'},
        ),
        migrations.CreateModel(
            name='FarmInput',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('input_type', models.CharField(choices=[('feed','Feed'),('vaccine','Vaccine'),('medication','Medication'),('equipment','Equipment'),('supplement','Supplement'),('disinfectant','Disinfectant'),('other','Other')], max_length=15)),
                ('brand', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('unit', models.CharField(max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity_available', models.PositiveIntegerField(default=0)),
                ('min_order_quantity', models.PositiveIntegerField(default=1)),
                ('region', models.CharField(blank=True, max_length=100)),
                ('is_available', models.BooleanField(default=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='inputs/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='input_listings', to=settings.AUTH_USER_MODEL)),
            ],
            options={'db_table': 'farm_inputs', 'ordering': ['-created_at']},
        ),
    ]
