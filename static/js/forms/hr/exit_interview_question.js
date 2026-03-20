// import { } from "../../overrides/form/hr/core.js"
console.log(lite);

export default {
    setup: {
        new_form_id: 'new-exit-interview-question',
        info_form_id: 'exit-interview-question-info',
        title: "Exit Interview Question",
        layout_columns: 6,
        model: "Exit_Interview_Question",
        allow_submit: false,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
    },
    form_actions: [
        // {
        //     title: "Generate Final Statement",
        //     icon: "content_copy",
        //     icon_color: "indigo",
        //     action: generate_final_statement,
        //     for_docstatus: [1],
        //     at_index: 1,
        // },
    
    ],
    fields: [
        {
            id: "name",
            fieldlabel: "Question Collection",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            default: lite?.user?.default_company || lite?.user?.company?.name || "",   
        },
        {
            id: "section-break-001",
            fieldlabel: " ",
            fieldtype: "section-break"
        },
        {
            id: "open-ended-questions",
            fieldlabel: "Open Ended Questions",
            fieldname: "open_ended_questions",
            model: "Open_Ended_Exit_Question",
            columns: 3,
            fieldtype: "table",
            required: false,
            hidden: false,
            description: "Questions with open/descriptive answers",
            fields: [
                {
                    id: "question",
                    fieldlabel: "Question",
                    fieldname: "question",
                    fieldtype: "text",
                    columns: 10,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    istablefield: true,
                },   
            ] 
        }, 
        {
            id: "closed-ended-questions",
            fieldlabel: "Closed Ended Questions",
            fieldname: "closed_ended_questions",
            model: "Closed_Ended_Exit_Question",
            columns: 3,
            fieldtype: "table",
            required: false,
            hidden: false,
            description: "Questions with ether 'No' or 'Yes' answers only",
            fields: [
                {
                    id: "question",
                    fieldlabel: "Question",
                    fieldname: "question",
                    fieldtype: "text",
                    columns: 10,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    istablefield: true,
                },   
            ] 
        },            
      
    ],
}