# Generated by Django 4.2.5 on 2024-03-10 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce_app', '0008_alter_order_order_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='all_shoes',
            field=models.BinaryField(),
        ),
    ]
