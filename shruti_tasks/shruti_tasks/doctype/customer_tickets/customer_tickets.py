# Copyright (c) 2025, shruti and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CustomerTickets(Document):
    
                
    def after_insert(self):
        """Notify assignee and customer if the ticket was created with an assigned user."""
        if self.assigned_to:
            self.notify_new_assignee(self.assigned_to)
            self.notify_customer_of_assignment()

    def on_update(self):
        """Trigger actions on ticket updates."""
        # Track changes in assigned_to
        if self.has_value_changed("assigned_to"):
            old_assigned_to = self.get_doc_before_save().assigned_to
            new_assigned_to = self.assigned_to
            if old_assigned_to != new_assigned_to and new_assigned_to:
                self.notify_new_assignee(new_assigned_to)
                self.notify_customer_of_assignment()

        # Trigger feedback request on resolution
        if self.has_value_changed("status") and self.status == "Resolved":
            self.send_feedback_request()

    def notify_new_assignee(self, user_email):
        """Send email notification to newly assigned user."""
        try:
            user = frappe.get_doc("User", user_email)
            subject = f"New Ticket Assigned: {self.name}"
            message = f"""
                <p>Hello {user.full_name},</p>
                <p>You've been assigned a new ticket.</p>
                <p><strong>Ticket:</strong> {self.name}</p>
                <p><strong>Category:</strong> {self.category}</p>
                <p><strong>Description:</strong> {self.description}</p>
                <p>Please review and process the ticket.</p>
                <p>Best regards,<br/><em>Support System</em></p>
            """

            frappe.sendmail(
                recipients=[user.email],
                subject=subject,
                message=message,
                header=["Ticket Assignment", "blue"],
                reference_doctype=self.doctype,
                reference_name=self.name
            )
            frappe.enqueue("frappe.email.queue.flush")

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                f"Failed to notify assignee {user_email} for ticket {self.name}"
            )

    def notify_customer_of_assignment(self):
        """Notify the customer that the ticket has been assigned to a support agent."""
        if not self.email:
            return

        try:
            assignee = frappe.get_cached_value("User", self.assigned_to, "full_name")
            subject = f"Your Ticket {self.name} Has Been Assigned"
            message = f"""
                <p>Dear Valued Customer,</p>
                <p>Your ticket <strong>{self.name}</strong> has been assigned to <strong>{assignee}</strong>.</p>
                <p>The assigned agent will reach out soon to assist you.</p>
                <p>Best regards,<br/><em>Customer Support Team</em></p>
            """

            frappe.sendmail(
                recipients=[self.email],
                subject=subject,
                message=message,
                header=["Ticket Update", "orange"],
                reference_doctype=self.doctype,
                reference_name=self.name
            )
            frappe.enqueue("frappe.email.queue.flush")

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                f"Failed to notify customer for ticket {self.name} on assignment"
            )

    def send_feedback_request(self):
        """Send feedback request email to the customer when the ticket is resolved."""
        try:
            customer_email = self.email
            feedback_url = f"http://shruti_tasks.localhost:8004/feedback"

            subject = "Please Share Your Feedback"
            message = f"""
                <p>Dear Valued Customer,</p>
                <p>Your ticket <strong>{self.name}</strong> has been successfully resolved.</p>
                <p>We value your feedback and would greatly appreciate it if you could share your experience:</p>
                <p><a href="{feedback_url}" style="display: inline-block; padding: 10px 20px; background-color: #28a745; color: white; text-decoration: none; border-radius: 4px;">Leave Feedback</a></p>
                <p>Thank you for choosing our services!</p>
                <p>Best regards,<br/><em>Customer Support</em></p>
            """

            frappe.sendmail(
                recipients=[customer_email],
                subject=subject,
                message=message,
                header=["Feedback Request", "green"],
                reference_doctype=self.doctype,
                reference_name=self.name
            )
            frappe.enqueue("frappe.email.queue.flush")

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                f"Failed to send feedback request for ticket {self.name}"
            )