# Generated by Django 5.1.4 on 2024-12-16 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoanal', '0002_alter_event_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
