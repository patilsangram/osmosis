from __future__ import unicode_literals
import frappe

from frappe.utils import add_days, getdate, cint, cstr

from frappe import throw, _
from frappe.utils import add_days, getdate, formatdate, get_first_day, date_diff


def auto_status_update_ms(doc, method):
	if (date_diff(doc.transaction_date,doc.installation_date)) <= 365*doc.contract_period:
		if doc.transaction_date < doc.amc_guarantee_valid_upto_date:
			frappe.db.set_value("Maintenance Schedule", doc.name, "amc_status", "Expired")