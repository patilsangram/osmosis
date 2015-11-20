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
<<<<<<< HEAD
=======
		project.customer=doc.customer
>>>>>>> 412ce2eac95f6031313180ad26fb8d9966ea6a6f
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

def new_stock_entry(doc, method):
	"""create stock entry on Tool mgmt submt"""
	if doc.tools:
		stk_en = frappe.new_doc("Stock Entry")
		if (doc.tools_status == "Tools Out"):
			stk_en.purpose = "Material Issue"
		elif doc.tools_status == "Tools In":
			stk_en.purpose = "Material Receipt"
		stk_en.tool_management = doc.name
		tool_tab = doc.get("tools")
		for item in tool_tab:
			tool_row = stk_en.append("items")
			tool_row.item_code = item.item_code
			tool_row.qty = item.qty
			tool_row.basic_rate = item.rate
			if doc.tools_status == "Tools Out":
				tool_row.s_warehouse = doc.default_warehouse
			elif doc.tools_status == "Tools In":
				tool_row.t_warehouse = doc.default_warehouse
			# tool_row.t_warehouse = doc.default_warehouse
		stk_en.submit()

def get_stock_item(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select item_code from `tabBin` where actual_qty>0""")


def on_cancel_sales_order(doc,method):
	cancel_stock_entry(doc)
	if(not doc.is_extra_sales_order):
		delete_project(doc)

def cancel_stock_entry(doc):
	stock_entries = frappe.db.sql("""select name from `tabStock Entry` where sales_order='%s'"""%(doc.name))
	if(stock_entries):
		for se in stock_entries:
			stock_e = frappe.get_doc("Stock Entry",se[0])
			stock_e.cancel()

def delete_project(doc):
	project=frappe.db.get_value("Project",{"sales_order":doc.name},"name")
	project_data=frappe.get_doc("Project",project)
	if(project_data.tasks):
		frappe.msgprint(_("Can not cancel sales Order as task created for the project"))
		# project=frappe.db.get_value("Task",{"Project":project_data.name},"name")
	else:
		project_data.delete()
