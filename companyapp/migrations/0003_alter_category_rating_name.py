# Generated by Django 4.1.4 on 2022-12-16 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companyapp', '0002_rename_liabilities_short_therm_trade_companyratios_liabilities_trade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='rating_name',
            field=models.IntegerField(choices=[(1, 'Low risk'), (2, 'Medium risk'), (3, 'High risk')]),
        ),
    ]