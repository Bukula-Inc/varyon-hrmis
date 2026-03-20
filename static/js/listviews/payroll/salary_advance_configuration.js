export default {
    setup: {
        model: 'Salary_Advance_Configuration',
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
            model: 'Salary_Advance_Configuration',
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
            column_title: "Council",
            column_name: "name",
            column_type: "text",
            columns: 1,
        },
    ]
}