# Generated by Django 4.2.1 on 2023-06-21 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Daily_posts', '0005_alter_newpost_text_alter_postcomment_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='Daily_posts.newpost'),
        ),
    ]
