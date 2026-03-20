import {idlelize_job} from "../../overrides/form/controller/controller.js"
export default {
    setup: {
        new_form_id: 'new-tenant',
        info_form_id: 'tenant-info',
        title: "Module Group",
        layout_columns: 3,
        model: "Tenant"
    },
    form_actions: [
        // { 
        //     title: "Idlelize Job",
        //     icon: "zone_person_idle",
        //     icon_color: "orange",
        //     action: idlelize_job,
        //     for_docstatus: [0, 1]
        // }
    ],
    fields: [
        {
            id: "name",
            fieldlabel: "Tenant Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Tenant Name",
            required: true,
            hidden: false,
        },
        {
            id: "subscription_frequency",
            fieldlabel: "Subscription Frequency",
            fieldname: "subscription_frequency",
            fieldtype: "read-only",
            columns: 1,
            placeholder: "Subscription Frequency",
            required: true,
            hidden: false,
            default:"Annually"
        },
        {
            id: "tenant_url",
            fieldlabel: "Tenant URL",
            fieldname: "tenant_url",
            fieldtype: "read-only",
            columns: 1,
            placeholder: "Enter URL",
            required: true,
            hidden: false,
        },
        {
            id: "expiry_date",
            fieldlabel: "Expiry Date",
            fieldname: "expiry_date",
            fieldtype: "read-only",
            columns: 1,
            placeholder: "Expiry Date",
            required: true,
            hidden: false,
        },
        {
            id: "total_users",
            fieldlabel: "Total Users",
            fieldname: "total_users",
            fieldtype: "int",
            columns: 1,
            placeholder: "Total Users",
            required: true,
            hidden: false,
            default:"0"
        },
        {
            id: "total_storage",
            fieldlabel: "Total Storage",
            fieldname: "total_storage",
            fieldtype: "int",
            columns: 1,
            placeholder: "Total Storage",
            required: true,
            hidden: false,
            default:"0"
        },
        {
            id: "license_no",
            fieldlabel: "License Number",
            fieldname: "license_no",
            fieldtype: "read-only",
            columns: 3,
            placeholder: "License Number",
            required: false,
            hidden: false,
            default:"0"
        },
        {
            id: "modules",
            fieldlabel: "Subscription Modules",
            fieldname: "modules",
            fieldtype: "table",
            model:"Tenant_Module_Pricing",
            placeholder: "Add Modules",
            required: true,
            hidden: false,
            addemptyrow:false,
            fields:[
                {
                    id: "module_price",
                    fieldlabel: "Module Priceing",
                    fieldname: "module_price",
                    fieldtype: "link",
                    model:"Module_Pricing",
                    columns: 10,
                    placeholder: "Select Module",
                    required: true,
                    hidden: false,
                },
                {
                    id: "module",
                    fieldlabel: "Module",
                    fieldname: "module",
                    fieldtype: "link",
                    model:"Module",
                    columns: 10,
                    placeholder: "Select Module",
                    required: true,
                    hidden: false,
                },
                {
                    id: "is_suspended",
                    fieldlabel: "Is Suspended",
                    fieldname: "is_suspended",
                    fieldtype: "check",
                    columns: 2,
                    placeholder: "Is Suspended",
                    false: true,
                    hidden: false,
                },
            ]
        },
    ]
}