export default {
    setup: {
        model: 'sickness absence',
        title: "Sickness Absence Report",
        report_type: "script",
        include_opening: true,
        include_closing: true,
        allow_print: true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true
    },
    filters: [
        {
            id: "department",
            fieldname: "department",
            fieldtype: "link",
            model: 'Department',
            placeholder: "Select Department",
        },
    ],
  
    actions: [],
    columns: [
        {
            column_title: "Employee Name",
            column_name: "employee_name",
            column_type: "text",
            width: 450,
        },
        {
            column_title: "Leave",
            column_name: "leave_type",
            column_type: "text",
            width: 450, 
        },
        {
            column_title: "From",
            column_name: "from_date",
            column_type: "text",
            width: 450, 
        },
        {
            column_title: "Sickness/Illness",
            column_name: "reason",
            column_type: "text",
            width: 450,
        },
    ]
}
