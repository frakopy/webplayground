# Generated by Django 4.1.1 on 2022-10-29 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0005_alter_thread_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='thread',
            options={'ordering': ['updated']},
        ),
    ]
