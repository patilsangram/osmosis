
cur_frm.add_fetch('item_code', 'item_name', 'item_name');
cur_frm.add_fetch('item_code', 'description', 'description');
//cur_frm.add_fetch('item_code', 'price_list_rate', 'rate');
frappe.ui.form.on("Tools", "rate", function(frm,cdt,cdn){
	d=locals[cdt][cdn];
	cal_amount(d)
})

frappe.ui.form.on("Tools", "qty", function(frm,cdt,cdn){
	d=locals[cdt][cdn];
	cal_amount(d)	
})

function cal_amount(d){
	d.amount=d.qty*d.rate;
	refresh_field("tools")
}

frappe.ui.form.on("Tool Management", "onload", function(frm){
	frm.doc.posting_date=frm.doc.posting_date || get_today();
})


cur_frm.fields_dict.sales_order.get_query = function(doc){
	return {
		filters: {"docstatus":1,
					"project_title":doc.project,
				}
		}
}

cur_frm.fields_dict.task.get_query = function(doc){
	return {
		filters: {
					"project":doc.project,
				}
		}
}

frappe.ui.form.on("Tool Management", "tools_status", function(frm){
	if(frm.doc.tools_status=="Tools Out"){
		frm.set_df_property("in_time", "read_only", 0);
		frm.set_df_property("out_time", "reqd", 1);
		frm.set_df_property("in_time", "read_only", 1);
	}
	else
		if(frm.doc.tools_status=="Tools In"){
		frm.set_df_property("in_time", "read_only", 0);
		frm.set_df_property("in_time", "reqd", 1);
		frm.set_df_property("out_time", "read_only", 1);
	}
})

frappe.ui.form.on("Tool Management", "in_time", function(frm){

	if(frm.doc.in_time<frm.doc.out_time){
		frm.doc.in_time="";
		refresh_field("in_time")
		frappe.msgprint("In time never be greater than out time")
	}
})