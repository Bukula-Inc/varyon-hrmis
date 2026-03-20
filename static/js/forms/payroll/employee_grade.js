;
export default {
    setup: {
        new_form_id: 'new-employee-grade',
        info_form_id: 'employee-grade-info',
        title: "Employee Grade",
        layout_columns: 8,
        model: "Employee_Grade"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Employee Grade Name",
            fieldname: "name",
            columns: 2,
            required: true,
            hidden: false,
            placeholder: " ",
        },
        {
            id: "company",
            fieldlabel: "Council",
            fieldname: "company",
            fieldtype: "link",
            model: "Company",
            columns: 2,
            required: false,
            hidden: true,
            placeholder: " ",
            filters: {
                is_group: 0,
                is_root: 0
            },
            default: lite.user.company.name,
        },
        {
            id: "payment-frequency",
            fieldlabel: "Payment Frequency",
            fieldname: "payment_frequency",
            fieldtype: "select",
            columns: 2,
            required: false,
            hidden: false,
            placeholder: " ",
            options: ["Monthly", "Weekly"],
            default:"Monthly"
        },
        {
            id: "basic-pay",
            fieldlabel: "Basic Pay",
            fieldname: "basic_pay",
            fieldtype: "currency",
            columns: 2,
            required: false,
            hidden: false,
            placeholder: " ",
        },
        {
            id: "earnings-deds",
            fieldlabel: "",
            fieldname: "",
            fieldtype: "section-break",
            required: false,
            hidden: false,
            addborder: true
        },
        {
            id: "earnings",
            fieldlabel: "Grade Earnings",
            fieldname: "earnings",
            fieldtype: "table",
            model: "Employee_Grade_Earning",
            description: "Add grade earnings",
            columns: 4,
            required: false,
            hidden: false,
            fields: [
                {
                    id: "earning-component",
                    fieldlabel: "Earning Component",
                    fieldname: "component",
                    fieldtype: "link",
                    model: "Salary_Component",
                    columns: 8,
                    required: false,
                    hidden: false,
                    placeholder: " ",
                    filters: {
                        component_type: "Earning",
                    }
                },
            ]
        },
        {
            id: "deductions",
            fieldlabel: "Grade Deductions",
            fieldname: "deductions",
            fieldtype: "table",
            model: "Employee_Grade_Deduction",
            description: "Add grade deductions",
            columns: 4,
            required: false,
            hidden: false,
            fields: [
                {
                    id: "deduction-component",
                    fieldlabel: "Deduction Component",
                    fieldname: "component",
                    fieldtype: "link",
                    model: "Salary_Component",
                    columns: 8,
                    required: false,
                    hidden: false,
                    placeholder: " ",
                    filters: {
                        component_type: "Deduction",
                    }
                },
            ]
        },
    ],
}