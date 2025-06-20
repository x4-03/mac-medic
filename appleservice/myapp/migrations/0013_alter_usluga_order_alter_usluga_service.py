# Generated by Django 5.2.1 on 2025-06-10 11:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_alter_usluga_price_alter_usluga_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usluga',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usluga', to='myapp.zlecenie'),
        ),
        migrations.AlterField(
            model_name='usluga',
            name='service',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
