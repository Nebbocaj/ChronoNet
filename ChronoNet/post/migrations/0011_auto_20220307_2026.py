# Generated by Django 3.2.10 on 2022-03-07 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_post_expires_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='views',
        ),
        migrations.RemoveField(
            model_name='post',
            name='views_allowed',
        ),
        migrations.RemoveField(
            model_name='post',
            name='views_left',
        ),
    ]
