export default {
    setup: {
        new_form_id: 'new-separation-type',
        info_form_id: 'separation-type-info',
        title: "Separation Type",
        layout_columns: 3,
        model: "Separation_Type",
        allow_submit:false,
        allow_cancel:false,
        allow_delete:true
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Separation Type",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            // filters: {
            //     status: "Active"
            // }
        },
        {
            id: "interview-question",
            fieldlabel: "Interview Question",
            fieldname: "interview_question",
            fieldtype: "link",
            model: "Exit_Interview_Question",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: true,
            // filters: {
            //     status: "Active"
            // }
        },
        {
            id: "description",
            fieldlabel: "Description",
            fieldname: "description",
            fieldtype: "rich",
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
            height: 200,
            
        },
        {
            id: "separation-package",
            fieldlabel: "Separation Package",
            fieldname: "separation_package",
            fieldtype: "table",
            model: "Separation_Package",
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
            fields:[
                {
                    id: "package-item",
                    fieldlabel: "Package Item",
                    fieldname: "package_item",
                    fieldtype: "link",
                    model: "Allowance_and_Benefit",
                    columns: 10,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    
                },
            ]
            
        },
    ],
}