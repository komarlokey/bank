# Generated by Django 4.2.5 on 2023-11-01 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0005_alter_card_expired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expired',
            field=models.DateField(),
        ),
    ]
