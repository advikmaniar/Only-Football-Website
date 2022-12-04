# Generated by Django 4.1.2 on 2022-11-18 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_item_category_alter_item_label"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="category",
            field=models.CharField(
                choices=[
                    ("K", "Kits"),
                    ("B", "Balls"),
                    ("A", "Accessories"),
                    ("F", "Footwear"),
                    ("M", "Men"),
                    ("W", "Women"),
                ],
                max_length=2,
            ),
        ),
    ]
