cur_frm.fields_dict.sales_order.get_query = function(doc){
	return {
		filters: {"docstatus":1,
					"is_extra_sales_order":0,
					"project_title":doc.project
				}
		}
}

cur_frm.cscript.custom_onload = function(doc, cdt, cdn) {
	if(doc.doctype=="Task"){
		cur_frm.fields_dict.depends_on.grid.get_field("task").get_query = function(doc) {
			if(doc.project){
				return {
					filters: [
						{
						'project':doc.project,
						},
						['Task','name','!=',doc.name]
					]
				}
			}
			else
			{
				frappe.msgprint("Please select Project First")
			}	
		}
	}
}

frappe.ui.form.on("Project Task","start_date",function(frm,cdt,cdn){
	d=locals[cdt][cdn];
	if(d.start_date<frm.doc.expected_start_date){
		d.start_date = '';
		refresh_field('tasks');
		frappe.msgprint("Task start date never be less than project expected start date");
	}
})
