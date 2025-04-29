# File: your_app/tasks.py

import frappe
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def mark_ended_events_as_completed():
    """
    This function finds all Town Hall Events whose end date has passed
    and marks them as 'Completed' if not already done.
    """

    now = frappe.utils.now_datetime()

    events = frappe.get_all("Town Hall Event",
        filters={
            "end_datetime": ["<", now],
            "status": ["!=", "Completed"]
        },
        fields=["name"]
    )

    for event in events:
        doc = frappe.get_doc("Town Hall Event", event.name)
        doc.status = "Completed"
        doc.save(ignore_permissions=True)

    frappe.db.commit()