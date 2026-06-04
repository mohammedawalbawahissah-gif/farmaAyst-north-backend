from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingmodule',
            name='scheduled_at',
            field=models.DateTimeField(blank=True, null=True, help_text='Date & time for live webinar/workshop'),
        ),
        migrations.AddField(
            model_name='trainingmodule',
            name='meeting_url',
            field=models.URLField(blank=True, help_text='Google Meet or Zoom link'),
        ),
        migrations.AddField(
            model_name='trainingmodule',
            name='meeting_platform',
            field=models.CharField(
                blank=True, max_length=20,
                choices=[('google_meet','Google Meet'),('zoom','Zoom'),('other','Other')],
            ),
        ),
        migrations.AlterField(
            model_name='trainingmodule',
            name='module_type',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('video','Video'),
                    ('pdf','PDF Guide'),
                    ('audio','Audio'),
                    ('document','Document'),
                    ('webinar','Live Webinar'),
                    ('workshop','Workshop'),
                    ('quiz','Quiz'),
                ],
            ),
        ),
    ]
