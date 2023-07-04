# Generated by Django 3.2.10 on 2022-03-22 15:07

from django.db import migrations
import markdownfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_post_expires_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='text_rendered',
            field=markdownfield.models.RenderedMarkdownField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=markdownfield.models.MarkdownField(rendered_field='text_rendered'),
        ),
    ]
