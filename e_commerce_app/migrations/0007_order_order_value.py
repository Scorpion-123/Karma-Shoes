# Generated by Django 4.2.5 on 2024-03-09 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce_app', '0006_order_order_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_value',
            field=models.IntegerField(default=False),
            preserve_default=False,
        ),
    ]
