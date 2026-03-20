export default {
    setup: {
        model: 'Salary_Component',
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
            model: 'Salary_Component',
            columns: 1,
            placeholder: "Name",
        },
        {
            id: "type",
            fieldname: "component_type",
            fieldtype: "select",
            columns: 1,
            placeholder: "Select Component Type",
            options: ["Earning", "Deduction"]
        },
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            column_title: "Type",
            column_name: "component_type",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Percentage",
            column_name: "percentage",
            column_type: "percentage",
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