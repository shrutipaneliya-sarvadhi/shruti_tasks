import frappe
from frappe.utils import nowdate

@frappe.whitelist(allow_guest=True)
def send_daily_ticket_summary():
    tickets = frappe.get_all("Customer Tickets", 
        filters={"creation": [">=", frappe.utils.today()]},
        fields=["name", "category", "description", "assigned_to"]
    )
    assignments = {}
    for t in tickets:
        if t.assigned_to:
            assignments.setdefault(t.assigned_to, []).append(t)

    for user, tickets in assignments.items():
        subject = f"Daily Ticket Summary - {len(tickets)} New Tickets"
        message = "<h3>New Tickets Today:</h3><ul>"
        for t in tickets:
            message += f"""
                <li>
                    <strong>{t.name}</strong> ({t.category})<br>
                    Description: {t.description}
                </li>
            """
        message += "</ul>"

        e=frappe.sendmail(
            # recipients=[user],
            recipients=["shrutipaneliya.sarvadhi@gmail.com"],
            subject=subject,
            message=message,
            delayed=False, 
        )
        frappe.enqueue("frappe.email.queue.flush")

        if e:
            print("Emails send")
    
    return "Mail Sended"



@frappe.whitelist(allow_guest=True)
def send_ticket_reminders_3():
    pending_tickets = frappe.get_all(
        "Customer Tickets",
        filters={
            "status": ["in", ["Open", "In Progress"]],
            "assigned_to": ["!=", ""]
        },
        fields=["name", "customer_name", "assigned_to", "status", "date"]
    )

    for ticket in pending_tickets:
        if ticket.date and frappe.utils.date_diff(nowdate(), ticket.date) >= 3:
            print("yeesssss",ticket)
            user_email = frappe.db.get_value("User", ticket.assigned_to, "email")
            if user_email:
                frappe.sendmail(
                    now=True,
                    # recipients=[user_email],
                    recipients=["shrutipaneliya.sarvadhi@gmail.com"],
                    subject=f"Reminder: Ticket {ticket.name} is still {ticket.status}",
                    message=f"""Dear {ticket.assigned_to},<br><br>
                    The ticket <b>{ticket.name}</b> for customer <b>{ticket.customer_name}</b> has been in <b>{ticket.status}</b> status for more than 3 days.<br>
                    Please review and take necessary action.<br><br>
                    Regards,<br>Your Support Team"""
                )

    return "Mail Sended"


@frappe.whitelist(allow_guest=True)
def auto_close_old_tickets_7():
    tickets = frappe.get_all(
        "Customer Tickets",
        filters={
            "status": ["in", ["Resolved"]],
            "assigned_to": ["!=", ""],
        },
        fields=["name", "date", "status"]
    )
    
    for ticket in tickets:
        if ticket.date and frappe.utils.date_diff(nowdate(), ticket.date) >= 7:
            frappe.db.set_value("Customer Tickets", ticket.name, "status", "Closed")
            frappe.db.commit()
            print(f"Ticket {ticket.name} closed due to inactivity.")
    
    return "Ticketd Closed"

