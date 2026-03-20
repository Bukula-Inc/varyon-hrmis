import { API_CONFIG } from "../../../connection/config.js";
;

export const on_print_configuration_load = (params) =>{
    lite.connect.get_doc("Model",params.value).then(r=>{
        if (r?.status === API_CONFIG.status_codes.ok){
            const doc_exclusives = [
                "created_on", "creation_time", "docstatus", 
                "owner", "modified_by","status","id","utils",
                "doc_exclusives","idx","disabled","doctype",
                "owner_name","modifier_name","last_modified",
            ]
            const data = r.data
            const field_defs = data.field_definitions
            if(!lite.utils.is_empty_object(field_defs)){
                let fc = []
                $.each(lite.utils.get_object_keys(field_defs),(_,f)=>{
                    if(!doc_exclusives.includes(f))
                        fc.push({
                            field_name:f,
                            field_type:field_defs[f].fieldtype,
                            columns:1,
                            include_in_print:1,
                            linked_model:field_defs[f]?.related_model,
                        })
                })
                if(data.linked_tables && !lite.utils.is_empty_array(data.linked_tables)){
                    $.each(data.linked_tables,(_,lt)=>{
                        fc.push({
                            field_name:lt.field_name,
                            field_type:"table",
                            columns:1,
                            include_in_print:1,
                            linked_model:lt.config.name
                        })
                    })
                }
                params.controller.populate_child_table("configuration_fields",fc)
            }
        }
    })
}