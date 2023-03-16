# Generated by Django 4.1.7 on 2023-03-16 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_alter_appointment_slot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='slot',
            field=models.CharField(blank=True, choices=[('1', '1 PM'), ('2', '2 PM'), ('3', '3 PM'), ('4', '4 PM')], max_length=10, null=True),
        ),
    ]
