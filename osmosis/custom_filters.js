cur_frm.fields_dict.sales_order.get_query = function(){
	return {
		filters: {"docstatus":1}
		}
}

cur_frm.set_df_property("sales_order", "reqd", 1);


