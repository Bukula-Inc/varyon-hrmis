export default class Core_Hr {
    constructor() {
        this.has_initialized = false;
        this.init();
    }

    async init() {
        try {
            const { status, data, error_message } = await lite.connect.x_fetch("get_appraisal_content");
            this.has_initialized = true;
            if (status !== lite.status_codes.ok) {
                lite.alerts.toast({ toast_type: status, title: "Something went wrong", message: error_message });
                return false;
            } else {
            
                lite.appraisal_content = data;
                return lite.appraisal_content;
            }
        } catch (error) {
            console.error("Initialization error:", error);
            lite.alerts.toast({ toast_type: "error", title: "Something went wrong", message: "Failed to fetch appraisal content." });
            return false;
        }
    }

    async get_opened_document () {
        const doc_id = lite.utils.get_url_parameters("doc")
        if (doc_id) {

            const {status,data,error_message} = await lite.connect.get_doc("Appraisal",doc_id)
            if (status === lite.status_codes.ok) {
                return data
            }
        } 
        return false
    }

    async get_self_appraisal_opened_document () {
        const doc_id = lite.utils.get_url_parameters("doc")
        if (doc_id) {

            const {status,data,error_message} = await lite.connect.get_doc("Self_Appraisal",doc_id)
            if (status === lite.status_codes.ok) {
                return data
            }
        } 
        return false
    }

    // Extend appraisal fields
    async extend_appraisal_fields(fields) {
        const appraisal_fields = [];
        const open_ended = lite.appraisal_content?.openqs || [];
        const closed_ended = lite.appraisal_content?.closedqs || [];
        const closed_ended_options = lite.utils.get_object_keys(lite.appraisal_content?.closedqs_options || []);  
        let openq = {}  
        let closedq = {} 
        const doc = await this.get_opened_document()
        if(doc){
            $.each(doc.open_ended_questions,(_,oeq)=>{
                openq[lite.utils.get_object_keys(oeq)[0]] = lite.utils.get_object_values(oeq)[0]
            })
            $.each(doc.closed_ended_questions,(_,ceq)=>{
                closedq[lite.utils.get_object_keys(ceq)[0]] = lite.utils.get_object_values(ceq)[0]
            })
        }
       
        appraisal_fields.push({
            id: "closed-ended-questions",
            fieldlabel: "Closed Ended Questions",
            fieldname: "closed_ended_questions",
            fieldtype: "section-break",
            addborder: true,
        });

        $.each(lite.utils.get_object_values(closed_ended), (_, comp) => {
            appraisal_fields.push({
                id: comp.name,
                fieldlabel: comp.name,
                fieldname: comp.name,
                fieldtype: "select",
                columns: 2,
                required: true,
                hidden: false,
                placeholder: "Select your answer",
                options:closed_ended_options,
                default:  closedq[comp.name]
            });
        });

        appraisal_fields.push({
            id: "open-ended-questions",
            fieldlabel: "Open Ended Questions",
            fieldname: "open_ended_questions",
            fieldtype: "section-break",
            addborder: true,
        });


        $.each(lite.utils.get_object_values(open_ended), (_, comp) => {
            appraisal_fields.push({
                id: comp.name,
                fieldlabel: comp.name,
                fieldname: comp.name,
                fieldtype: "longtext",
                classnames: "h-[90px] p-2",
                columns: 2,
                required: true,
                hidden: false,
                placeholder: "Type your answear" ,
                default: openq[comp.name]
            });
        });

        return fields.concat(appraisal_fields);
    }

    async extend_self_appraisal_fields(fields) {
        const appraisal_fields = [];
        const open_ended = lite.appraisal_content?.openqs || [];
        const closed_ended = lite.appraisal_content?.closedqs || [];
        const closed_ended_options = lite.utils.get_object_keys(lite.appraisal_content?.closedqs_options || []);  
        let openq = {}  
        let closedq = {} 
        const doc = await this.get_self_appraisal_opened_document()
        if(doc){
            $.each(doc.open_ended_questions,(_,oeq)=>{
                openq[lite.utils.get_object_keys(oeq)[0]] = lite.utils.get_object_values(oeq)[0]
            })
            $.each(doc.closed_ended_questions,(_,ceq)=>{
                closedq[lite.utils.get_object_keys(ceq)[0]] = lite.utils.get_object_values(ceq)[0]
            })
        }
       
        appraisal_fields.push({
            id: "closed-ended-questions",
            fieldlabel: "Closed Ended Questions",
            fieldname: "closed_ended_questions",
            fieldtype: "section-break",
            addborder: true,
        });

        $.each(lite.utils.get_object_values(closed_ended), (_, comp) => {
            appraisal_fields.push({
                id: comp.name,
                fieldlabel: comp.name,
                fieldname: comp.name,
                fieldtype: "select",
                columns: 2,
                required: true,
                hidden: false,
                placeholder: "Select your answer",
                options:closed_ended_options,
                default:  closedq[comp.name]
            });
        });

        appraisal_fields.push({
            id: "open-ended-questions",
            fieldlabel: "Open Ended Questions",
            fieldname: "open_ended_questions",
            fieldtype: "section-break",
            addborder: true,
        });


        $.each(lite.utils.get_object_values(open_ended), (_, comp) => {
            appraisal_fields.push({
                id: comp.name,
                fieldlabel: comp.name,
                fieldname: comp.name,
                fieldtype: "longtext",
                classnames: "h-[90px] p-2",
                columns: 2,
                required: true,
                hidden: false,
                placeholder: "Type your answear" ,
                default: openq[comp.name]
            });
        });

        return fields.concat(appraisal_fields);
    }
}
