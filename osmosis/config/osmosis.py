from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Documents"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Nature of Complaint",
					"description": _("Complaints details."),
				},
				{
					"type": "doctype",
					"name": "Tool Management",
					"description": _("Tools work and transaction."),
				},
			]	
		},
		{
			"label":_("Masters"),
			"icon":"icon-star",
			"items": [
					{
					"type":"doctype",
					"name":"Nature of Work",
					"description":_("Work details."),
					},
					{
					"type":"doctype",
					"name":"Suburb",
					"description":_("List of suburb."),
					},
				]
		},
	]
