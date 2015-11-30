
//set current date in date
frappe.ui.form.on("Lead","onload",function(frm){
	frm.doc.date= frm.doc.date || frappe.datetime.nowdate();
	refresh_field("date")
})

frappe.ui.form.on("Lead","contact_date",function(frm){
	check_date(frm.doc);
})

//on opportunity transaction date
frappe.ui.form.on("Opportunity","contact_date",function(frm){
	check_date(frm.doc);
})

function check_date(doc){
	if(doc.contact_date<frappe.datetime.get_datetime_as_string()){
		doc.contact_date=frappe.datetime.get_datetime_as_string();
		refresh_field('contact_date');
		frappe.msgprint("Next Contact Date Never be Past Date");
	}
}

//fetch fields from lead on creating customer from lead
frappe.ui.form.on("Customer","onload",function(frm){
	frm.add_fetch('lead_name', 'area', 'area');
	frm.add_fetch('lead_name', 'society_name', 'society_name');
	frm.add_fetch('lead_name', 'suburb', 'suburb');
})

//fetch fields from customer on creating quotation from customer
frappe.ui.form.on("Quotation","onload",function(frm){
	frm.add_fetch('Customer', 'society_name', 'society_name');
	frm.add_fetch('lead', 'society_name', 'society_name');
})

frappe.ui.form.on("Opportunity","onload",function(frm){
	frm.add_fetch('customer', 'society_name', 'society_name');
	frm.add_fetch('lead', 'society_name', 'society_name');
})

//button on sales order for extra sales order
cur_frm.cscript.custom_refresh = function(doc, cdt, cdn) {
	if(doc.doctype=="Sales Order" && !doc.is_extra_sales_order){	
		if (doc.docstatus==1 && doc.status != 'Stopped'){ 																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																												
				cur_frm.add_custom_button(__('Extra Sales Order'), make_extra_sales_order);
		}
	}

	if(doc.doctype=='Quotation' && doc.docstatus==1 && doc.quotation_to=='Lead'){
		// console.log(doc.lead)
		frappe.call({
			method: "osmosis.custom_methods.check_customer",
			args: {
				"name": doc.lead,
			},
			callback: function(r) {
				console.log(r.message)
				if(!r.message){
					cur_frm.add_custom_button(__('Create Customer'), new_customer);
				}
			}
		})
	}
}

new_customer=function(){
	frappe.model.open_mapped_doc({
		method: "osmosis.custom_methods.make_customer",
		frm: cur_frm
	})
}

make_extra_sales_order = function() {
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
	refresh_buyback_item(frm,cdt,cdn);
	refresh_buyback_total(frm,cdt,cdn);
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


frappe.ui.form.on("Sales Taxes and Charges", "charge_type", function(frm, cdt, cdn) {
	d=locals[cdt][cdn];
	tax_len=frm.doc.taxes.length;
	if(tax_len > 1 && frm.doc.taxes[tax_len-2].is_buyback=='Yes'){
		var item = frappe.get_doc(cdt, cdn);
		cur_frm.fields_dict["taxes"].grid.grid_rows[item.idx - 1].remove();
		frappe.msgprint("Insert Tax Above the Buyback row")
	}
	 
	if(frm.doc.taxes[0].charge_type=='On Previous Row Amount' || frm.doc.taxes[0].charge_type=='On Previous Row Total'){
		d.charge_type='';
		refresh_field("taxes")
		frappe.msgprint("Charge Type On Previous Row Amount or On Previous Row Total never be first row");
	}
})


cur_frm.cscript.custom_onload = function(doc, cdt, cdn) {
	if(doc.doctype=="Quotation"||doc.doctype=="Sales Order"||doc.doctype=="Delivery Note"||doc.doctype=="Sales Invoice"){	
		cur_frm.fields_dict.items.grid.get_field("item_code").get_query = function(doc) {
			return {
				filters: [
					['Item','item_group','!=','Tools']
				]
			}	
		}
	}
}

