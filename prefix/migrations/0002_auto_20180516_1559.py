# Generated by Django 2.0.5 on 2018-05-16 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prefix', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='npanxxthrough',
            unique_together={('npanxx_src', 'npanxx_dest')},
        ),
    ]