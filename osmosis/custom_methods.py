import frappe
from frappe.utils import rounded,money_in_words
from frappe.model.mapper import get_mapped_doc



def create_project(doc, method):
	"""create new pronect on submit of sales order"""
	project = frappe.new_doc("Project")
	project.project_name=doc.name
	project.sales_order=doc.name
	project.save(ignore_permissions=True)
	frappe.msgprint("%s created successfully",project.project_name)

@frappe.whitelist()
def make_extra_sales_order(source_name, target_doc=None):
	doclist = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Sales Order",
			"validation": {
				"docstatus": ["=", 0]
			}
		},
		"Sales Order Item": {
			"doctype": "Sales Order Item",
			"field_map": {
				"name": "so_detail",
				"parent": "sales_order",
			},
		},
		"Sales Taxes and Charges": {
			"doctype": "Sales Taxes and Charges",
			"add_if_empty": True
		},
		"Sales Team": {
			"doctype": "Sales Team",
			"add_if_empty": True
		}
	}, target_doc)

	return doclist
