# Generated by Django 5.0.3 on 2024-04-14 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0017_alter_post_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="name",
            field=models.CharField(default="2", max_length=255),
        ),
        migrations.AlterField(
            model_name="comment",
            name="posts_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="blog.post",
            ),
        ),
    ]
