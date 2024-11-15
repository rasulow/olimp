# Generated by Django 5.1.1 on 2024-10-11 16:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(choices=[(1, 'first place'), (2, 'second place'), (3, 'third place')], default=1)),
                ('category', models.ForeignKey(limit_choices_to={'id__in': ()}, on_delete=django.db.models.deletion.CASCADE, to='main.category')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student')),
            ],
        ),
    ]
