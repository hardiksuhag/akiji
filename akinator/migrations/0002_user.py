# Generated by Django 2.2.4 on 2020-07-22 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akinator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=100)),
                ('time_active', models.CharField(max_length=100)),
                ('prob_data', models.CharField(max_length=100)),
            ],
        ),
    ]
