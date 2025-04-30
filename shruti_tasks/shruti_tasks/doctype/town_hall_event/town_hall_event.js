// Copyright (c) 2025, shruti and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Town Hall Event", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Town Hall Event", {
    refresh(frm) {
        // Only add the button once
        if (!frm.custom_buttons["View Registrations"]) {
            frm.add_custom_button(
                __("View Registrations"),
                function () {
                    const event_name = frm.doc.name;
                    const filters = [["town_hall_event", "=", event_name]];

                    frappe.set_route("List", "Town Hall Event Registration", {
                        town_hall_event: event_name
                    });
                },
            );
        }
    }
});