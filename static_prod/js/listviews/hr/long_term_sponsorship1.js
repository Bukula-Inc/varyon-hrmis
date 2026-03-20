
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
       
    ],
    actions: {
        main: [
            
        ],
        row: [
            {
                fun: wipe_all_transactions,
                title: 'Get JSON',
                icon: 'code',
                icon_color: 'teal',
            },
        ]
    },
    columns: [
        // {
        //     column_title: "Employee No",
        //     column_name: "employee",
        //     column_type: "text",
        //     columns: 1,
        // },
        // {
        //     column_title: "Course of Study",
        //     column_name: "course_of_study",
        //     column_type: "text",
        //     columns: 1,
        // },
        // {
        //     column_title: "Council",
        //     column_name: "institution",
        //     column_type: "text",
        //     columns: 1,
        // },
        // {
        //     column_title: "Status",
        //     column_name: "status",
        //     column_type: "status",
        //     columns: 1,
        // },
        
    ]
}