export default {
    setup: {
        new_form_id: 'new-leave-setup',
        info_form_id: 'leave-setup-info',
        title: "Leave Setup",
        layout_columns: 2,
        model: "Leave_Setup"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Days to be Allocated per Month ",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
        {
            id: "leave-type",
            fieldlabel: "Leave_Type",
            fieldname: "leave_type",
            fieldtype: "link",
            model:"Leave_Type",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
       
        {
            id: "carry-forward",
            fieldlabel: "Is Carry Forward",
            fieldname: "carry_forward",
            fieldtype: "check",
            columns: 1,
            required: false,
            hidden: false,
        },
        {
            id: "backdating",
            fieldlabel: "Allow Backdating of Leave Days",
            fieldname: "backdating",
            fieldtype: "check",
            columns: 1,
            required: false,
            hidden: false,
        },
    
       
        {
            id: "leave-recreation",
            fieldlabel: "Leave Allocations to be recreated if ended",
            fieldname: "leave_recreation",
            fieldtype: "check",
            columns: 1,
            required: false,
            hidden: false,
        },
     
      
    ],
}