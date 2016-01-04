
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
	d.amount=(d.qty || 0)*(d.rate||0);
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
		filters: [
					{
					'project':doc.project,
					},
					['Task','status','in','Open,Working']	
			]
	}
}

frappe.ui.form.on("Tool Management", "onload", function(frm){
	hide_in_out(frm);
	hide_in(frm);	
})

cur_frm.fields_dict.tools.grid.get_field("item_code").get_query = function(doc) {
	return {
		query: "osmosis.custom_methods.get_stock_item",
	}
}

frappe.ui.form.on("Tool Management", "tools_status", function(frm){
	if(frm.doc.docstatus!=1 && frm.doc.tools_status=="Tools In"){
		frm.doc.tools_status="";
		refresh_field("tools_status")
		frappe.msgprint("For Tools In, Tools must be out")
	}
	hide_in_out(frm);
	hide_in(frm);
})
function hide_in(frm){
	if(frm.doc.docstatus==1 && frm.doc.tools_status=="Tools In"){
		frm.set_df_property("in_time", "reqd", 1);
		frm.set_df_property("in_time", "read_only", 0);
	}
}

function hide_in_out(frm){
	if(!frm.doc.tools_status){
		frm.set_df_property("in_time", "read_only", 1);
		frm.set_df_property("out_time", "read_only", 1);
	}
	if(frm.doc.tools_status=="Tools Out"){
		frm.set_df_property("in_time", "read_only", 1)
		frm.set_df_property("out_time", "read_only", 0);
		frm.set_df_property("out_time", "reqd", 1);
	}
}

frappe.ui.form.on("Tool Management", "in_time", function(frm){
	if(frm.doc.in_time < frm.doc.out_time){
		// frm.doc.in_time="";
		// refresh_field("in_time")
		frappe.msgprint("In time must be greater than out time")
	}
})

frappe.ui.form.on("Tools", "item_code", function(frm,cdt,cdn){
	d=locals[cdt][cdn];
	frappe.call({
		method: "osmosis.osmosis.doctype.tool_management.tool_management.get_price_list_rate",
		args: {
			"item_code": d.item_code,
		},
		callback: function(r) {
			if(r.message){
				d.rate=r.message
				refresh_field("tools")
			}
		}
	});
})