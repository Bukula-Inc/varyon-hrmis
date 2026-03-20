export default {
    setup: {
        new_form_id: 'form',
        info_form_id: 'form',
        title: "Add Comment/Remark",
        layout_columns: 1,
        model: "Workflow Comment",
        action_type: "save"
    },
    fields: [
        { 
            id:"comment",
            fieldlabel:"Add Comment/Remark(Optional)",
            fieldname:"comment",
            fieldtype:"rich",
            height:300,
            required: false,
            placeholder:"Add Comment/Remark(Optional)"
        }
    ],
}