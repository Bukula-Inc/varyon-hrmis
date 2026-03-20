

const employee_info = await lite.connect.get_system_settings();

export default {
    setup: {
        new_form_id: 'new-training-program-feedback',
        info_form_id: 'training-program-feedback-info',
        title: "Training Program Feedback",
        layout_columns: 6,
        model: "Training_Feedback",
        allow_submit: true,
        allow_cancel: false,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
        allow_disable: false,
    },
    fields: [
        {
            id: "name",
            fieldlabel: "FeedBack",
            fieldname: "name",
            fieldtype: "text",
            columns: 2,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "employee",
            fieldlabel: "Employee ",
            fieldname: "employee",
            fieldtype: "read-only",
            columns: 2,
            placeholder: " ",
            required: false,
            hidden: false,
            default: lite?.employee_info?.name
        },
        {
            id: "training_program",
            fieldlabel: "Training Program",
            fieldname: "training_event",
            fieldtype: "link",
            model: "Training_Program",
            columns: 2,
            placeholder: " ",
            required: true,
            hidden: false, 
        },
        {
            id: "report-attachment",
            fieldlabel: "Report Attachment",
            fieldname: "report_attachment",
            fieldtype: "file",
            columns: 3,
            required: false,
            placeholder: " ",
        },
        {
            id: "other-attachment",
            fieldlabel: "Other Attachments",
            fieldname: "other_attachments",
            model: "Traaing_Program_attachment",
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
                    columns: 1,
                    required: false,
                    placeholder: " ",
                },
                {
                    id: "attachment",
                    fieldlabel: "Attachment",
                    fieldname: "attachment",
                    fieldtype: "file",
                    columns: 5,
                    required: false,
                    placeholder: " ",
                },                
            ]
        },
    ]
}
