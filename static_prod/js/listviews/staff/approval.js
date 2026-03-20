;
export default {
    setup: {
        model: "Approver",
        list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true,
    },
    filters: [
        {
            id: "filter-created_on-date",
            fieldname: "created_on",
            fieldtype: "date",
            mode:"single",
            columns: 1,
            placeholder: "Creation Date",
        },
        {
            id: "initializer",
            fieldname: "owner",
            fieldtype: "link",
            mode:"Lite_User",
            columns: 1,
            placeholder: "Initialized By",
        },
        {
            id: "document_type",
            fieldname: "for_doctype",
            fieldtype: "link",
            model:"Model",
            columns: 1,
            placeholder: "Select Document Type",
        },
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            column_title: "Initialized By",
            column_name: "owner_first_name",
            column_type: "text",
            columns: 3,
            formatter: (value, rest)=>{
                return `${value}`
            }
        },
        {
            column_title: "Document Type",
            column_name: "for_doctype",
            column_type: "text",
            columns: 2,
            formatter: (value, rest)=>{
                return lite.utils.replace_chars(value, "_", " ")
            }
        },
        {
            column_title: "Current Stage",
            column_name: "current_stage",
            column_type: "status",
            columns: 3,
        },
    ]
}