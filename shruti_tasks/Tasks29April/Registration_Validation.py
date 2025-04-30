import frappe

def validate_reg(self, doc):
    """
    Validates whether the participant limit for a Town Hall Event has been reached.
    Throws an exception if the max participants limit is exceeded.
    """

    try:
        # Ensure the event exists
        if not self.town_hall_event:
            frappe.throw("Event reference is missing. Cannot proceed with validation.")

        event = frappe.get_doc("Town Hall Event", self.town_hall_event)

        if not event.max_participants:
            frappe.throw(f"Maximum participants limit is not defined for the event '{event.event_name}'.")

        # Count confirmed registrations
        confirmed_regs = frappe.db.count(
            "Town Hall Event Registration",
            {
                "town_hall_event": event.name,
                "status": "Confirmed"
            }
        )

        if confirmed_regs >= event.max_participants:
            msg = f"Cannot register. Maximum participant limit of {event.max_participants} has been reached for the event '{event.event_name}'."
            frappe.throw(msg)

    except frappe.DoesNotExistError as e:
        frappe.throw("The selected event does not exist.")
        frappe.db.rollback()

    except Exception as e:
        frappe.throw("An unexpected error occurred during registration. Please try again later.")
        frappe.db.rollback()



# import frappe

# def validate_reg(self,doc):

#         event = frappe.get_doc("Town Hall Event", self.town_hall_event)
#         print(event)
#         confirmed_regs = frappe.db.count(
#             "Town Hall Event Registration",
#             {
#                 "town_hall_event": event.name,
#                 "status": "Confirmed"
#             }
#         )
#         print(confirmed_regs)
#         if confirmed_regs >= event.max_participants:
#             print("error")
#             frappe.throw(f"Cannot register. Maximum participant limit of {event.max_participants} has been reached for the event '{event.event_name}'.")
