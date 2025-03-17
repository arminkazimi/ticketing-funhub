# Generated by Django 5.1.7 on 2025-03-16 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0002_alter_ticket_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ticket",
            name="attachment",
        ),
        migrations.RemoveField(
            model_name="ticket",
            name="description",
        ),
        migrations.AddField(
            model_name="ticketmessage",
            name="attachment",
            field=models.FileField(
                blank=True, null=True, upload_to="ticket_attachments/"
            ),
        ),
    ]
