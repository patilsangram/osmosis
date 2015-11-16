from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, flt, fmt_money, formatdate
from frappe import msgprint, _, scrub


def make_stock_entry(sales_order, method):
	st = frappe.new_doc('Stock Entry')
	st.purpose = 'Material Receipt',
	st.posting_date = doc.posting_date
	print"hello"
	for d in sales_order.get("items"):
		d.item_code = doc.item_code
	print"hello after"