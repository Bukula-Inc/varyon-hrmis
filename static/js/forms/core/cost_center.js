export default {
    setup: {
        new_form_id: 'new-cost-center',
        info_form_id: 'cost-center-info',
        title: "Cost Center",
        layout_columns: 2,
        model: "Cost_Center"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Cost Center Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Cost Center Name",
            required: true,
            hidden: false,
        },
        {
            id: "name",
            fieldlabel: "Company",
            fieldname: "company",
            fieldtype: "link",
            model:"Company",
            columns: 1,
            placeholder: "Enter Company",
            required: true,
            hidden: false,
            default: lite.defaults?.company?.name
        },
        {
            id: "project",
            fieldlabel: "Project",
            fieldname: "project",
            fieldtype: "link",
            model:"Project",
            columns: 1,
            placeholder: "Enter Project",
            required: false,
            hidden: false,
        },
        {
            id: "name",
            fieldlabel: "Customer",
            fieldname: "customer",
            fieldtype: "link",
            model:"Customer",
            columns: 1,
            placeholder: "Enter Customer",
            required: false,
            hidden: false,
            fetchfrom:"project",
            fetchfield: "client",
        },
        {
            id: "is-group",
            fieldlabel: "Is Group",
            fieldname: "is_group",
            fieldtype: "check",
            columns: 1,
            placeholder: "Is Group",
            required: false,
            hidden: true,
            default:"0"
        },

    ],
}