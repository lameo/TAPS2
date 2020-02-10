# Generated by Django 3.0.3 on 2020-02-08 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0006_auto_20200208_1930'),
    ]

    operations = [
        migrations.CreateModel(
            name='household_individual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('marital_status', models.CharField(max_length=100)),
                ('spouse', models.CharField(max_length=100)),
                ('occupation_type', models.CharField(max_length=100)),
                ('annual_income', models.CharField(max_length=100)),
                ('DOB', models.CharField(max_length=100)),
                ('householdID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family_members', to='household.Household')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('householdID', 'name')},
            },
        ),
        migrations.DeleteModel(
            name='Track',
        ),
    ]
