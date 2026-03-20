export default {
    setup: {
        model: 'Second_Salary_Advance_Application',
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
            model: 'Second_Salary_Advance_Application',
            columns: 1,
            placeholder: "Select Name",
        },
    ],
    actions: {
        main: [],
        row: []
    },
    default_filters:{
        individual: lite.user?.name
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
            column_title: "Disbursed On",
            column_name: "disbursed_on",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Due Date",
            column_name: "due_date",
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