cur_frm.fields_dict.sales_order.get_query = function(doc){
	return {
		filters: {"docstatus":1,
					"is_extra_sales_order":0,
					"project_title":doc.project
				}
		}
}



