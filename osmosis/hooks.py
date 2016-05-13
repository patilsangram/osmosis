# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "osmosis"
app_title = "osmosis"
app_publisher = "osmosis"
app_description = "osmosis"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "makarand.b@indictranstech.com"
app_version = "0.0.1"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/css/osmosis.min.css"
app_include_js = "/assets/js/osmosis.min.js"

# include js, css files in header of web template
# web_include_css = "/assets/osmosis/css/osmosis.css"
# web_include_js = "/assets/osmosis/js/osmosis.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "osmosis.install.before_install"
# after_install = "osmosis.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "osmosis.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
	# "all": [
	# 	# "osmosis.tasks.all"
	# 	"osmosis.maintenance_schedule.auto_status_update_ms"
	# ],
# }
# 	"daily": [
# 		"osmosis.tasks.daily"
		 
# 	],
# 	"hourly": [
# 		"osmosis.tasks.hourly"
# 	],
# 	"weekly": [
# 		"osmosis.tasks.weekly"
# 	]
# 	"monthly": [
# 		"osmosis.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "osmosis.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.selling.doctype.quotation.quotation.make_sales_order": "osmosis.custom_methods.make_sales_order"
}

doc_events = {
	"Sales Order": {
		# "validate": ["osmosis.custom_methods.reduce_buyback_amount"],
		"on_submit": ["osmosis.custom_methods.create_project","osmosis.custom_methods.make_stock_entry"],
		"on_cancel": ["osmosis.custom_methods.on_cancel_sales_order"],
		# "validate":["osmosis.custom_methods.so_autoname"],
	},
	"Tool Management": {
		"on_submit": "osmosis.custom_methods.new_stock_entry",
		"on_update_after_submit":"osmosis.custom_methods.new_stock_entry",
	},
	"Time Log":{
		"validate": ["osmosis.custom_methods.check_employee_timelog"],
		# "on_submit": ["osmosis.custom_methods.send_notifications"],
	},
	"Delivery Note":{
		"on_submit": ["osmosis.custom_methods.check_tasks_against_project"],
	},
	"Employee": {
		"autoname": "osmosis.custom_methods.employee_autoname"
	},
	"Attendance": {
		"validate": "osmosis.custom_methods.time_validation"
	},
	"Maintenance Schedule": {
		"validate": "osmosis.maintenance_schedule.auto_status_update_ms"
	}

	# "Item":{
	# 	"on_update": ["osmosis.custom_methods.add_price_from_item"],
	# },
	# "Item Group":{
	# 	"validate": ["osmosis.custom_methods.create_item_price_list"],
	# },
	# "Quotation": {
	# 	"validate": ["osmosis.custom_methods.reduce_buyback_amount"],
	# },
	# "User": {
	# 	"validate": "erpnext.hr.doctype.employee.employee.validate_employee_role",
	# 	"on_update": "erpnext.hr.doctype.employee.employee.update_user_permissions"
	# },
	# "Sales Taxes and Charges Template": {
	# 	"on_update": "erpnext.shopping_cart.doctype.shopping_cart_settings.shopping_cart_settings.validate_cart_settings"
	# },
	# "Price List": {
	# 	"on_update": "erpnext.shopping_cart.doctype.shopping_cart_settings.shopping_cart_settings.validate_cart_settings"
	# },
 }

standard_queries = {
	"Item": "osmosis.custom_methods.item_query"
}

fixtures = ["Custom Field","Property Setter","Item Group", "Print Format"]
