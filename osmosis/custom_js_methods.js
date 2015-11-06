
//set current date in date
frappe.ui.form.on("Lead","onload",function(frm){
	frm.doc.date= frm.doc.date || frappe.datetime.nowdate();
	refresh_field("date")
})

//fetch fields from lead on creating customer from lead
frappe.ui.form.on("Customer","lead_name",function(frm){
	frm.add_fetch('lead_name', 'area', 'area');
	frm.add_fetch('lead_name', 'society_name', 'society_name');
	frm.add_fetch('lead_name', 'suburb', 'suburb');
})

//fetch fields from customer on creating quotation from customer
frappe.ui.form.on("Quotation","customer",function(frm){
	frm.add_fetch('lead_name', 'society_name', 'society_name');
})

//add custom button on sales order
frappe.ui.form.on("Sales Order","refresh",function(frm){
	if(frm.doc.docstatus != 'Stopped') {
		cur_frm.add_custom_button(__('Extra Sales Order'), cur_frm.cscript['extra_sales_order']);
	}
})

cur_frm.cscript['extra_sales_order'] = function(doc) {
	frappe.model.open_mapped_doc({
		method: "osmosis.custom_methods.make_extra_sales_order",
		frm: cur_frm
	})
}

//added for buy back amount changes reflect on js
frappe.ui.form.on(cur_frm.doctype,"refresh",function(frm){
	frappe.ui.form.on(cur_frm.doctype, "buy_back_amount", function(frm) {
		refresh_grand_total(frm)
	})
})


function refresh_grand_total(frm){
	var distributed_amount = 0.0;
			var tax_count = frm.doc["taxes"] ? frm.doc["taxes"].length : 0;
			frm.doc.grand_total = (flt(tax_count ? frm.doc["taxes"][tax_count - 1].total : frm.doc.net_total) - frm.doc.buy_back_amount);
			frm.doc.base_grand_total = ((frm.doc.total_taxes_and_charges) ?
				flt(frm.doc.grand_total * frm.doc.conversion_rate) : frm.doc.base_net_total)-frm.doc.buy_back_amount;
			frappe.model.round_floats_in(frm.doc, ["grand_total", "base_grand_total"]);

			frm.doc.rounded_total = Math.round(frm.doc.grand_total);
			frm.doc.base_rounded_total = Math.round(frm.doc.base_grand_total);
			frm.doc.base_in_words = frm.doc.in_words = "";
	
		field=["grand_total","base_grand_total","rounded_total","in_words"];
		refresh_field(field);
}


