export default {
    setup: {
        new_form_id: 'new-hr-text-templates',
        info_form_id: 'hr-text-templates-info',
        title: "HR Text Template",
        layout_columns: 6,
        model: "HR_Text_Template"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Template",
            fieldname: "name",
            fieldtype: "text",
            columns: 2,
            placeholder: "Name",
            required:false,
            hidden: false,
            default: "",
        },
        {
            id: "text-content",
            fieldlabel: "Discreption",
            fieldname: "text_content",
            fieldtype: "rich",
            height: "400px",
            columns: 6,
            placeholder: " ",
            required:false,
            hidden: false,
            default: "",
        },
    ],
} 