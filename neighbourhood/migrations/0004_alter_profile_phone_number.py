# Generated by Django 4.2.5 on 2024-02-28 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neighbourhood', '0003_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
