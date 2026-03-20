const ss = await lite.connect.get_system_settings()
export default {
    setup: {
        new_form_id: 'new-overtime-application',
        info_form_id: 'overtime-application-info',
        title: "Overtime Application",
        layout_columns: 3,
        model: "Overtime",
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_disable: false,
        allow_sending_mail: false,
    },
    fields: [
        {
            id: "applicant",
            fieldlabel: "Applicant",
            fieldname: "applicant",
            fieldtype: "read-only",
            addborder: true,
            columns: 1,
            required: true,
            hidden: false,
            default: lite.employee_info.name,
        },
         {
            id: "start_time",
            fieldlabel: "Start Time",
            fieldname: "start_time",
            fieldtype: "text",
            model: "Overtime",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            mode: "time"

           
        },
        {
            id: "end_time",
            fieldlabel: "End Time",
            fieldname: "end_time",
            fieldtype: "text",
            model: "Overtime",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            mode: "time"
          
        },
        {
            id: "total_earning",
            fieldlabel: "Total Earning",
            fieldname: "total_earning",
            fieldtype: "read-only",
            columns: 1,
            placeholder: "",
            required: false,
            hidden: false,
          
        },
        {
            id: "purpose",
            fieldlabel: "Purpose",
            fieldname: "purpose",
            fieldtype: "rich",
            columns: 3,
            height: 200,
            required: false,
            hidden: false,
            placeholder: " ",

        },
    
    ],
}