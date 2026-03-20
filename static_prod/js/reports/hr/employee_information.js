export default {
    setup: {
        model: 'Employee Information',
        title: "Employee Information",
        report_type: "script",
        include_opening: true,
        include_closing: true,
        allow_print: true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true,
        is_grid_layout : false,
    },
    filters: [
     
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Employee',
            linkfield: "name",
            width: 1,
            placeholder: "Employee ID",
        },
        {
            id: "department",
            fieldname: "department",
            fieldtype: "link",
            model: 'Department',
            placeholder: "Department",
        },
        {
            id: "designation",
            fieldname: "designation",
            fieldtype: "link",
            model: 'Designation',
            placeholder: "Designation",
        },
        {
            id: "status",
            fieldname: "status",
            fieldtype: "link",
            model: "Doc_Status",
            linkfield: "status",
            placeholder: "Status",
        },
      
    ],
    actions: [],
    columns: [
        {
            column_title: "Employee No",
            column_name: "name",
            column_type: "link",
            model:"Employee",
            width: 200,
            classname: "text-left"
        },
        {
            column_title: "Employee First Name",
            column_name: "first_name",
            column_type: "text",
            width: 170,
        },
        {
            column_title: "Employee Last Name",
            column_name: "last_name",
            column_type: "text",
            width: 170,
        },
        {
            column_title: "Employee Other Names",
            column_name: "middle_name",
            column_type: "text",
            width: 170,
        },
        {
            column_title: "Gender ",
            column_name: "gender",
            column_type: "link",
            width: 100,
        },
        {
            column_title: "D.O.B",
            column_name: "d_o_b",
            column_type: "text",
            width: 100,
        },
        {
            column_title: "Date Of Joining",
            column_name: "date_of_joining",
            column_type: "text",
            width: 150,
        },

        {
            column_title: "Email Address",
            column_name: "email",
            column_type: "text",
            width: 230,
        },
        {
            column_title: "Contact No ",
            column_name: "contact",
            column_type: "text",
            width: 180,
        },
        {
            column_title: "Department",
            column_name: "department",
            column_type: "link",
            model: 'Department',
            width: 200,
        },
        {
            column_title: "Job Title",
            column_name: "designation",
            column_type: "link",
            model: 'Designation',
            width: 200,
        },
        {
            column_title: "ID/Passport ",
            column_name: "id_no",
            column_type: "text",
            width: 170,
        },
        {
            column_title: "SSN ",
            column_name: "napsa",
            column_type: "text",
            width: 170,
        },

        {
            column_title: "NHIMA No ",
            column_name: "nhima",
            column_type: "text",
            width: 170,
        },
        {
            column_title: "TPin",
            column_name: "tpin",
            column_type: "text",
            width: 350,
        },
        {
            column_title: "Working Days ",
            column_name: "working_days",
            column_type: "text",
            width: 100,
        },

        {
            column_title: "Working Hours ",
            column_name: "working_hours",
            column_type: "text",
            width: 100,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            width: 170,
        },
    ]
}