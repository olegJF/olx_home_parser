# Generated by Django 3.0.4 on 2020-11-16 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0004_auto_20201116_0919'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='realestate',
            options={'ordering': ['updated']},
        ),
        migrations.AlterField(
            model_name='realestate',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
