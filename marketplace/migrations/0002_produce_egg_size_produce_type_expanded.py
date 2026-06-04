from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produce',
            name='egg_size',
            field=models.CharField(
                blank=True, null=True, max_length=10,
                choices=[('small','Small'),('medium','Medium'),('large','Large'),('jumbo','Jumbo')],
                help_text='Only applicable when produce_type is eggs',
            ),
        ),
        migrations.AlterField(
            model_name='produce',
            name='produce_type',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('broilers','Broilers'),
                    ('eggs','Eggs'),
                    ('layers','Layer Birds'),
                    ('day_old','Day-old Chicks'),
                    ('smoked','Smoked Chicken'),
                    ('guinea_fowl','Guinea Fowl'),
                    ('turkey','Turkey'),
                    ('duck','Duck'),
                    ('quail','Quail'),
                    ('other','Other'),
                ],
            ),
        ),
    ]
