from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='priority',
            field=models.CharField(
                max_length=10,
                choices=[('low','Low'),('medium','Medium'),('high','High'),('urgent','Urgent')],
                default='medium',
            ),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_object_type',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_object_id',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notif_type',
            field=models.CharField(
                max_length=30,
                choices=[
                    ('application_status',     'Application Status'),
                    ('repayment_due',          'Repayment Due'),
                    ('repayment_received',     'Repayment Received'),
                    ('contract_signed',        'Contract Signed'),
                    ('disbursement',           'Disbursement'),
                    ('order_update',           'Order Update'),
                    ('training_new',           'New Training'),
                    ('credit_workflow',        'Credit Workflow'),
                    ('new_opportunity',        'New Opportunity'),
                    ('agreement_created',      'Agreement Created'),
                    ('contract_generated',     'Contract Generated'),
                    ('disbursement_requested', 'Disbursement Requested'),
                    ('disbursement_approved',  'Disbursement Approved'),
                    ('disbursement_rejected',  'Disbursement Rejected'),
                    ('action_required',        'Action Required'),
                    ('system',                 'System'),
                ],
            ),
        ),
    ]
