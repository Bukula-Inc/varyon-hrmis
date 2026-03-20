export default {
    setup: {
        new_form_id: 'new-disciplinary-Committee',
        info_form_id: 'info-disciplinary-Committee',
        title: "Disciplinary Committee",
        layout_columns: 2,
        model: "Disciplinary_Committee"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Disciplinary Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            // placeholder: "Enter Disciplinary Name",
            required: true,
            hidden: false,
            default: "",
        },
        {
            id: "for-charge",
            fieldlabel: "For Charge",
            fieldname: "charge",
            fieldtype: "link",
            model: "Charge_Form",
            columns: 1,
            placeholder: "Enter Charge",
            required: true,
            hidden: false,
            default: "",
        },
        {
            id: "chairperson",
            fieldlabel: "Chairperson",
            fieldname: "chairperson",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Disciplinary Chairperson",
            required: true,
            hidden: false,
            default: "",
        },
        

        {
            id: "external_members",
            fieldlabel: "Internal Committee Members",
            fieldname: "internal_members",
            fieldtype: "table",
            columns: 2,
            required: false,
            hidden: false,
            model: "Internal_Disciplinary_Committee_Member",
            fields: [
                {
                    id: "member_email",
                    fieldlabel: "Select User",
                    fieldname: "member_email",
                    fieldtype: "link",
                    model: "Lite_User",
                    columns: 4,
                    placeholder: "Select User",
                    required: false,
                    hidden: false,
                    istablefield: true,
                },

                {
                    id: "member_name",
                    fieldlabel: "Member Name",
                    fieldname: "member_name",
                    fieldtype: "text",
                    columns: 4,
                    placeholder: "Member Name",
                    required: false,
                    hidden: false,
                    istablefield: true,
                    fetchfrom: "member_email",
                    fetchfield: "first_name"
                },
                
            ]
        },



        {
            id: "external_members",
            fieldlabel: "External Committee Members",
            fieldname: "external_members",
            fieldtype: "table",
            columns: 2,
            required: false,
            hidden: false,
            model: "External_Disciplinary_Committee_Member",
            fields: [
                {
                    id: "member_email",
                    fieldlabel: "Email",
                    fieldname: "member_email",
                    fieldtype: "text",
                    model: "Lite_User",
                    columns: 4,
                    placeholder: "Enter Email",
                    required: false,
                    hidden: false,
                    istablefield: true,
                },

                {
                    id: "member_name",
                    fieldlabel: "Member Name",
                    fieldname: "member_name",
                    fieldtype: "text",
                    columns: 4,
                    placeholder: "Member Name",
                    required: false,
                    hidden: false,
                    istablefield: true,
                    fetchfrom: "member_email",
                    fetchfield: "first_name"
                },
            ]
        },
        
    ],
}