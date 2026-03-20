export default {
    setup: {
        model: 'Domain_Controller',
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
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Domain_Controller',
            linkfield: "name",
            columns: 1,
            placeholder: "Domain Controller Name",
        },
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            column_title: "IP Address",
            column_name: "domain_ip",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "URL",
            column_name: "domain_url",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Record Type",
            column_name: "domain_default_record_type",
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