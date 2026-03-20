export default {
    setup: {
        new_form_id: 'form',
        info_form_id: 'info',
        title: "Workflow Approver Group",
        layout_columns: 2,
        model: "Workflow_Approver_Group"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Workflow Approver Group Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Workflow Approver Group Name",
            required: true,
            hidden: false,
            description: "Workflow Approver Group Name",
        },
        {
            id: "minimum-total-approvers",
            fieldlabel: "Minimum Total Approvers",
            fieldname: "minimum_total_approvers",
            fieldtype: "int",
            columns: 1,
            placeholder: "Minimum Total Approvers",
            required: true,
            hidden: false,
            default: 1
        },
        {
            id: "sec",
            fieldlabel: "Approvers",
            fieldname: "apps",
            fieldtype: "section-break",
            columns: 1,
            placeholder: "Approvers",
            required: true,
            hidden: false,
            addborder:true
        },
        {
            id: "approvers",
            fieldlabel: "Approvers",
            fieldname: "approvers",
            fieldtype: "table",
            placeholder: "Workflow Approvers",
            required: true,
            hidden: false,
            description: "Add Aprovers to the group",
            fields:[
                {
                    id: "approver",
                    fieldlabel: "Approver(Role)",
                    fieldname: "approver",
                    fieldtype: "link",
                    model:"Role",
                    columns: 10,
                    placeholder: "Select Approver",
                    required: true,
                    hidden: false,
                },
                {
                    id: "should-always-be-present",
                    fieldlabel: "Should Always Be Present",
                    fieldname: "should_always_be_present",
                    fieldtype: "check",
                    columns: 2,
                    placeholder: "Should Always Be Present",
                    required: false,
                    hidden: false,
                },
            ]
        },
    ],
}