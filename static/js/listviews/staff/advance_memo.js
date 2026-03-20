export default {
    setup: {
        model: 'Advance_Memo',
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
            model: 'Advance_Memo',
            columns: 1,
            placeholder: "Select Name",
        },
    ],
    actions: {
        main: [],
        row: []
    },
    
    default_filters:{
        employee_id: lite.employee_info?.name
    },
    columns: [
        {
            column_title: "Employee No",
            column_name: "employee_id",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Requested Amount",
            column_name: "amount",
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