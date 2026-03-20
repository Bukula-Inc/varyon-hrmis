export default {
    setup: {
        model: 'Account_Branch_Code',
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
            model: 'Account_Branch_Code',
            columns: 1,
            placeholder: "Select Name",
        },
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            column_title: "Bank",
            column_name: "bank",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Branch Code",
            column_name: "sort_code",
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