# File: your_app/api.py

import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def register_for_event():
    data = frappe.form_dict

    required_fields = ["event", "full_name", "email", "phone"]
    for field in required_fields:
        if not data.get(field):
            frappe.throw(_("Missing required field: {0}").format(_(field)))

    event_name = data.get("event")
    full_name = data.get("full_name")
    email = data.get("email")
    phone = data.get("phone")

    try:
        event = frappe.get_doc("Town Hall Event", event_name)

        confirmed_regs = frappe.db.count(
            "Town Hall Event Registration",
            {
                "town_hall_event": event_name,
                "status": "Confirmed"
            }
        )

        if confirmed_regs >= event.max_participants:
            frappe.throw(_("Maximum participant limit has been reached for this event."))

        registration = frappe.get_doc({
            "doctype": "Town Hall Event Registration",
            "town_hall_event": event_name,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "status": "Pending"  # Default status
        })

        send_registration_confirmation_email(registration, event)

        registration.insert(ignore_permissions=True)
        frappe.db.commit()

        return {
            "message": "Registration successful",
            "registration_id": registration.name
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Event Registration Error"))
        frappe.throw(_("Failed to register: {0}").format(str(e)))


def send_registration_confirmation_email(registration, event):
    subject = f"Thank You for Registering for {event.event_name}"

    # Format dates in readable format
    start_time = frappe.utils.format_datetime(event.start_datetime, "medium")
    end_time = frappe.utils.format_datetime(event.end_datetime, "medium")

    # Simple HTML or plain text message
    message = f"""
    <h3>Dear {registration.full_name},</h3>

    <p>Thank you for registering for the event: <strong>{event.event_name}</strong></p>

    <p><strong>Event Details:</strong></p>
    <ul>
        <li><strong>Start:</strong> {start_time}</li>
        <li><strong>End:</strong> {end_time}</li>
    </ul>

    <p>We look forward to seeing you there!</p>

    <p>Best regards,<br>Town Hall Team</p>
    """

    frappe.sendmail(
        recipients=[registration.email],
        sender=None,  # Will use default outgoing email account
        subject=subject,
        message=message,
        header=["Registration Confirmation", "green"]
    )
    frappe.enqueue("frappe.email.queue.flush")

    return {
            "message": "Email Sended",
        }