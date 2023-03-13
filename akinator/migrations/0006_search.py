# Generated by Django 2.2.4 on 2020-08-03 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akinator', '0005_name_search_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_time', models.DateTimeField(verbose_name='time of search')),
                ('name_searched', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
