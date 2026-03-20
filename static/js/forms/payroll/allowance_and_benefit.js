export default {
    setup: {
        new_form_id: 'new-allowance-and-benefit',
        info_form_id: 'allowance-and-benefit-info',
        title: "Allowance and Benefit",
        layout_columns: 6,
        model: "Allowance_and_Benefit",
        allow_submit:false,
        allow_cancel:false,
        allow_delete:true
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 2,
            placeholder: " ",
            required: false,
            hidden: false,
            // filters: {
            //     status: "Active"
            // }
        },
        {
            id: "extra-fields",
            fieldlabel: "Extra fields",
            fieldname: "extra_fields",
            fieldtype: "select",
            columns: 2,
            placeholder: " ",
            required: false,
            hidden: false,
            options: ["Transportation Description", "Medical Benefits", "None"],
            default: "None"   
        },
        {
            id: "affects-payroll",
            fieldlabel: "affects payroll",
            fieldname: "affects_payroll",
            fieldtype: "check",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            
        },
        {
            id: "create-salary-component",
            fieldlabel: "Create Salary Component",
            fieldname: "create_salary_component",
            fieldtype: "check",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            
        },
        {
            id: "description",
            fieldlabel: "Description",
            fieldname: "description",
            fieldtype: "rich",
            columns: 6,
            placeholder: " ",
            required: false,
            hidden: false,
            height: 200,
            
        },
        {
            id: "categories",
            fieldlabel: "Category",
            fieldname: "categories",
            fieldtype: "table",
            model: "Allowance_and_Benefit_Category",
            columns: 6,
            placeholder: " ",
            required: false,
            hidden: false,
            fields:[
                {
                    id: "salary-grade",
                    fieldlabel: "Salary Grade",
                    fieldname: "salary_grade",
                    fieldtype: "link",
                    model: "Employee_Grade",
                    columns: 6,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    
                },
                {
                    id: "ab-amount",
                    fieldlabel: "Allowance and Benefit Amount",
                    fieldname: "amount",
                    fieldtype: "float",
                    columns: 2,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    classnames: "text-end font-semibold text-[2rem]",
                    displayon: ["extra-fields", "None", "Transportation Description"],
                    default: "0.00"
                    
                },
                {
                    id: "transportation",
                    fieldlabel: "Transportation",
                    fieldname: "transportation",
                    fieldtype: "text",
                    columns: 2,
                    placeholder: " ",
                    required: false,
                    hidden: true,
                    classnames: "text-end font-semibold text-[2rem]",
                    displayon: ["extra-fields", "Transportation Description"],
                    default: ""
                    
                },
                {
                    id: "in-patient",
                    fieldlabel: "In Patient",
                    fieldname: "in_patient",
                    fieldtype: "float",
                    columns: 1,
                    placeholder: " ",
                    required: false,
                    hidden: true,
                    classnames: "text-end font-semibold text-[2rem]",
                    displayon: ["extra-fields", "Medical Benefits"],
                    default: "0.00"
                    
                },
                {
                    id: "out-patient",
                    fieldlabel: "Out Patient",
                    fieldname: "out_patient",
                    fieldtype: "float",
                    columns: 1,
                    placeholder: " ",
                    required: false,
                    hidden: true,
                    classnames: "text-end font-semibold text-[2rem]",
                    displayon: ["extra-fields", "Medical Benefits"],
                    default: "0.00"
                    
                },
                {
                    id: "optical",
                    fieldlabel: "Optical",
                    fieldname: "optical",
                    fieldtype: "float",
                    columns: 1,
                    placeholder: " ",
                    required: false,
                    hidden: true,
                    classnames: "text-end font-semibold text-[2rem]",
                    displayon: ["extra-fields", "Medical Benefits"],
                    default: "0.00"
                    
                },
                {
                    id: "dental",
                    fieldlabel: "Dental",
                    fieldname: "dental",
                    fieldtype: "float",
                    columns: 1,
                    placeholder: " ",
                    required: false,
                    hidden: true,
                    classnames: "text-end font-semibold text-[2rem]",
                    displayon: ["extra-fields", "Medical Benefits"],
                    default: "0.00"
                    
                },
            ]
            
        },
    ],
}