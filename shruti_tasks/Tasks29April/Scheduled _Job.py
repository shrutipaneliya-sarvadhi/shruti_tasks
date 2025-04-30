import frappe
from datetime import datetime
from frappe.utils import now_datetime

@frappe.whitelist(allow_guest=True)
def mark_ended_events_as_completed():
    """
    This function finds all Town Hall Events whose end date has passed
    and marks them as 'Completed' if not already done.
    Returns a JSON-compatible dict with the result/status for API use.
    """

    try:
        now = now_datetime()

        events = frappe.get_all("Town Hall Event",
            filters={
                "end_datetime": ["<", now],
                "status": ["!=", "Completed"]
            },
            fields=["name"]
        )

        if not events:
            message = "No Town Hall Events to update. All ended events are already marked as Completed."
            frappe.logger().info(message)
            return {"status": "success", "message": message}

        updated_events = []

        for event in events:
            try:
                doc = frappe.get_doc("Town Hall Event", event.name)
                doc.status = "Completed"
                doc.save(ignore_permissions=True)
                updated_events.append(doc.name)
                frappe.logger().debug(f"Marked Town Hall Event {doc.name} as Completed.")
            except Exception as e:
                frappe.logger().error(f"Failed to update Town Hall Event {event.name}: {str(e)}", exc_info=True)

        frappe.db.commit()

        success_msg = f"Successfully marked {len(updated_events)} event(s) as Completed: {', '.join(updated_events)}"
        frappe.logger().info(success_msg)
        return {
            "status": "success",
            "message": success_msg,
            "completed_events": updated_events
        }

    except Exception as e:
        error_msg = f"Error in mark_ended_events_as_completed task: {str(e)}"
        frappe.log_error(error_msg, "Town Hall Event Auto-Completion Task")
        frappe.db.rollback()
        return {
            "status": "error",
            "message": error_msg
        }



# import frappe
# from datetime import datetime

# @frappe.whitelist(allow_guest=True)
# def mark_ended_events_as_completed():
#     """
#     This function finds all Town Hall Events whose end date has passed
#     and marks them as 'Completed' if not already done.
#     """

#     now = frappe.utils.now_datetime()

#     events = frappe.get_all("Town Hall Event",
#         filters={
#             "end_datetime": ["<", now],
#             "status": ["!=", "Completed"]
#         },
#         fields=["name"]
#     )

#     for event in events:
#         doc = frappe.get_doc("Town Hall Event", event.name)
#         doc.status = "Completed"
#         doc.save(ignore_permissions=True)

#     frappe.db.commit()