# Generated by Django 2.2.4 on 2020-08-02 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akinator', '0004_auto_20200730_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='name',
            name='search_count',
            field=models.CharField(default='0', max_length=10),
        ),
    ]