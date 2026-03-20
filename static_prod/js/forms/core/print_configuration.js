export default {
    setup: {
        new_form_id: 'new-print-configuration',
        info_form_id: 'print-configuration-info',
        title: "Print configuration",
        layout_columns: 2,
        model: "Print_Configuration"
    },
    fields: [
        
        {
            id: "app-model",
            fieldlabel: "Model Name",
            fieldname: "app_model",
            fieldtype: "link",
            model:"Model",
            columns: 1,
            placeholder: "Select Model",
            required: true,
            hidden: false,
            
        } ,    
        {
            id: "configuration-fields",
            fieldlabel: "Model Name",
            fieldname: "configuration_fields",
            fieldtype: "table",
            model:"Print_Configuration_Field",
            placeholder: "",
            required: true,
            hidden: false,
            
            fields:[
                {
                    id: "field-name",
                    fieldlabel: "Field Name",
                    fieldname: "field_name",
                    fieldtype: "read-only",
                    columns: 5,
                    placeholder: "Select Field",
                    required: true,
                    hidden: false,
                    
                    classnames:"font-semibold"
                },
                {
                    id: "field-type",
                    fieldlabel: "Field Type",
                    fieldname: "field_type",
                    fieldtype: "read-only",
                    columns: 5,
                    placeholder: "Select Field Type",
                    required: true,
                    hidden: false,
                    
                    classnames:"font-semibold"
                },
                {
                    id: "columns",
                    fieldlabel: "Layout Columns",
                    fieldname: "columns",
                    fieldtype: "text",
                    columns: 5,
                    placeholder: "Enter Columns",
                    required: true,
                    hidden: false,
                    
                    classnames:"font-semibold"
                },
                {
                    id: "linked-model",
                    fieldlabel: "Linked Model",
                    fieldname: "linked_model",
                    fieldtype: "read-only",
                    columns: 5,
                    placeholder: "Select Linked Model",
                    required: false,
                    hidden: false,
                    
                    classnames:"font-semibold"
                },
                {
                    id: "include-in-print",
                    fieldlabel: "Include In Print",
                    fieldname: "include_in_print",
                    fieldtype: "check",
                    columns: 3,
                    placeholder: "",
                    required: false,
                    hidden: false,
                    
                    default:1
                },
            ]
        }     
    ],
}