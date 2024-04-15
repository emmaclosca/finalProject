from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_alter_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(default=''),
        ),
    ]
