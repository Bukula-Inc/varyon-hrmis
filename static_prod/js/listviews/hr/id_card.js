import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'ID_Card',
        list_height: 50,
        allow_submit: true,
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
            model: 'ID_Card',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
        },
        {
            id: "officer-name",
            fieldname: "officer_name",
            fieldtype: "link",
            model: 'ID_Card',
            linkfield: "officer_name",
            columns: 1,
            placeholder: "Officer's Name",
        },
     
       
    ],
    actions: {
        main: [
            
        ],
        row: [
            {
                fun: wipe_all_transactions,
                title: 'Get JSON',
                icon: 'code',
                icon_color: 'teal',
            },
        ]
    },
    columns: [
        {
            column_title: "Officer Name",
            column_name: "officer_name",
            column_type: "text",
            columns: 4,
        },
        {
            column_title: "Job Title",
            column_name: "job_title",
            column_type: "text",
            columns: 4,
        },        
    ]
}