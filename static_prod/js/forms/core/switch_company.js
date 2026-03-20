let companies = []
$.each(lite.user.permitted_companies || [],(_,comp)=>companies.push(comp.company))
export default {
    setup: {
        new_form_id: 'switch-company',
        info_form_id: 'switch-company',
        title: "Switch Company",
        layout_columns: 1,
        model: "Switch Company",
        action_type: "save"
    },
    fields: [
        { 
            id:"company",
            fieldlabel:"Select Company",
            fieldname:"company",
            fieldtype:"select",
            options: companies,
            required: true,
            placeholder:"Select Company"
        },
        { 
            id:"comfirm-password",
            fieldlabel:"Confirm Your Password",
            fieldname:"confirm_password",
            fieldtype:"password",
            required: true,
            placeholder:"Confirm Your Password"
        }
    ],
}