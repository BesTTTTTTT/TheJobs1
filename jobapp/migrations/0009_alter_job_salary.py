# Generated by Django 4.2.9 on 2024-01-28 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0008_job_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='salary',
            field=models.CharField(max_length=255),
        ),
    ]