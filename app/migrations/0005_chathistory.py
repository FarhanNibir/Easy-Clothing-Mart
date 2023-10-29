# Generated by Django 4.2 on 2023-10-06 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_product_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChatHistory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_message", models.TextField()),
                ("bot_response", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]