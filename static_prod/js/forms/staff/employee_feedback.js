;

export default {
    setup: {
        new_form_id: 'new-staff-employee-feedback',
        info_form_id: 'staff-employee-feedback-info',
        title: "Employee Feedback",
        layout_columns: 2,
        model: "Employee_Feedback",
        allow_delete: false,
        allow_disable: false,
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Feedback Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
        {
            id: "type-id",
            fieldlabel: "Type",
            fieldname: "si",
            fieldtype: "section-break",
            addborder: true,
            columns: 1,
            required: false,
            hidden: false,
        },
        {
            id: "questions",
            fieldlabel: "Questions",
            fieldname: "questions",
            fieldtype: "check",
            columns: 1,
            required: false,
            hidden: false,
        },
       
      
        {
            id: "comments",
            fieldlabel: "Comments",
            fieldname: "comments",
            fieldtype: "check",
            columns: 1,
            required: false,
            hidden: false,
        },
    
       
        {
            id: "your-feedback",
            fieldlabel: "Your Feedback",
            fieldname: "your_feedback",
            fieldtype: "text",
            columns: 1,
            required: false,
            hidden: false,
        },
      
        {
            id: "email",
            fieldlabel: "Email",
            fieldname: "email",
            fieldtype: "read-only",
            columns: 1,
            required: false,
            hidden: false,
            default: lite?.employee_info?.email,
        },

        {
            id: "first-name",
            fieldlabel: "First Name",
            fieldname: "first_name",
            fieldtype: "read-only",
            columns: 1,
            required: false,
            hidden: false,
            default: lite?.employee_info?.first_name,
        },
      
        {
            id: "last-name",
            fieldlabel: "Last Name",
            fieldname: "last_name",
            fieldtype: "read-only",
            columns: 1,
            required: false,
            hidden: false,
            default: lite?.employee_info?.last_name,
        },
    ],
}