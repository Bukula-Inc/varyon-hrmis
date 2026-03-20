import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Applicant_Short_List',
        list_height: 50,
        allow_submit: false,
        allow_cancel: false,
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
            model: 'Applicant_Short_List',
            linkfield: "name",
            columns: 1,
            placeholder: "Applicant",
        },
        {
            id: "designation",
            fieldname: "job_position",
            fieldtype: "link",
            model: 'Designation',
            linkfield: "name",
            columns: 1,
            placeholder: "Job Title",
        },
        {
            id: "qualification-filter",
            fieldname: "qualification",
            fieldtype: "link",
            model: 'Document',
            linkfield: "name",
            columns: 1,
            placeholder: "Qualification",
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
            column_title: "Applicant First Name",
            column_name: "applicant_first_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Applicant Last Name",
            column_name: "applicant_last_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
    ]
}