export default {
    setup: {
        new_form_id: 'new-probation',
        info_form_id: 'probation-info',
        title: "Probation",
        layout_columns: 4,
        model: "Probation"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Probation Title ",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "length",
            fieldlabel: "Probation Period (Month)",
            fieldname: "probation_length",
            fieldtype: "select",
            options: [1,2,3,4,5,6,7,8,9,10,11,12],
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
        {
            id: "intervals",
            fieldlabel: "Length Intervals",
            fieldname: "length_intervals",
            fieldtype: "readonly",
            option: ["Months"],
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: true,
            default: "Months"
        },
       
        {
            id: "basic-pay",
            fieldlabel: "Basic Pay",
            fieldname: "basic_pay",
            fieldtype: "float",
            columns: 1,
            required: false,
            hidden: false,
        },

        {
            id: "earnings",
            fieldlabel: "Earnings",
            fieldname: "earnings",
            fieldtype: "table",
            model: "Earnings",
            required: false,
            hidden: false,
            addemptyrow: false,            
            columns: 2,
            fields: [
                {
                    id: "name",
                    fieldlabel: "Name",
                    fieldname: "earning",
                    fieldtype: "link",
                    model: "Salary_Component",
                    columns: 7,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    istablefield: true,
                    filters:{
                        component_type:"Earning"
                    }
                },
            
            ]
        },

        {
            id: "deductions",
            fieldlabel: "Deductions",
            fieldname: "deductions",
            fieldtype: "table",
            model: "Salary_Component",
            required: false,
            hidden: false,
            addemptyrow: false,
            columns: 2,
            fields: [
                {
                    id: "deduction-name",
                    fieldlabel: "Name",
                    fieldname: "deduction",
                    fieldtype: "link",
                    model: "Salary_Component",
                    columns: 7,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    istablefield: true,
                    filters:{
                        component_type:"Deduction"
                    }
                },
            ]
        },
    ],
}