# Generated by Django 5.1.6 on 2025-02-16 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("deck", "0005_mulliganresult"),
    ]

    operations = [
        migrations.AlterField(
            model_name="card",
            name="category",
            field=models.CharField(
                choices=[
                    ("ポケモン", "ポケモン"),
                    ("たねポケモン", "たねポケモン"),
                    ("グッズ", "グッズ"),
                    ("サポート", "サポート"),
                    ("ポケモンのどうぐ", "ポケモンのどうぐ"),
                    ("スタジアム", "スタジアム"),
                    ("エネルギー", "エネルギー"),
                ],
                max_length=20,
            ),
        ),
    ]
