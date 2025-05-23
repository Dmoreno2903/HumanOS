# Generated by Django 5.2.1 on 2025-05-11 04:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_us', '0006_merge_20250511_0253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backgroundpersonmodel',
            name='candidate',
            field=models.ForeignKey(help_text='Candidate that has the background', on_delete=django.db.models.deletion.DO_NOTHING, related_name='backgrounds', to='work_us.candidatemodel', verbose_name='Candidate'),
        ),
    ]
