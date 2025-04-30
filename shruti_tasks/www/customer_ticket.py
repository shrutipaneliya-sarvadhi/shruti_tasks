import frappe
from frappe.utils.user import get_users_with_role
from datetime import date



@frappe.whitelist(allow_guest=True)
def save_ticket():
    today = date.today().strftime("%Y-%m-%d")
    try:
        data = frappe.form_dict
        category = data.get("category")
        
        # Log category and roles
        print(f"Category: {category}")
        
        description = data.get("description", "").lower() if data.get("description") else ""

        # 🧠 Auto-assign category based on description if not provided
        if not category and description:
            if any(word in description for word in ["error", "crash"]):
                category = "Bug"
            elif any(word in description for word in ["bad", "angry", "not working"]):
                category = "Complaint"
            elif any(word in description for word in ["feature", "nice to have"]):
                category = "Suggestion"
            else:
                category = "Other"

        print(f"Final Category: {category}")

        assigned_user = None
        if category == "Bug":
            users = get_users_with_role("Maintenance Manager")
            print(f"Tech Users: {users}")
            assigned_user = users[0] if users else None
        elif category == "Suggestion":
            users = get_users_with_role("Sales Manager")
            print(f"Sales Users: {users}")
            assigned_user = users[0] if users else None
        elif category == "Complaint":
            users = get_users_with_role("Support Team")
            print(f"Support Users: {users}")
            assigned_user = users[0] if users else None
        elif category == "Other":
            users = get_users_with_role("HR Manager")
            print(f"Support Users: {users}")
            assigned_user = users[0] if users else None
        
        # Create ticket
        issue = frappe.get_doc({
            "doctype": "Customer Tickets",
            "customer_name": data.get("customerName"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "category": category,
            "status": "Open",
            "description": data.get("description"),
            "resolution_notes": data.get("resolutionNotes"),
            "assigned_to": assigned_user,
            "date":today
        })
        issue.insert(ignore_permissions=True)
        frappe.db.commit()
        
         # 📧 Send confirmation email to the customer
        customer_email = data.get("email")
        if customer_email:
            try:
                subject = "Ticket Submission Confirmation"
                message = """
                    <p>Dear {name},</p>
                    <p>Your ticket has been successfully submitted. Here are the details:</p>
                    <ul>
                        <li><strong>Ticket ID:</strong> {id}</li>
                        <li><strong>Category:</strong> {category}</li>
                        <li><strong>Description:</strong> {desc}</li>
                        <li><strong>Status:</strong> Open</li>
                    </ul>
                    <p>We will address your request shortly.</p>
                    <p>Best regards,<br/><em>Customer Support Team</em></p>
                """.format(
                    name=data.get("customerName"),
                    id=issue.name,
                    category=category,
                    desc=data.get("description")
                )

                frappe.sendmail(
                    recipients=[customer_email],
                    subject=subject,
                    message=message,
                    header=("Ticket Notification", "green"),
                    reference_doctype="Customer Tickets",
                    reference_name=issue.name
                )
                frappe.enqueue("frappe.email.queue.flush")

            except Exception as email_error:
                frappe.log_error(
                    frappe.get_traceback(),
                    "Failed to send confirmation email for ticket: {0}".format(issue.name)
                )


        return {"message": "Ticket submitted successfully!"}
    
    except Exception as e:
        print("error")