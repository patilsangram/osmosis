from __future__ import unicode_literals
import frappe

from frappe.utils import add_days, getdate, cint, cstr

from frappe import throw, _
from frappe.utils import add_days, getdate, formatdate, get_first_day, date_diff, today, add_years


def auto_status_update_ms(doc, method):
	new = add_years(doc.installation_date, doc.contract_period)
	doc.amc_guarantee_valid_upto_date=new
	if doc.transaction_date >= doc.amc_guarantee_valid_upto_date:
		doc.amc_status = "Expired"