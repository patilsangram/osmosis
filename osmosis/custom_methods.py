import frappe
from frappe.utils import rounded,money_in_words
from frappe.model.mapper import get_mapped_doc
from frappe import throw, _

def create_project(doc, method):
	"""create new pronect on submit of sales order"""
	if(doc.is_extra_sales_order==True and doc.parent_sales_order):
		pass
	else:
		project = frappe.new_doc("Project")
		project.project_name=doc.project_title
		project.sales_order=doc.name
		print project.sales_order
		project.save(ignore_permissions=True)
		frappe.msgprint(_("{0} created successfully").format(project.project_name))


def make_stock_entry(doc, method):
	"""create stock entry for buy back item on submit of sales order"""
	if doc.buyback_item:
		se = frappe.new_doc("Stock Entry")
		se.purpose = "Material Receipt"
		se.sales_order = doc.name
		bt = doc.get("buyback_item")
		for item in bt:
			bt_row = se.append("items")
			bt_row.item_code = item.item_code
			bt_row.qty = item.quantity
			bt_row.basic_rate = item.rate
			bt_row.t_warehouse = item.warehouse
		se.submit()

