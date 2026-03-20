export default {
    setup: {
        new_form_id: 'new-recovery',
        info_form_id: 'recovery-info',
        title: "Payroll Refunds",
        layout_columns: 3,
        model: "Payroll_Refunds",
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
    },
    fields: [
        {
            id: "employee",
            fieldlabel: "Employee No",
            fieldname: "employee",
            fieldtype: "link",
            model: "Employee",
            placeholder: " ",
            columns: 1,
            required: true,
            hidden: false,
        },
        {
            id: "employee_names",
            fieldlabel: "Employee Name",
            fieldname: "employee_names",
            fieldtype: "read-only",
            placeholder: " ",
            columns: 1,
            required: false,
            hidden: false,
            fetchfrom: "employee",
            fetchfield: "full_name"
        },
        {
            id: "staff_id",
            fieldlabel: "Employee No",
            fieldname: "staff_id",
            fieldtype: "read-only",
            placeholder: " ",
            columns: 1,
            required: false,
            hidden: true,
            fetchfrom: "employee",
            fetchfield: "name"
        },
        {
            id: "refunds",
            fieldlabel: "Refunds",
            fieldname: "refunds",
            fieldtype: "table",
            model: "RefundsJSON",
            description: "add all refunds to be applied to the Employee",
            placeholder: " ",
            columns: 3,
            required: true,
            hidden: false,
            fields: [
                {
                    id: "salary_component",
                    fieldlabel: "Salary Component",
                    fieldname: "salary_component",
                    fieldtype: "link",
                    model: "Salary_Component",
                    filters: {
                        component_type: "Earning",
                        value_type: "Custom"
                    },
                    columns: 12,
                    required: true,
                    hidden: false,
                    placeholder: " ",
                },
                {
                    id: "amount",
                    fieldlabel: "Amount",
                    fieldname: "amount",
                    fieldtype: "float",
                    columns: 4,
                    required: true,
                    hidden: false,
                    placeholder: " ",
                    default: "0.00",
                    is_figure: true,
                    classnames: "text-right font-extrabold text-35 text-secondary_color bg-secondary_color/20"
                },
            ]
        }
    ],
}