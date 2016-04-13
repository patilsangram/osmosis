import frappe
from frappe.utils import rounded,money_in_words, nowdate
from frappe.model.mapper import get_mapped_doc
from frappe import throw, _
from erpnext.controllers.queries import get_filters_cond, get_match_cond

def create_project(doc, method):
	"""create new project on submit of sales order"""
	if(doc.is_extra_sales_order==True and doc.parent_sales_order):
		pass
	else:
		project = frappe.new_doc("Project")
		project.project_name=doc.project_title
		project.sales_order=doc.name
		project.expected_start_date=doc.transaction_date
		project.customer=doc.customer
		project.save(ignore_permissions=True)
		doc.project_name=doc.project_title
		frappe.db.set_value("Sales Order",doc.name,"project_name",doc.project_title)
		frappe.msgprint(_("Project '{0}' created successfully").format(project.project_name))


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
		stk_en.save(ignore_permissions=True)
		stk_en.submit()

def get_stock_item(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select distinct i.item_code from (select item_code from `tabBin`
		where actual_qty>0) b, `tabItem` i where i.item_code=b.item_code 
		and i.item_group='Tools' and i.is_stock_item=1""")


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
	if(project_data.tasks or project_data.status != "Open"):
		frappe.throw(_("Can not cancel sales Order as project in progress"))
		# project=frappe.db.get_value("Task",{"Project":project_data.name},"name")
	else:
		project_data.delete()

def get_sales_order(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select name from `tabSales Order` where (name='%s' or parent_sales_order='%s') and docstatus='1' """%(filters['sales_order'],filters['sales_order']))

def show_new_project(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select name from `tabProject` where status = 'Open' OR status = 'Completed'""")

# def reduce_buyback_amount(doc):
# 	if(doc.buyback_total):
# 		if(doc.total<doc.buyback_total):
# 			frappe.throw(_("Buyback Total Never be greater than Items Total"))
# 	if(doc.taxes):
# 		for d in doc.get('taxes'):
# 			if(d.is_buyback):
# 				# if(len(doc.get('taxes')) != ((doc.get('taxes').index(d))+1)):
# 				# 	frappe.throw(_("Always Insert Tax before Buyback row"))
# 				doc.taxes.remove(d)
# 		# if(doc.taxes):
# 		# 	if(doc.get('taxes')[0].charge_type == 'On Previous Row Amount' or doc.get('taxes')[0].charge_type == 'On Previous Row Total'):
# 		# 		frappe.throw(_("Always Insert Tax before Buyback row"))

# 		for index,d in enumerate(doc.get('taxes')):
# 			d.idx = index + 1
	
# 	if(doc.buyback_total): 			
# 		add_bb_to_tax(doc)

# 	# from erpnext.controllers.taxes_and_totals import calculate_taxes_and_totals
# 	# calculate_taxes_and_totals(doc)

# def add_bb_to_tax(doc):
# 	taxes=doc.append('taxes',{})
# 	taxes.charge_type =	"Actual"
# 	taxes.account_head = frappe.db.get_single_value('Osmosis Configurations', 'account_head')
# 	taxes.cost_center = frappe.db.get_single_value('Osmosis Configurations', 'cost_center')
# 	taxes.description = "Buyback Amount reduced"
# 	taxes.tax_amount = -doc.buyback_total
# 	taxes.is_buyback = "Yes"

@frappe.whitelist()
def check_customer(name):
	return frappe.db.get_value("Customer",{'lead_name':name},'lead_name')

@frappe.whitelist()
def make_customer(doc,customer_group):
	import json
	doc=json.loads(doc)
	cust = frappe.new_doc("Customer")
	lead_data = frappe.get_doc("Lead",doc.get('lead'))
	if lead_data.company_name:
		cust.customer_type = "Company"
		cust.customer_name = lead_data.company_name
	else:
		cust.customer_type = "Individual"
		cust.customer_name = lead_data.lead_name
	cust.area = lead_data.area
	cust.suburb = lead_data.suburb
	cust.website = lead_data.website
	cust.lead_name=doc.get('lead')
	cust.territory=doc.get('territory')
	cust.society_name=doc.get('society_name')
	cust.customer_group=customer_group
	cust.save(ignore_permissions=True)
	frappe.msgprint(_("Customer '{0}' created successfully").format(cust.customer_name))

def check_employee_timelog(doc,method):
	other_tm_logs=frappe.db.sql("select name from `tabTime Log` where employee=%s and docstatus=1",doc.employee,as_list=1)
	for tm_log in other_tm_logs:
		tm_log_doc=frappe.get_doc("Time Log",tm_log[0])
		if(tm_log_doc.task):
			tasks=frappe.get_doc("Task",tm_log_doc.task)
			if(tasks.status=="Open" or tasks.status=="Working"):
				from datetime import datetime
				from_tm=datetime.strptime(doc.from_time, '%Y-%m-%d %H:%M:%S')
				to_tm=datetime.strptime(doc.to_time, '%Y-%m-%d %H:%M:%S')
				if((tm_log_doc.from_time<=from_tm<=tm_log_doc.to_time) or (tm_log_doc.from_time<=to_tm<=tm_log_doc.to_time) or (from_tm<=tm_log_doc.from_time<=to_tm) or (from_tm<=tm_log_doc.to_time<=to_tm)):
					frappe.throw(_("{0} busy in {1} of {2} ").format(doc.employee,tm_log_doc.name,tm_log_doc.task))

@frappe.whitelist()
def Tools_required(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.tools_status="Tools Out"

	doclist = get_mapped_doc("Task", source_name, {
		"Task": {
			"doctype": "Tool Management",
			"field_map": {
				"project":"project",
				"task":"name",
				"sales_order":"sales_order"
			},
		},	
	}, target_doc,set_missing_values)

	return doclist

def create_item_price_list(doc, method):
	"""check for standard_buying and standard_selling"""
	if(doc.standard_buying):
		std="Standard Buying"
		find_items(doc,std)
	if(doc.standard_selling):
		std="Standard Selling"
		find_items(doc,std)

def find_items(doc,std):
	items=frappe.db.sql("""select name from `tabItem` where item_group=%s""", (doc.name), as_list=True)
	if(items):
		for item in items:
			item_price_list=frappe.db.sql("""select name from `tabItem Price` where item_code= %s and price_list= %s""", (item[0],std), as_list=True)
			if(item_price_list):
				price_list_rate=get_price_list_rate(std,doc)
				update_item_price_list(item_price_list,price_list_rate)
			else:
				price_list_rate=get_price_list_rate(std,doc)
				create_price_list_item(price_list_rate,std,item[0])

def update_item_price_list(item_price_list,price_list_rate):	
	for itm in item_price_list:
		frappe.db.sql("""update `tabItem Price` set price_list_rate=%s where name=%s""", (price_list_rate,itm[0]), as_list=True)

def create_price_list_item(price_list_rate,std,item):
	item_price = frappe.get_doc({
		"doctype": "Item Price",
		"price_list": std,
		"item_code": item,
		"currency": "INR",
		"price_list_rate": price_list_rate
	})
	item_price.insert()

def get_price_list_rate(std,doc):
	if(std=="Standard Buying"):
		return doc.buying_price
	if(std=="Standard Selling"):
		return doc.selling_price

def add_price_from_item(doc,method):
	item_group=doc.item_group
	item_group_doc=frappe.get_doc("Item Group",item_group)
	if(item_group_doc.standard_buying):
		std="Standard Buying"
		create_price_list_item(item_group_doc.buying_price,std,doc.name)
	if(item_group_doc.standard_selling):
		std="Standard Selling"
		create_price_list_item(item_group_doc.selling_price,std,doc.name)

def check_tasks_against_project(doc,method):
	if(doc.project_name):
		sales_order = doc.items[0].against_sales_order
		tasks=frappe.db.sql("select name from `tabTask` where project='%s' and sales_order='%s'"%(doc.project_name,sales_order),as_list=1,debug=1)
		if(tasks):
			for task in tasks:
				status=frappe.db.get_value("Task",{"name":task[0]},"status")
				if(status=="Open" or status=="Working"):
					frappe.throw(_("Task {0} is {1} Please Closed it.").format(task[0],status))

@frappe.whitelist()
def get_address(lead):
	return frappe.db.get_value("Address",{'lead':lead},'name')


def send_notifications(doc,method):
	if(doc.employee):
		msg = """Task {0} is assigned to you, In Time log {1} to {2},
		Please complete within Time
		""".format(doc.task,doc.from_time,doc.to_time)
		email=frappe.db.get_value("Employee",{"name":doc.employee},"user_id")
		frappe.sendmail(email, subject=_("Task allocation notification"), content=msg, bulk=True)

@frappe.whitelist()
def make_sales_order(source_name, target_doc=None):
	so=frappe.db.sql("""select name from `tabSales Order Item` where prevdoc_docname=%s and docstatus=1""",source_name)
	if not so:
		from erpnext.selling.doctype.quotation.quotation import _make_sales_order
		return _make_sales_order(source_name, target_doc)


@frappe.whitelist()
def item_query(doctype, txt, searchfield, start, page_len, filters):
	conditions = []
	return frappe.db.sql("""select tabItem.name,
		if(length(tabItem.item_name) > 40,
			concat(substr(tabItem.item_name, 1, 40), "..."), item_name) as item_name,
		if(length(tabItem.description) > 40, \
			concat(substr(tabItem.description, 1, 40), "..."), description) as decription,
		CASE tabItem.item_group
			when "Plumbing" then 
				concat("<b>DI-IN:</b> ",ifnull(tabItem.diameter_in_inches, 0), " <b>DI-MM:</b> ", ifnull(tabItem.diameter_in_millimeter,0)," <b>TH:</b> ", ifnull(tabItem.thickness,0)," <b>SI:</b> ", ifnull(tabItem.size,0))
			when "Pump" then
				concat("<b>DI-IN:</b> ",ifnull(tabItem.diameter_in_inches, 0), " <b>DI-MM:</b> ", ifnull(tabItem.diameter_in_millimeter,0)," <b>O-IN:</b> ", ifnull(tabItem.outlet_in_inches,0)," <b>O-MM:</b> ", ifnull(tabItem.outlet_in_millimeter,0)," <b>HP:</b> ", ifnull(tabItem.hp,0)," <b>PH:</b> ", ifnull(tabItem.phase,0)," <b>ST:</b> ", ifnull(tabItem.stage,0))
			when "Electrical" or "Unit Component" or "Auto Pump System" then
				concat("<b>RR:</b> ",ifnull(tabItem.relay_range, 0), " <b>SI:</b>",ifnull(tabItem.size,0))
			else
				concat(" ")	
		END as phase
		from tabItem
		where tabItem.docstatus < 2
			and ifnull(tabItem.has_variants, 0)=0
			and tabItem.disabled=0
			and (tabItem.end_of_life > %(today)s or ifnull(tabItem.end_of_life, '0000-00-00')='0000-00-00')
			and (tabItem.`{key}` LIKE %(txt)s
				or tabItem.item_name LIKE %(txt)s
				or tabItem.description LIKE %(txt)s
				or tabItem.variant_of_item LIKE %(txt)s
				or tabItem.diameter_in_inches LIKE %(txt)s
				or tabItem.outlet_in_inches LIKE %(txt)s
				or tabItem.stage LIKE %(txt)s
				or tabItem.thickness LIKE %(txt)s
				or tabItem.size LIKE %(txt)s
				or tabItem.diameter_in_millimeter LIKE %(txt)s
				or tabItem.outlet_in_millimeter LIKE %(txt)s
				or tabItem.phase LIKE %(txt)s
				or tabItem.hp LIKE %(txt)s
				or tabItem.relay_range LIKE %(txt)s)
			{fcond} {mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, item_name), locate(%(_txt)s, item_name), 99999),
			name, item_name
		limit %(start)s, %(page_len)s """.format(key=searchfield,
			fcond=get_filters_cond(doctype, filters, conditions),
			mcond=get_match_cond(doctype)),
			{
				"today": nowdate(),
				"txt": "%%%s%%" % txt,
				"_txt": txt.replace("%", ""),
				"start": start,
				"page_len": page_len
			})

@frappe.whitelist()
def employee_autoname(doc, method):
	doc.name = doc.employee_id

@frappe.whitelist()
def time_validation(doc, method):
	if not doc.time_out or not doc.time_in:
		frappe.throw("Enter Time In and Time Out")
	if doc.time_out < doc.time_in:
		frappe.throw("'Time Out' should be greater than 'Time In'")
	