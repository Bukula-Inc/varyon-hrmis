export default {
    setup: {
        new_form_id: 'new-salary-component-allocation',
        info_form_id: 'salary-component-info-allocation',
        title: "Employee Salary Allocation",
        layout_columns: 4,
        model: "Salary_Component_Allocation",
    },
    fields: [

        {
            id: "name",
            fieldlabel: "Component Name",
            fieldname: "name",
            fieldtype: "read-only",
            model: "Salary_Component",
            columns: 2,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "component_type",
            fieldlabel: "Component Type",
            fieldname: "component_type",
            fieldtype: "read-only",
            model: "Salary_Component",
            columns: 2,
            placeholder: " ",
            required: false,
            hidden: false,
        },       
        {
            id: "employee",
            fieldlabel: "Employees",
            fieldname: "employee",
            fieldtype: "table",
            model: "Employee",
            required: false,
            hidden: false,
            
            columns: 4,
            fields: [

                {
                    id: "employee",
                    fieldlabel:  "Employee No",
                    fieldname: "employee",
                    fieldtype: "link",
                    model: "Employee",
                    columns: 7,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    istablefield: true,
                    filters: {
                        status: "Active"
                    }
                },
            ]
        },

    ],
}