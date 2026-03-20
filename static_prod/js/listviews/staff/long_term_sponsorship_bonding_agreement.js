

export default {
    setup: {
        model: 'Long_Term_Sponsorship_Bonding_Period',
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
            model: 'Long_Term_Sponsorship_Bonding_Period',
            columns: 1,
            placeholder: "Name",
        },

    ],
    actions: {},
    default_filters:{
        employee: lite.employee_info?.name
    },

         columns: [
        {
            column_title: "Agreement Date",
            column_name: "agreement_date",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Employee No",
            column_name: "employee",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Applicant Names",
            column_name: "applicant_names",
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