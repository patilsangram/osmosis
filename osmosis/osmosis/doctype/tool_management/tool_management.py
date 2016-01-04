# -*- coding: utf-8 -*-
# Copyright (c) 2015, osmosis and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ToolManagement(Document):
	def on_update_after_submit(self):
		if(self.in_time < self.out_time):
			frappe.throw("In time must be greater than out time")

@frappe.whitelist()
def get_price_list_rate(item_code):
	return frappe.db.get_value("Item Price",{"item_code":item_code,"price_list":"Standard Selling"},"price_list_rate") or 0