export default {
    setup: {
        new_form_id: 'change-password',
        info_form_id: 'change-password',
        title: "Change Password",
        layout_columns: 2,
        model: "Change_Password",
        action_type: "save"
    },
    fields: [
        { 
            id:"old-password",
            fieldlabel:"Old Password",
            fieldname:"old_password",
            fieldtype:"password",
            required: true,
            placeholder:"Old Password",
            columns:2
        },
        { 
            id:"new-password",
            fieldlabel:"New Password",
            fieldname:"new_password",
            fieldtype:"password",
            required: true,
            placeholder:"New Password"
        },
        { 
            id:"rpt-password",
            fieldlabel:"Repeat New Password",
            fieldname:"rpt_password",
            fieldtype:"password",
            required: true,
            placeholder:"Repeat New Password"
        }

    ],
}