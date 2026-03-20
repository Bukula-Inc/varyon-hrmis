export default {
    setup: {
        new_form_id: 'new-template_content',
        info_form_id: 'template-content-info',
        title: "Template Content",
        layout_columns: 2,
        model: "Template_Content"
    },
    fields: [
        
        {
            id: "name",
            fieldlabel: "Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Name",
            required: true,
            hidden: false,
        },  
        {
            id: "template_type",
            fieldlabel: "Template Type",
            fieldname: "template_type",
            fieldtype: "select",
            columns: 1,
            placeholder: "Select Template Type",
            options:["Report", "Email", "Document", "Other"],
            required: true,
            hidden: false,
        },  
        {
            id: "content",
            fieldlabel: "Type or paste your template format code here (HTML, JINJA, JS)",
            fieldname: "content",
            fieldtype: "code",
            language:"html",
            theme:"light",
            columns: 3,
            placeholder: "Type or Paste html here",
            required: true,
            hidden: false,
            classnames:"h-[450px] py-3"
        } , 
    ],
}