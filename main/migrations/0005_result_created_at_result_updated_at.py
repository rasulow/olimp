# Generated by Django 5.1.1 on 2024-10-13 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_result_date_alter_result_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
