// ;
// const employee_info = await lite.connect.get_system_settings()

// export default {
//     setup: {
//         new_form_id: 'new-employee-resignation',
//         info_form_id: 'employee-resignation-info',
//         title: "Employee Seperation",
//         layout_columns: 3,
//        model: "Employee_Seperation",
//         allow_submit: true,
//         allow_cancel: true,
//         allow_delete: true,
//         allow_print: false,
//         allow_sending_mail: false,
//     },
//     fields: [
    
//         {
//             id: "employee",
//             fieldlabel: "Employee ",
//             fieldname: "employee",
//             fieldtype: "link",
//             model: "Employee",
//             columns: 1,
//             placeholder: "Employee",
//             required: true,
//             hidden: false,
//             default:lite?.employee_info?.name

//         },
    
//         {
//             id: "employee-name",
//             fieldlabel: "Employee Name",
//             fieldname: "name",
//             fieldtype: "text",
//             columns: 1,
//             placeholder: "Select Employee Name",
//             required: false,
//             hidden: false,
//             fetchfrom:"employee",
//             fetchfield: "full_name",
            
//         },
     
//         {
//             id: "department",
//             fieldlabel: "Department /  Unit",
//             fieldname: "department",
//             fieldtype: "read-only",
//             columns: 1,
//             placeholder: "Enter department",
//             required: false,
//             hidden: false,
//             fetchfrom:"employee",
//             fetchfield: "department"
//         },
//         {
//             id: "designation",
//             fieldlabel: "Job Title",
//             fieldname: "designation",
//             fieldtype: "read-only",
//             columns: 1,
//             placeholder: "Enter Job Title",
//             required: false,
//             hidden: false,
//             fetchfrom:"employee",
//             fetchfield: "designation"
//         },
//         {
//             id: "resignation-date",
//             fieldlabel: "Date of Resignation",
//             fieldname: "resignation_date",
//             fieldtype: "date",
//             columns: 1,
//             placeholder: " Enter Resignation Date",
//             required: true,
//             hidden: false,
//             value: lite.utils.today()
//         },
//         {
//             id: "reports-to",
//             fieldlabel: "Reports To",
//             fieldname: "reports_to",
//             fieldtype: "read-only",
//             columns: 1,
//             placeholder: "Reports To",
//             required: false,
//             hidden: false,
//             fetchfrom:"employee",
//             fetchfield: "report_to"
//         },
//         {
//             id: "notice-period",
//             fieldlabel: "Notice Period of last days of work",
//             fieldname: "notice_period",
//             fieldtype: "date",
//             columns: 1,
//             placeholder: " Enter Notice Period of last days of work",
//             required: true,
//             hidden: false,
//         },
//         {
//             id: "interview-summary",
//             fieldlabel: "Reason For Resignation",
//             fieldname: "interview_summary",
//             fieldtype: "rich",
//             height: 300,
//             columns: 3,
//             placeholder: "Reason For Resignation",
//             required: false,
//             hidden: false,
//         },
       
      
//     ],
// }