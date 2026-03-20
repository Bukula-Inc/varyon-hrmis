export default {
    setup: {
        new_form_id: 'new-bonus',
        info_form_id: 'bonus-info',
        title: "Bonus",
        layout_columns: 3,
        model: "Bonus",
        allow_submit: true,
        allow_cancel: false,
        allow_print: false,
        allow_delete: false,
    },
    fields: [
        // {
        //     id: "bonus_type",
        //     fieldlabel: "Bonus Type",
        //     fieldname: "bonus_type",
        //     fieldtype: "link",
        //     model: "Bonus_Type",
        //     columns: 1,
        //     placeholder: " ",
        //     required: true,
        //     hidden: false,
        // },      
        {
            id: "bonus_calculation_type",
            fieldlabel: "Bonus Calculation Type",
            fieldname: "bonus_calculation_type",
            fieldtype: "select",
            columns: 1,
            required: false,
            hidden: false,
            options: ["Percentage",],
            default: "Percentage"
        },
        {
            id: "-id",
            fieldlabel: "Bonus Employee",
            fieldname: "si",
            fieldtype: "section-break",
            addborder: true,
            columns: 1,
            required: false,
            hidden: false,
        },
         
        {
            id: "bonus_employees",
            fieldlabel: "Add Employee For Bonus",
            fieldname: "bonus_employees",
            fieldtype: "table",
            model: "Bonus_To_Employee",
            required: false,
            hidden: false,
            
            fields: [ 
                {
                    id: "employee",
                    fieldlabel: "Employee No",
                    fieldname: "employee",
                    fieldtype: "read-only",
                    placeholder: " ",
                    model: "Employee",
                    columns: 3,
                    required: false,
                    hidden: false,
                    istablefield: true,
                    filters: {
                        status__in: ["Active", "On Leave", "Suspended"],
                    }, 
                },
                {
                    id: "employee_name",
                    fieldlabel: "Employee Name",
                    fieldname: "employee_name",
                    fieldtype: "read-only",
                    columns: 3,
                    required: true,
                    hidden: false,
                    fetchfrom: "employee",
                    fetchfield: "full_name"
        
                },
                {
                    id: "employee_designation",
                    fieldlabel: "Employee Designation",
                    fieldname: "employee_designation",
                    fieldtype: "read-only",
                    columns: 3,
                    required: true,
                    hidden: false,
                    fetchfrom: "employee",
                    fetchfield: "designation"
        
                },
                {
                    id: "department",
                    fieldlabel: "Employee Department",
                    fieldname: "department",
                    fieldtype: "read-only",
                    columns: 3,
                    required: true,
                    hidden: false,
                    fetchfrom: "employee",
                    fetchfield: "department"
        
                },
                {
                    id: "score",
                    fieldlabel: "Score (%)",
                    fieldname: "score",
                    fieldtype: "read-only",
                    columns: 3,
                    required: false,
                    hidden: false,
                    placeholder: " ",
                    is_figure: true,
                    classnames: 'text-right font-bold'
        
                },
                {
                    id: "bonus_amount",
                    fieldlabel: "Bonus Amount",
                    fieldname: "bonus_amount",
                    fieldtype: "read-only",
                    columns: 3,
                    required: false,
                    hidden: false,
                    placeholder: " ",
                    is_figure: true,
                    classnames: 'text-right font-bold'
        
                },
            ] ,
        },  
        // {
        //     id: "description",
        //     fieldlabel: "Description",
        //     fieldname: "description",
        //     fieldtype: "rich",
        //     columns: 3,
        //     required: false,
        //     hidden: false,
        //     height: 300,
        // },
    ],
}