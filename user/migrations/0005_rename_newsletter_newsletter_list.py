# Generated by Django 4.2.6 on 2023-10-28 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_newsletter_profile_new_post_email'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='newsletter',
            new_name='Newsletter_list',
        ),
    ]
