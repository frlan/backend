# Generated by Django 3.2.4 on 2021-07-19 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wp_party', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='id',
            field=models.SmallAutoField(primary_key=True, serialize=False),
        ),
    ]
