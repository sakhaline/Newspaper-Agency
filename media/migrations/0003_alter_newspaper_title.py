# Generated by Django 4.2.7 on 2023-11-23 04:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("media", "0002_alter_redactor_years_of_experience"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newspaper",
            name="title",
            field=models.CharField(max_length=255),
        ),
    ]