import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Advance Report',
        title: "Advance Report",
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
            id: "employee",
            column_title: "Applicant",
            fieldname: "employee",
            fieldtype: "link",
            model: "Employee",
            placeholder: "Select Applicant",
        },  
        {
            id: "cleared",
            column_title: "Status",
            fieldname: "cleared",
            fieldtype: "select",
            options: ["Open", "Closed"],
            placeholder: "Select Status",
        },  
    ],
    actions: [
      {
            fun: wipe_all_transactions,
            title: 'Get JSON',
            icon: 'code',
            icon_color: 'orange',
        },
    ],

    columns: [
        {
            column_title: "From Date",
            column_name: "effective_date",
            column_type: "date",
            width: 200,
        },
        {
            column_title: "End Date",
            column_name: "last_payment_date",
            column_type: "date",
            width: 200,
        },
        {
            column_title: "Applicant",
            column_name: "applicant",
            column_type: "link",
            width: 200,
        },
        {
            column_title: "Advance Type",
            column_name: "advance_type",
            width: 350,
        },
        {
            column_title: "Reference",
            column_name: "reference",
            column_type: "link",
            width: 350,
        },
        {
            column_title: "Principal Amount",
            column_name: "amount",
            width: 200,
            is_figure: true,
            apply_formatter_on_total:true,
            formatter: (value)=>{
                return lite.utils.currency(value,"ZMW","ZMW")
            }
        },
        {
            column_title: "Settlement Status",
            column_name: "is_paid",
            width: 350,
        },
        {
            column_title: "Payment Method",
            column_name: "repayment_method",
            width: 200,
        },
        {
            column_title: "Remaining Period (Months)",
            column_name: "remaining_months",
            width: 200,
        },
      
        {
            column_title: "Paid Amount",
            column_name: "paid_amount",
            is_figure: true,
            width: 200,
            apply_formatter_on_total:true,
            formatter: (value)=>{
                return lite.utils.currency(value,"ZMW","ZMW")
            }
        },
        {
            column_title: "Last Payment Made",
            column_name: "recently_settled_amount",
            width: 200,
            is_figure: true,
            apply_formatter_on_total:true,
            formatter: (value)=>{
                return lite.utils.currency(value,"ZMW","ZMW")
            }
        },
    
        {
            column_title: "Outstanding Balance",
            column_name: "balance",
            is_figure: true,
            width: 200,
            apply_formatter_on_total:true,
            formatter: (value)=>{
                console.log('====================================');
                console.log(value);
                console.log('====================================');
                return lite.utils.currency(value,"ZMW","ZMW")
            }
        },
    ]
}