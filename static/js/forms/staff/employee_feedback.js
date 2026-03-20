;

export default {
    setup: {
        new_form_id: 'new-staff-employee-feedback',
        info_form_id: 'staff-employee-feedback-info',
        title: "Training Program Feedback",
        layout_columns: 6,
        model: "Training_Feedback",
        allow_delete: false,
        allow_disable: false,
    },
    fields: [
        {
            id: "employee",
            fieldlabel: "Employee No",
            fieldname: "employee",
            fieldtype: "link",
            model: "Employee",
            columns: 2,
            placeholder: " ",
            required: false,
            hidden: false,
            default: lite?.employee_info?.name,
            filters: {
                status: "Active",
            }, 
        },
        {
            id: "training_program",
            fieldlabel: "Training Program",
            fieldname: "training_program",
            fieldtype: "link",
            model: "Training_Program",
            columns: 2,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "relevance",
            fieldlabel: "Relevance",
            fieldname: "relevance",
            fieldtype: "select",
            options: [
                "Very Relevant",
                "Somewhat Relevant",
                "Not Very Relevant",
                "Not at All Relevant"
            ],
            columns: 2,
            required: false
        },
        {
            id: "report-attachment",
            fieldlabel: "Attachment Activity Report",
            fieldname: "report_attachment",
            fieldtype: "file",
            columns: 3,
            required: true
        },
        {
            id: "other-attachment",
            fieldlabel: "Other Attachments",
            fieldname: "other_attachments",
            fieldtype: "table",
            columns: 3,
            height: 300,
            required: false,
            fields:[
                {
                    id: "attachment-title",
                    fieldlabel: "Attachment Title",
                    fieldname: "attachment_title",
                    fieldtype: "text",
                    columns: 4,
                    required: false,
                    placeholder: " ",
                },
                {
                    id: "attachment",
                    fieldlabel: "Attachment",
                    fieldname: "attachment",
                    fieldtype: "file",
                    columns: 6,
                    required: false,
                    placeholder: " ",
                },
            ]
        },
    ],
}