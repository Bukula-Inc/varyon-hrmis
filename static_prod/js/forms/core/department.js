;
const ss = await lite.connect.get_system_settings()

export default {
    setup: {
        model: "Department",
        new_form_id: 'new-department',
        info_form_id: 'department-info',
        title: "Department",
        layout_columns: 2,
    },
    fields: [
        {
            id: "department",
            fieldlabel: "Department /  Unit",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Department",
            required: true,
            hidden: false,
            description: ""
        },
        {
            id: "department",
            fieldlabel: "Head Of Department",
            fieldname: "head_of_department",
            fieldtype: "link",
            model:"Lite_User",
            columns: 1,
            placeholder: "Head Of Department",
            required: false,
            hidden: false,
            description: ""
        },
    
        {
            id: "company",
            fieldlabel: "Council",
            fieldname: "company",
            fieldtype: "link",
            model: "Company",
            columns: 1,
            placeholder: "Enter Company",
            required: false,
            hidden: false,
            default:ss?.data?.default_company
        },
        {
            id: "cost-center",
            fieldlabel: "Cost Center",
            fieldname: "cost_center",
            fieldtype: "link",
            model: "Cost_Center",
            columns: 1,
            placeholder: "Enter Cost Center",
            required: false,
            hidden: false,
            description: ""
        },
       

    ]
}