
//set current date in date
frappe.ui.form.on("Lead","onload",function(frm){
	frm.doc.date= frm.doc.date || frappe.datetime.nowdate();
	refresh_field("date")
})

//fetch fields from lead on creating customer from lead
frappe.ui.form.on("Customer","onload",function(frm){
	frm.add_fetch('lead_name', 'area', 'area');
	frm.add_fetch('lead_name', 'society_name', 'society_name');
	frm.add_fetch('lead_name', 'suburb', 'suburb');
})

//fetch fields from customer on creating quotation from customer
frappe.ui.form.on("Quotation","onload",function(frm){
	frm.add_fetch('customer', 'society_name', 'society_name');
})

//button on sales order for extra sales order
frappe.ui.form.on("Sales Order", "refresh", function(frm) {
	if (frm.doc.docstatus==1 && frm.doc.status != 'Stopped') {																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																												
		cur_frm.add_custom_button(__('Extra Sales Order'), make_extra_sales_order);
	}
});

make_extra_sales_order = function(btn) {
   var eso = frappe.model.make_new_doc_and_get_name('Sales Order');
   eso = locals['Sales Order'][eso];
   eso.project_title = cur_frm.doc.project_title;
   eso.customer = cur_frm.doc.customer;
   eso.parent_sales_order = cur_frm.doc.name;
   eso.is_extra_sales_order=true;

   loaddoc('Sales Order', eso.name);
}

//added for buy back amount changes reflect on js
frappe.ui.form.on("Buyback Item", "rate", function(frm,cdt,cdn) {
	refresh_buyback_item(frm);
	refresh_buyback_total(frm);
});

frappe.ui.form.on("Buyback Item", "quantity", function(frm,cdt,cdn) {
	refresh_buyback_item(frm,cdt,cdn);
	refresh_buyback_total(frm,cdt,cdn);
});

frappe.ui.form.on("Buyback Item", "buyback_item_remove", function(frm) {
	refresh_buyback_total(frm);
});

function refresh_buyback_item(frm,cdt,cdn){
	d=locals[cdt][cdn]
	d.amount=parseFloat(d.rate) * parseFloat(d.quantity);
	refresh_field("buyback_item");
}

function refresh_buyback_total(frm){
	frm.doc.buyback_total = 0.0;
	$.each(frm.doc["buyback_item"] || [], function(i, buyback_item) {
		frm.doc.buyback_total += buyback_item.amount;
	});
	refresh_field("buyback_total")
}


frappe.ui.form.on("Quotation","onload" ,function(frm){
	cur_frm.fields_dict.buyback_item.grid.get_field("item_code").get_query = function(doc) {
		return {
			filters: {
				"item_group":"Buyback"
			}
		}	
	}
})
frappe.ui.form.on("Purchase Order","onload" ,function(frm){
	cur_frm.fields_dict.project.get_query = function(doc) {
		return {
			filters: {
				"status":"Open" 
			}
		}
	}
})
frappe.ui.form.on("Issue","onload" ,function(frm){
	cur_frm.fields_dict.project.get_query = function(doc) {
		return {
			query: "osmosis.custom_methods.show_new_project"
		}
	}
})