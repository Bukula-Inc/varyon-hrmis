def natural_list_dicts (obj: dict) -> list:

    result_list = []
    for item_name, inner_dict in obj.items():
        result_list.append ({
            "item_name": item_name,
            "in_qty": int (inner_dict["in_qty_restock"]),
            "incoming_value": float (inner_dict["incoming_value_restock"]),
            "out_qty": int (inner_dict["out_qty_sold"]),
            "out_value": int (inner_dict["out_value_sold"]),
            "current_qty": int (inner_dict['in_qty_restock']) - int (inner_dict['out_qty_sold']),
            "current_value": float (inner_dict["incoming_value_restock"]) - float (inner_dict["out_value_sold"]),
            "remaining_qty": int (inner_dict['in_qty_restock']) - int (inner_dict['out_qty_sold']),
            "remaining_value": float (inner_dict["incoming_value_restock"]) - float (inner_dict["out_value_sold"])
        })    
    return result_list