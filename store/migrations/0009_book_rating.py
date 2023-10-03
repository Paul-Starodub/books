# Generated by Django 4.2.5 on 2023-10-03 16:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0008_book_readers"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="rating",
            field=models.DecimalField(
                decimal_places=2, default=None, max_digits=3, null=True
            ),
        ),
    ]
