# Generated by Django 3.1.4 on 2021-04-29 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='farm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.farm'),
        ),
    ]