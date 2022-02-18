# Generated by Django 4.0.1 on 2022-02-18 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_remove_rate_rate_rate_value'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='rate',
            constraint=models.UniqueConstraint(fields=('post', 'user'), name='unique_rate'),
        ),
    ]
