# Generated by Django 4.2.6 on 2023-10-23 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_rename_created_post_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
