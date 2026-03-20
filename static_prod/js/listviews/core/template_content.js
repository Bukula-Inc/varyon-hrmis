import { wipe_all_transactions } from "./functions.js"
export default {
    setup: {
        model: 'Template_Content',
        list_height: 50,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: true,
        allow_export_csv: false,
        allow_export_excel: false,
        allow_print: false
    },
    filters: [
        {
            id: "template-content-name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Template_Content',
            columns: 1,
            placeholder: "Template Content Name",
        },
    ],
    actions: {
        main: [ ],
        row: [ ]
    },
    columns: [
        {
            column_title: "Template Type",
            column_name: "template_type",
            column_type: "text",
            columns: 1,
            sortable: true
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
            sortable: true
        },
    ]
}