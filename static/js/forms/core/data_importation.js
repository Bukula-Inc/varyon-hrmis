import { start_importation, download_template } from "../../overrides/form/core/core.js";

export default {
    setup: {
        allow_submit: true,
        allow_delete:false,
        allow_cancel:true,
        new_form_id: 'form',
        info_form_id: 'info',
        title: "Data Importation",
        layout_columns: 4,
        model: "Data_Importation"
    },
    form_actions: [
        { title: "Start Data Importation", icon: "partner_reports", icon_color: "green", action: start_importation, for_docstatus: [1,0] }
    ],
    form_buttons:[
        {title: "Download Template", icon: "download", icon_color: "orange", action: download_template, for_docstatus: [0], classname: "border-orange-500"}
    ],
    fields: [
        
        {
            id: "model",
            fieldlabel: "Importing For",
            fieldname: "model",
            fieldtype: "link",
            model:"Model",
            columns: 1,
            placeholder: "Select Model Name",
            required: true,
            hidden: false,
        },
        {
            id: "file",
            fieldlabel: "File",
            fieldname: "file_url",
            fieldtype: "file",
            columns: 1,
            placeholder: "Select Excel/CSV File",
            required: true,
            hidden: false,
            accept:["xcls","csv"],
            maxsize: 983293
        },
        {
            id: "file-name",
            fieldlabel: "Initial File Name",
            fieldname: "file_name",
            fieldtype: "read-only",
            columns: 1,
            placeholder: "Enter File Name",
            required: true,
            hidden: true,
        },
        {
            id: "file-size",
            fieldlabel: "File Size",
            fieldname: "file_size",
            fieldtype: "read-only",
            columns: 1,
            placeholder: "Enter File Size",
            required: false,
            hidden: false,
            default:"0.00 Bytes"
        },
        {
            id: "initial-status",
            fieldlabel: "Initial Status",
            fieldname: "initial_status",
            fieldtype: "link",
            model: "Doc_Status",
            columns: 1,
            placeholder: "Select Initial Status",
            required: true,
            hidden: false,
            default:"Active"
        },
        {
            id: "file-extension",
            fieldlabel: "File Extension",
            fieldname: "file_extension",
            fieldtype: "read-only",
            columns: 1,
            placeholder: "",
            required: false,
            hidden: false,
        },
        {
            id: "total-rows",
            fieldlabel: "Total Rows",
            fieldname: "total_rows",
            fieldtype: "read-only",
            columns: 1,
            placeholder: "Enter Naming Series Format",
            required: false,
            hidden: false,
            default:"0",
            is_figure:true,
            default:"0"
        },
        {
            id: "total-successful",
            fieldlabel: "Total Successful",
            fieldname: "total_successful",
            fieldtype: "read-only",
            columns: 1,
            placeholder: "",
            required: false,
            hidden: false,
            default:"0",
            is_figure:true,
            default:"0"
        },
        {
            id: "total-failed",
            fieldlabel: "Total Failed",
            fieldname: "total_failed",
            fieldtype: "read-only",
            columns: 1,
            placeholder: "",
            required: false,
            hidden: false,
            default:"0",
            is_figure:true,
            default:"0"
        },
        {
            id: "has-extracted-rows",
            fieldlabel: "Has Extracted Rows",
            fieldname: "has_extracted_rows",
            fieldtype: "check",
            columns: 1,
            placeholder: "Has Extracted Rows",
            required: false,
            hidden: false,
            default:"0",
            is_figure:false,
            default:1
        },



        {
            id: "file-content",
            fieldlabel: "File Content",
            fieldname: "file_content",
            fieldtype: "table",
            placeholder: "",
            required: false,
            hidden: false,
            readonly:true,
            displayon:["has-extracted-rows" , 1],
            addemptyrow: false,
            fields:[
                {
                    id: "name",
                    fieldlabel: "File Name",
                    fieldname: "file_name",
                    fieldtype: "text",
                    columns: 8,
                    placeholder: "Enter File Name",
                    required: false,
                    hidden: false,
                    default:"0"
                },
            ]
        },

    ],
}