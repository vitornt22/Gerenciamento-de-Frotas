# Generated by Django 4.0.4 on 2022-07-24 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_alter_contract_chassi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='chassi',
            field=models.CharField(max_length=21, unique=True),
        ),
    ]
