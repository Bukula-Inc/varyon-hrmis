export default {
    setup: {
        new_form_id: 'new-training-result',
        info_form_id: 'training-result-info',
        title: "Training Result",
        layout_columns: 3,
        model: "Training_Result",
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
    },
    fields: [
        {
            id: "employees",
            fieldlabel: "Employees",
            fieldname: "employees",
            fieldtype: "table",
            required: true,
            hidden: false,
            model: "Result",
            fields: [
                {
                    id: "training-event",
                    fieldlabel: "Training Event",
                    fieldname: "training_event",
                    fieldtype: "link",
                    model: "Training_Event",
                    columns: 1,
                    placeholder: " ",
                    required: true,
                    hidden: false,
                },
                {
                    id: "employee",
                    fieldlabel: "Employee No",
                    fieldname: "employee",
                    fieldtype: "link",
                    model: "Employee",
                    columns: 1,
                    placeholder: " ",
                    required: true,
                    hidden: false,
                    istablefield: true,
                    fetchfrom:"training-event",
                    fetchfield: "employee",
                    filters: {
                        status: "Active",
                    }, 
                },
              
                {
                    id: "hours",
                    fieldlabel: "Hours",
                    fieldname: "hours",
                    fieldtype: "text",
                    columns: 1,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                },
                {
                    id: "grade",
                    fieldlabel: "Grade",
                    fieldname: "grade",
                    fieldtype: "text",
                    columns: 1,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                },
                {
                    id: "comment",
                    fieldlabel: "Comment",
                    fieldname: "comment",
                    fieldtype: "text",
                    columns: 1,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                },
               
                
            ]
        },
       
      
    ],
}