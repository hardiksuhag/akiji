# Generated by Django 2.2.4 on 2020-07-30 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akinator', '0003_auto_20200723_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ans_given',
            field=models.CharField(default='-1', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='ans_real',
            field=models.CharField(default='-1', max_length=100),
        ),
    ]
