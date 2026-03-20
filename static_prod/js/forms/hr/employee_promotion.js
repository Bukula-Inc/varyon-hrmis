export default {
    setup: {
        new_form_id: 'new-promotion',
        info_form_id: 'employee-promotion-info',
        title: "Employee Promotion",
        layout_columns: 4,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
        model: "Employee_Promotion"
    },
    fields: [
        {
            id: "employee",
            fieldlabel: "Employee No",
            fieldname: "employee",
            fieldtype: "link",
            model: "Employee",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            filters: {
                status: "Active",
            }, 
        },
        {
            id: "employee-name",
            fieldlabel: "Employee Name",
            fieldname: "employee_name",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"employee",
            fetchfield: "full_name"
        },
       
        {
            id: "promotion-date",
            fieldlabel: "Promotion Date",
            fieldname: "promotion_date",
            fieldtype: "date",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            value: lite.utils.today()
        },
        {
            id: "company",
            fieldlabel: "Council",
            fieldname: "company",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: true,
            fetchfrom:"employee",
            fetchfield: "company"
        },
        {
            id: "department",
            fieldlabel: "Department /  Unit",
            fieldname: "department",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"employee",
            fetchfield: "department"
        },
       
        {
            id: "current-basic",
            fieldlabel: "Current Basic Pay",
            fieldname: "current_basic",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"employee",
            fetchfield: "basic_pay"
        },
        {
            id: "salary-details",
            fieldlabel: "Promotion Details",
            fieldname: "ci",
            fieldtype: "section-break",
            addborder: true,
            columns: 1,
            hidden: false,
        },

        {
            id: "promotion_options",
            fieldlabel: "Promotion Options",
            fieldname: "promotion_options",
            fieldtype: "select",
            options: ["Salary Based",], // "Position Based"
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            default: "Salary Based",
        },
        {
            id: "role",
            fieldlabel: "Select New Role",
            fieldname: "role",
            fieldtype: "link",
            model: "Role",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            displayon: ["promotion_options", "Position Based"]
        },

        {
            id: "salary_promotion_options",
            fieldlabel: "Salary Promotion Options",
            fieldname: "salary_promotion_options",
            fieldtype: "select",
            options: ["Add Salary Components", "Use Employee Grade"],
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            default: "Add Salary Components",
            displayon: ["promotion_options", "Salary Based"],
        },
        {
            id: "employee_grade",
            fieldlabel: "Select Employee Grade",
            fieldname: "employee_grade",
            fieldtype: "link",
            model: "Employee_Grade",
            columns: 1,
            placeholder: "Enter Select Employee Grade",
            required: false,
            hidden: false,
            displayon: ["salary_promotion_options", "Use Employee Grade"]
        },

        {
            id: "revised-basic",
            fieldlabel: "Revised Basic Pay",
            fieldname: "revised_basic",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            displayon: ["promotion_options", "Salary Based"]
        },
        {
            id: "earnings",
            fieldlabel: "Earnings",
            fieldname: "earnings",
            fieldtype: "table",
            model: "Earnings",
            required: false,
            hidden: false,
            
            columns: 2,
            // displayon: ["promotion_options", "Salary Based"],
            fields: [
                {
                    id: "earning",
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
            
            columns: 2,
            fields: [
                {
                    id: "deduction",
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

        {
            id: "salary-details",
            fieldlabel: "Terms and Conditions of Promotion",
            fieldname: "ci",
            fieldtype: "section-break",
            addborder: true,
            columns: 1,
            hidden: false,
        },
        {
            id: "terms_and_conditions",
            fieldlabel: "Term of Promotion",
            fieldname: "terms_and_conditions",
            fieldtype: "rich",
            columns: 4,
            placeholder: " ",
            required: false,
            hidden: false,
            height: 300,
        },
    ],
}