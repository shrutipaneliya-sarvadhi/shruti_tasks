# Copyright (c) 2025, shruti and contributors
# For license information, please see license.txt

import frappe

# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data

def execute(filters=None):
    columns = [
        {
            "label": "Metric",
            "fieldname": "metric",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "Value",
            "fieldname": "value",
            "fieldtype": "Int",
            "width": 150
        }
    ]

    # Query data
   

    upcoming_events = frappe.db.sql("""
        SELECT COUNT(*) FROM `tabTown Hall Event`
        WHERE status = 'Upcoming'
    """, as_dict=0)[0][0]

    total_registrations = frappe.db.sql("""
        SELECT COUNT(*) FROM `tabTown Hall Event Registration`
    """, as_dict=0)[0][0]

    # Optional: Participation by event (for chart)
    participation_by_event = frappe.db.sql("""
        SELECT t1.event_name, COUNT(t2.name) AS registrations
        FROM `tabTown Hall Event` t1
        LEFT JOIN `tabTown Hall Event Registration` t2
        ON t1.name = t2.town_hall_event
        GROUP BY t1.name
    """, as_dict=1)

    # Prepare data
    data = [
        {"metric": "Upcoming Events", "value": upcoming_events},
        {"metric": "Total Registrations", "value": total_registrations}
    ]

    chart = None
    if participation_by_event:
        labels = [row["event_name"] for row in participation_by_event]
        values = [row["registrations"] for row in participation_by_event]

        chart = {
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "name": "Registrations",
                        "values": values
                    }
                ]
            },
            "type": "bar"
        }

    return columns, data, None, chart