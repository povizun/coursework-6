# Generated by Django 5.0.4 on 2024-05-31 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_alter_blogpost_creator_alter_blogpost_image_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'permissions': [('can_view_all_mailings', 'Can view all mailings'), ('can_change_status', 'Can change status of all mailings')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]