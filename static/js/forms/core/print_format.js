export default {
    setup: {
        new_form_id: 'form',
        info_form_id: 'info',
        title: "Print Format",
        layout_columns: 3,
        model: "Print_Format"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Print Format Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Print Format Name",
            required: true,
            hidden: false,
            
        },
        {
            id: "app-model",
            fieldlabel: "Model Name",
            fieldname: "app_model",
            fieldtype: "link",
            model:"Model",
            columns: 1,
            placeholder: "Select Model Name",
            required: false,
            hidden: false,
            
        },
        {
            id: "is-default",
            fieldlabel: "Is Default",
            fieldname: "is_default",
            fieldtype: "check",
            columns: 1,
            placeholder: "Is Default",
            required: false,
            hidden: false,
            
        },
        {
            id: "html",
            fieldlabel: "Type or paste your print format code here (HTML, JINJA, JS)",
            fieldname: "html",
            fieldtype: "code",
            language:"html",
            theme:"light",
            columns: 3,
            placeholder: "Type or Paste html here",
            required: true,
            hidden: false,
            
            classnames:"h-[450px] py-3"
        }        
    ],
}