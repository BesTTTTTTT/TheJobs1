# Generated by Django 4.2.9 on 2024-02-04 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0013_alter_job_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='Typework',
            field=models.CharField(choices=[('A', 'B'), ('C', 'D'), ('E', 'F'), ('G', 'H'), ('I', 'J')], max_length=20),
        ),
    ]
