export default {
    setup: {
        new_form_id: 'form',
        info_form_id: 'info',
        title: "Share Type",
        layout_columns: 2,
        model: "Share_Type"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Share Type Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Share Type Name",
            required: true,
            hidden: false,
            description: "Share Type Name",
        },
        {
            id: "currency",
            fieldlabel: "Currency",
            fieldname: "currency",
            fieldtype: "link",
            model:"Currency",
            columns: 1,
            placeholder: "Select Currency",
            required: true,
            hidden: false,
            description: "Select Currency",
        },
        {
            id: "amount-per-share",
            fieldlabel: "Price Per Share",
            fieldname: "price_per_share",
            fieldtype: "float",
            columns: 1,
            placeholder: "Enter Price Per Share",
            required: true,
            hidden: false,
            description: "Share Type Name",
        },

    ],
}