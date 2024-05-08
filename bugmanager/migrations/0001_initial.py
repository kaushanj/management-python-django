# Generated by Django 5.0.4 on 2024-05-07 08:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("cloudwatch", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Developer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_developer", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Bug",
            fields=[
                (
                    "bug_id",
                    models.CharField(
                        max_length=255, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("resolved", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "dimension",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cloudwatch.dimension",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BugOwner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "bug",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="developers",
                        to="bugmanager.bug",
                    ),
                ),
            ],
        ),
    ]
