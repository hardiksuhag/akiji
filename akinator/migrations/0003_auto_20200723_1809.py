# Generated by Django 2.2.4 on 2020-07-23 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('akinator', '0002_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_name', models.CharField(default='defaultmem', max_length=100)),
                ('times_searched', models.CharField(default='0', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(default='defaultques', max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='prob_data',
        ),
        migrations.AddField(
            model_name='user',
            name='history',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='prob_list',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='name',
            name='name_text',
            field=models.CharField(default='defaultname', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='ip_address',
            field=models.CharField(default='defaultip', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='time_active',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('times_yes', models.CharField(default='0', max_length=100)),
                ('times_total', models.CharField(default='1', max_length=100)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='akinator.Member')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='akinator.Question')),
            ],
        ),
    ]
