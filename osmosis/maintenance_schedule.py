from __future__ import unicode_literals
import frappe

from frappe.utils import add_days, getdate, cint, cstr

from frappe import throw, _
from frappe.utils import add_days, getdate, formatdate, get_first_day, date_diff, today, add_years


def auto_status_update_ms(doc, method):
	new = add_years(doc.installation_date, doc.guarantee_period)
	new = add_days(new, days=-1)
	doc.amc_guarantee_valid_upto_date = new

	if doc.transaction_date:
		doc.amc_status = "Untraceable"
	elif date_diff(doc.transaction_date,doc.installation_date)<=365*doc.contract_period:
		doc.amc_status = "N/A"
	elif doc.amc_guarantee_valid_upto_date>doc.transaction_date:
		doc.amc_status = "Guarantee"
	else:
		doc.amc_status="Expired"
	
	if doc.amc_start_month:
		guarntee=add_years(doc.amc_start_month,doc.contract_period)
		guarntee = add_days(guarntee, days=-1)
		doc.amc_guarantee_valid_upto_date=guarntee
		doc.amc_status = "AMC"