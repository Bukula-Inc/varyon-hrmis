

export default {
    setup: {
        model: 'Long_Term_Sponsorship',
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
            model: 'Long_Term_Sponsorship',
            columns: 1,
            placeholder: "Name",
        },
        {
            id: "industry",
            fieldname: "industry",
            fieldtype: "link",
            model: 'Industry',
            columns: 1,
            placeholder: "Select Industry",
        },
        {
            id: "sector",
            fieldname: "sector",
            fieldtype: "link",
            model: 'Sector',
            columns: 1,
            placeholder: "Select Sector",
        },

    ],
    actions: {
        
    },
    default_filters:{
        employee: lite.employee_info?.name
    },

         columns: [
        {
            column_title: "Employee No",
            column_name: "employee",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Course of Study",
            column_name: "course_of_study",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Council",
            column_name: "institution",
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