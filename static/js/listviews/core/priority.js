import { wipe_all_transactions } from "./functions.js";

export default {
    setup: {
        model: 'Priority',
        list_height: 50,
        allow_submit: false,
        allow_cancel: true,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Priority',
            columns: 1,
            placeholder: "Pick Priority Name",
        },
      

    ],
    actions: {
        
    },
    columns: [
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        }, 
    ]
}