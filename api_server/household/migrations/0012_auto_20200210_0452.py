# Generated by Django 3.0.3 on 2020-02-09 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0011_auto_20200210_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household_individual',
            name='spouse',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
