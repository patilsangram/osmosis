frappe.ui.form.on("Lead","onload",function(frm){
	console.log("hiii")
	frm.date=frappe.datetime.get_today();
	refresh_field("date")
})