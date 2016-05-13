@frappe.whitelist()
def price_list_rates(item_code):
	rates=frappe.db.get_all("Item Price",filters={"buying":1,"item_code":item_code},fields=["price_list","price_list_rate"])
	for rate in rates:
		print rate["price_list"]
		print rate["price_list_rate"]