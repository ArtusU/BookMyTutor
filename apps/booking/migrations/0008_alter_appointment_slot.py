# Generated by Django 4.1.7 on 2023-03-18 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_alter_appointment_slot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='slot',
            field=models.CharField(blank=True, choices=[('10 am', '10 am'), ('11 am', '11 am'), ('12 pm', '12 pm'), ('2 pm', '2 pm'), ('3 pm', '3 pm'), ('4 pm', '4 pm')], max_length=10, null=True),
        ),
    ]
