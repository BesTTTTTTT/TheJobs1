# Generated by Django 4.2.9 on 2024-01-28 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0007_alter_job_typework'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='salary',
            field=models.CharField(default='10000', max_length=255),
        ),
    ]
