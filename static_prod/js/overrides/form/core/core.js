// WORKFLOW OVERRIDE FUNCTIONS
export const switch_company = async(params) =>{
    const quick_modal = await lite.modals.quick_form("core", "switch company",{text:"Switch", fun: async (values,setup)=>{
        const loader_id = lite.alerts.loading_toast({
            title: "Switching", 
            message:`Please wait while we switch the company.`
        })
        const {status, data, error_message} = await lite.connect.core("switch_company", values)
        lite.alerts.destroy_toast(loader_id)
        if(status === lite.status_codes.ok){
            lite.modals.close_modal(quick_modal.modal_id)
            lite.session.clear_cookies_for_domain()
            lite.connect.set_user_cookie(data.token)
            lite.alerts.toast({
                toast_type:lite.status_codes.ok,
                title:"Process Concluded",
                message:"Company Switched Successfully! \n Refreshing the page now"
            })
            setTimeout(() => { location.replace(data.url) }, 1000);
        }
    }})
}

// CURRENCY AND EXCHANGE RATE
export const on_exchange_rate_change = async (params)=>{
    const controller = params.controller
    const rate = lite.utils.string_to_float(params?.value||0)
    if(rate && rate > 0){
        const inverse = lite.utils.fixed_decimals(1/rate,4)
        params.controller.set_form_value(controller.get_form_field("inverse"),inverse)
    }
    else{
        params.controller.set_form_value(controller.get_form_field("rate"),"0.00")
    }
}








// DATA IMPORTATION
export const on_file_change = (params) =>{
    const controller = params.controller
    let size = 0, ext = '', name = '', type = ''
    if(params?.files && params?.files?.length > 0){
        size = params?.files[0]?.file_size
        name = params?.files[0]?.file_name
        type = params?.files[0]?.file_type
        size = params?.files[0]?.file_size
    }
    controller.set_form_value(controller.get_form_field("file_name"),name)
    controller.set_form_value(controller.get_form_field("file_extension"),ext)
    controller.set_form_value(controller.get_form_field("file_size"),size,`${lite.utils.thousand_separator(size,2)} Bytes`)

}



export const start_importation = async (params) =>{
    const controller = params.form_controller
    const loader_id = lite.alerts.loading_toast({
        title: `Importing Data`, 
        message:"Please wait while data importation is underway."
    })
    const import_data = await lite.connect.x_post("start_data_importation",{"doc":[params.values.id]})
    lite.alerts.destroy_toast(loader_id)
    if(import_data.status === lite.status_codes.ok){
        lite.alerts.toast({
            toast_type: import_data.status,
            title: "Importation Completed",
            message: "Importation Completed!",
            timer: 10000
        })
        controller.init_form()
    }
}

export const download_template = async (params) =>{
    const controller = params.form_controller
    const values = params.values
    if(!values.model){
        lite.alerts.toast({
            toast_type: lite.status_codes.forbidden,
            title: "Missing Source Document Type",
            message: "Please select what type of importation you are doing!",
            timer: 4000
        })
    }
    else{
        const model = await lite.connect.get_doc("Model", values.model)
        if(model.status === lite.status_codes.ok){
            const data = model.data?.field_definitions
            let keys = ""
            $.each(lite.utils.get_object_keys(data),(_,k)=>{
                if(!k["null"] && !["id","created_on","creation_time","last_modified","idx","doctype","modified_by","owner","docstatus","status","disabled"].includes(k))
                    keys += `${lite.utils.capitalize(lite.utils.replace_chars(k,"_"," "))},`
            })
            keys = `${keys.slice(0, -1)}\n`

            const blob = new Blob([keys], { type: "text/csv;charset=utf-8;" });
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", `${lite.utils.capitalize(lite.utils.replace_chars(values.model,"_"," "))}.csv`);
            link.style.visibility = "hidden";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}

export const extend_data_importation_fields = async (params, fields) =>{
    if(!lite.is_new_form){
        const doc = await lite.connect.get_doc("Data_Importation",lite.utils.get_url_parameters("doc"))
        if(doc.status === lite.status_codes.ok){
            const file_content = doc.data?.file_content
            if(lite.utils.array_has_data(file_content)){
                const row = lite.utils.get_object_keys(file_content[0])
                $.each(fields,(_,f)=>{
                    if(f.fieldname === "file_content"){
                        f.fields = [{
                            "id": "status",
                            "fieldlabel": "Status",
                            "fieldname": "status",
                            "fieldtype": "read-only",
                            "columns": 6,
                            "placeholder": "",
                            "required": false,
                            "hidden": false,
                            classnames:"text-default font-semibold"
                        }]
                        $.each(row,(_,i)=>{
                            if(_ < 70 && i != "status"){
                                f.fields.push({
                                    "id": i,
                                    "fieldlabel": lite.utils.capitalize(lite.utils.replace_chars(i,"_"," ")),
                                    "fieldname": i,
                                    "fieldtype": "text",
                                    "columns": i?.toLowerCase() === "name" || i?.toLowerCase() === "error" ? 8 : 4,
                                    "placeholder": "",
                                    "required": false,
                                    "hidden": false,
                                })
                            }
                        })
                    }
                })
                return fields
            }
        }
    }
}


export const on_print_configuration_load = (params) =>{
    lite.connect.get_doc("Model",params.value).then(r=>{
        if (r?.status === lite.status_codes.ok){
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
                            columns: 1,
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




// user
export const on_user_loaded = (params) =>{
    const dp = lite.form_data?.dp || "/media/defaults/avatas/dp.jpeg"
    $(".user-dp").attr("src", dp)
}

export const on_user_email_changed = (params) =>{
    const controller = params.controller
    controller.set_form_value(controller.get_form_field("name"), params.value,null, false)
}

export const on_test_email_config  = async (params)=>{
    const test = await lite.connect.x_post("test_email_config")
}



// SHARE MANAGEMENT
export const calculate_shares  = async (params)=>{
    const {controller} = params
    const values =  controller.get_form_data().values
    const total_shares = lite.utils.string_to_float(values.total_shares)
    
    let 
        total_value = 0,
        total_owned_shares = 0, 
        total_owned_value = 0, 
        total_unowned_shares = total_shares,
        total_unowned_value = 0

    if(total_shares && values.share_type){
        const share_type = await lite.connect.get_doc("Share_Type", values.share_type)
        if(share_type.status === lite.status_codes.ok){
            const share_type_data = share_type.data
            const amount = lite.utils.string_to_float(share_type_data?.price_per_share)
            const currency = lite.utils.string_to_float(share_type_data?.currency)
            total_value = total_shares * amount
            total_unowned_value = total_value
            controller.set_form_value(controller.get_form_field("total_value"),total_value)

            $.each(values.shareholders,(i,sh)=>{
                const total_shareholder_shares = lite.utils.string_to_float(sh.shareholder_total_shares)
                const shareholder_percentage = (total_shareholder_shares/total_shares) * 100
                const shareholder_Value = total_shareholder_shares * amount
                const share_perc = controller.get_form_table_field("shareholders",sh.row_id,"shareholder_share_percentage")
                const share_val = controller.get_form_table_field("shareholders",sh.row_id,"shareholder_share_value")
                controller.set_form_table_value("shareholders",sh.row_id,share_perc,shareholder_percentage, `${lite.utils.thousand_separator(shareholder_percentage,2)}%`,false)
                controller.set_form_table_value("shareholders",sh.row_id,share_val,shareholder_Value, lite.utils.currency(shareholder_Value,lite.currency_decimals,currency),false)
                
                total_owned_shares += total_shareholder_shares
                total_owned_value += shareholder_Value
                total_unowned_shares -= total_shareholder_shares
                total_unowned_value -= total_owned_value
                
            })
        }
        controller.set_form_value(controller.get_form_field("total_shareholders"),values.shareholders?.length)
        controller.set_form_value(controller.get_form_field("total_owned_shares"), total_owned_shares)
        controller.set_form_value(controller.get_form_field("total_owned_value"), total_owned_value)
        controller.set_form_value(controller.get_form_field("total_unowned_shares"), total_unowned_shares)
        controller.set_form_value(controller.get_form_field("total_unowned_value"), total_unowned_value)
    }
}


export const update_form_customization = async(params)=>{
    const {status, data, error_message} = await lite.connect.get_doc("Model", params.value)
    // if(status === lite.status_codes.ok){
    //     const fields = data.fields
    //     const normal_fields = lite.utils.get_object_keys(fields.normal_fields),
    //           foreign_key_fields = lite.utils.get_object_keys(fields.foreign_key_fields) 
    //     const all_cols = [...normal_fields, ...foreign_key_fields]?.filter(item=> !["id","created_on","creation_time","last_modified","docstatus","idx","disabled","doctype","company_id", "owner", "modified_by", "status"].includes(item))
    //     let field_rows = []
    //     $.each(all_cols,(_,field)=> {field_rows.push({ field_name:field, make_mandatory: 0, hide_field: 0, display_on: "" })})
    //     params?.controller?.populate_child_table("field_config",field_rows,true)
    // }
}