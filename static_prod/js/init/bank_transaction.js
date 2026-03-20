export default class Bank_Transaction_Actions{
    constructor(){
        this.current_record = {}
        this.init()
                    
        this.actions = {
            submit: this.submit_transactions,
            delete: this.delete_transactions,
            reverse: this.reverse_transactions,
            "audit trail": this.audit_trail_transactions,
            "workflow comments": this.workflow_comments_transactions,
        }
    }

    async submit_transactions(id, row, cls){
        const {status, data, error_message} = await lite.connect.submit_doc({ model:"Bank_Transaction", doc_id:[id]})
        if(status === lite.status_codes.ok){
            cls.current_record.status = "Submitted"
            cls.current_record.docstatus = 1
            const updated_row = lite.bank_transactions_controller.create_bank_entry_row(lite.bank_transactions_controller.transaction_statuses.submitted,cls.current_record,false)
            $(row)?.replaceWith(updated_row)
        }
    }

    async delete_transactions(id, row, cls){
        if(id){
            const {status} = await lite.connect.delete_docs({model: "Bank_Transaction", docs:[id]})
            if(status == lite.status_codes.ok){
                lite.alerts.toast({
                    toast_type:lite.status_codes.ok,
                    title:"Deleted Successfully",
                    message:"Transaction deleted successfully",
                })
                $(row)?.remove()
            }
        }
    }

    async reverse_transactions(id, row, cls){
        if(id){
            const reverse_loader = lite.alerts.loading_toast({title:"Reversing Transaction",message:"Please wait while the transaction gets reversed"})
            const {status, data, error_message} = await lite.connect.x_post("reverse_bank_transaction", {tid:id})
            lite.alerts.destroy_toast(reverse_loader)
            if(status === lite.status_codes.ok){
                cls.current_record.status = "Reversed"
                cls.current_record.docstatus = 2
                const updated_row = lite.bank_transactions_controller.create_bank_entry_row(lite.bank_transactions_controller.transaction_statuses.cancelled,cls.current_record,false)
                $(row)?.replaceWith(updated_row)
            }
        }

    }

    async audit_trail_transactions(id){

    }

    async workflow_comments_transactions(id, row, cls){
        $("#bank-transactions-form")?.find(".comments-wrapper")?.remove()
        $("#bank-transactions-form")?.append(lite.html_generator.create_workflow_comment_content(cls.current_record))
        $(".comments-wrapper").removeClass("hidden")
        $(".close-comments-btn")?.off("click")?.click(e=>$(".comments-wrapper")?.remove())
    }


    generate_action_loader_html(){
        return `
            <div class='w-full min-h-[100px] flex flex-col items-center justify-center'>
                ${lite.utils.generate_loader({loader_type:"spin", size:30, light_mode:false})}
                <span class="mt-5">Determining available Actions</span>
            </div>
        `
    }
    generate_action_html(doc_id, action, stage_no, icon="check_box_outline_blank", outline_color="#f00000", inner_color, is_workflow=false){
        return `
         <li for="${doc_id}" stage="${stage_no}" action="${action}" class="${is_workflow ? "bank-transaction-wf-action-item" : "bank-transaction-dir-action-item"} transition duration-[1000] mb-2 min-w-full hover:bg-[${lite.utils.adjust_hex_color_intensity(outline_color, 30)}] rounded-md intro-x bg-[${lite.utils.adjust_hex_color_intensity(outline_color, 80)}]" for="${action}">
            <a  href="javascript:;" class=" w-full w-[max-content] py-2 px-1 flex items-center justify-start max-w-[400px] text-[${inner_color}]"> 
                <span class="material-symbols-outlined mr-1 text-16">${icon}</span> ${action}
            </a>
        </li>
        `
    }

    init(){
        $(document).on("click", '.bank-transaction-action-btn', async (e) => {
            const id = $(e.currentTarget)?.attr("id")
            $(`#bank-transaction-options-${id}`)?.html(this.generate_action_loader_html())
            const {status, data, error_message} = await lite.connect.get_doc("Bank_Transaction", id)
            if(status == lite.status_codes.ok){
                this.current_record = data
                const workflow = data.workflow
                let options = ""
                $(`#bank-transaction-options-${id}`)?.empty()
                if(workflow && lite.utils.array_has_data(workflow?.available_actions)){
                    $.each(workflow.available_actions,(idx,wfa)=>{
                        options += this.generate_action_html(data.id, wfa.action, wfa.stage_no, wfa.icon, wfa.color, wfa.color,true)
                    })
                }
                else{
                    if (!workflow?.has_workflow){
                        if(data.docstatus === 0 && data.status == "Draft"){
                            options += `
                                ${this.generate_action_html(data.id, "Submit", 0, "select_check_box", "#1f3bcc", "#1f3bcc", false)}
                                ${this.generate_action_html(data.id, "Delete", 0, "delete", "#f00004", "#f00004", false)}
                            `
                        }
                        else if(data.docstatus === 1){
                            options += `
                                ${this.generate_action_html(data.id, "Reverse", 0, "undo", "#171a6e", "#171a6e", false)}
                            `
                        }
                    }
                }
                if(workflow?.has_workflow){
                    options += `${this.generate_action_html(data.id, "Workflow Comments", 0, "comment", "#039979", "#039979", false)}`
                }
                // options += `${this.generate_action_html(data.id, "Audit Trail", 0, "clear_all", "#7a0382", "#7a0382", false)}`
                $(`#bank-transaction-options-${id}`).html(options)
            }
        })

        // for direct actions where wf is applicable
        $(document).on("click", '.bank-transaction-wf-action-item', async (e) => {
            const 
                id = $(e.currentTarget)?.attr("for"),
                action = $(e.currentTarget)?.attr("action"),
                stage_no = $(e.currentTarget)?.attr("stage"),
                row = $(`.bank-transaction-row[value-id=${id}]`)
            
            const quick_modal = await lite.modals.quick_form("core", "workflow comment",{text:"Proceed", fun: async (values, setup)=>{
                if (!id || !stage_no) {
                    lite.alerts.toast({
                        toast_type: lite.status_codes.unprocessable_entity,
                        title: `Update Failed!`,
                        message: `Document ID/Stage no missing!`,
                    })
                } else {
                    lite.connect.workflow_action({
                        model: "Bank_Transaction",
                        values: [id],
                        stage_no:stage_no,
                        comment: values.comment || "",
                        action: action
                    }).then(resolve => {
                        if (resolve?.status === lite.status_codes.ok) {
                            lite.modals.close_modal(quick_modal.modal_id)
                            lite.alerts.toast({
                                toast_type: resolve.status,
                                title: `Updated ${lite.utils.replace_chars("Bank_Transaction", "_", " ")}`,
                                message: `Transaction updated successfully!`,
                            })
                            $(`#bank-transaction-options-${id}`)?.empty()

                            // update bank transactoin row
                            const updated_row = lite.bank_transactions_controller.create_bank_entry_row(lite.bank_transactions_controller.transaction_statuses.submitted,resolve.data,false)
                            $(row)?.replaceWith(updated_row)
                        }
                    })            
                }
            }})
        })

        // for direct actions where wf is none applicable, and the rest audit trail and workflow comments
        $(document).on("click", '.bank-transaction-dir-action-item', async (e) => {
            e.preventDefault()
            const 
                id = $(e.currentTarget)?.attr("for"),
                action = $(e.currentTarget)?.attr("action"),
                row = $(`.bank-transaction-row[value-id=${id}]`)
                if(action){
                    this.actions[lite.utils.lower_case(action)](id, row, this)
                }
            
        })
    }
}