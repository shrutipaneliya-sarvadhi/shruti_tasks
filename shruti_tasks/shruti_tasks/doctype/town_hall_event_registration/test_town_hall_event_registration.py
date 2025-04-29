# Copyright (c) 2025, shruti and Contributors
# See license.txt

import frappe
from frappe.model.document import Document

class TownHallEventRegistration(Document):
    def validate(self):
        frappe.msgprint("Calling validate...")
        print("..................#######calliog")
        # Fetch the linked event
        event = frappe.get_doc("Town Hall Event", self.town_hall_event)
        print(event)
        # Count confirmed registrations for this event
        confirmed_regs = frappe.db.count(
            "Town Hall Event Registration",
            {
                "town_hall_event": event.name,
                "status": "Confirmed"
            }
        )
        print(confirmed_regs)
        # Check if max participants reached
        if confirmed_regs >= event.max_participants:
            print("erreoe")
            frappe.throw(f"Cannot register. Maximum participant limit of {event.max_participants} has been reached for the event '{event.event_name}'.")
