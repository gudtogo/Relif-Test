# Generated by Django 4.2.11 on 2024-10-09 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_alter_message_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='role',
            field=models.CharField(blank=True, choices=[('client', 'client'), ('agent', 'agent')], max_length=100, null=True),
        ),
    ]
