# Generated by Django 4.2.11 on 2024-10-09 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_alter_message_sentat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deudas',
            name='dueDate',
            field=models.DateTimeField(),
        ),
    ]
