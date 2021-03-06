# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-04-16 08:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20190415_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='comment_count',
            field=models.IntegerField(default=0, verbose_name='评论数'),
        ),
        migrations.AddField(
            model_name='article',
            name='down_count',
            field=models.IntegerField(default=0, verbose_name='踩数'),
        ),
        migrations.AddField(
            model_name='article',
            name='up_count',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.FileField(default='avatar/default.png', upload_to='avatar/', verbose_name='头像'),
        ),
    ]
