# Generated by Django 5.1.7 on 2025-03-16 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0003_remove_ticket_attachment_remove_ticket_description_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ticket",
            options={
                "ordering": ["-created_at"],
                "permissions": [
                    ("can_view_all_tickets", "Can view all tickets"),
                    ("can_reply_to_tickets", "Can reply to tickets"),
                ],
            },
        ),
    ]
