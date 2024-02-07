# Generated by Django 4.2.9 on 2024-02-06 11:47

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0015_custom_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='custom',
            name='cv_file',
            field=models.FileField(blank=True, default='', null=True, upload_to='cv_files/'),
        ),
        migrations.AddField(
            model_name='custom',
            name='date_applied',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='custom',
            name='position_applied',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='custom',
            name='source',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='custom',
            name='status',
            field=models.CharField(default='Pending', max_length=100),
        ),
        migrations.AddField(
            model_name='custom',
            name='tal_phon',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='custom',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobapp.company'),
        ),
        migrations.AlterField(
            model_name='job',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
