export default {
    setup: {
        model: 'Acting_Appointment_Memo',
        list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Acting_Appointment',
            columns: 1,
            placeholder: "Select Appointment",
        },
     
        {
            id: "position-owner-filter",
            fieldname: "position_owner",
            fieldtype: "link",
            model: 'Employee',
            columns: 1,
            placeholder: "Select Employee ID",
        },
        {
            id: "acting-officer",
            fieldname: "acting_officer",
            fieldtype: "link",
            model: 'Employee',
            columns: 1,
            placeholder: "Select Officer",
        },
        
      
    ],
    actions: {
        
    },
    columns: [
        {
            column_title: "Position Owner",
            column_name: "position_owner",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Acting Officer",
            column_name: "acting_officer",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Job Title",
            column_name: "job_title",
            column_type: "text",
            columns: 1,
        },
      
    ]
}