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

	if(doc.doctype=="Project"){
		cur_frm.fields_dict.tasks.grid.get_field("against_sales_order").get_query = function(doc) {
			if(doc.sales_order){
				return {
					query: "osmosis.custom_methods.get_sales_order",
					filters:{
						'sales_order':doc.sales_order,
					}
				}
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

cur_frm.cscript.custom_refresh = function(doc, cdt, cdn) {
	if(doc.doctype=="Task" && !doc.__islocal){	
		cur_frm.add_custom_button(__('Add Tools Required'), Tools_required);
	}
}
Tools_required=function(){
	frappe.model.open_mapped_doc({
		method: "osmosis.custom_methods.Tools_required",
		frm: cur_frm
	})
}

frappe.ui.form.on("Task","refresh",function(frm){
cur_frm.fields_dict['helper_name'].get_query = function(doc) {
	return {
		query:"osmosis.custom_methods.get_info_if_employee_help"
	}
}
cur_frm.fields_dict['technician_name'].get_query = function(doc) {
	return {
		query:"osmosis.custom_methods.get_info_if_employee_tech"
	}
}
cur_frm.fields_dict['supervisor_name'].get_query = function(doc) {
	return {
		query:"osmosis.custom_methods.get_info_if_employee_sup"
	}
}
})
