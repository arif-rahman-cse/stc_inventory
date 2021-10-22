# Generated by Django 3.2.8 on 2021-10-22 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesparent',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='salesparent',
            name='status',
            field=models.CharField(default='Open', max_length=20),
        ),
    ]
