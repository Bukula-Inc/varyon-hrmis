import { organization, individual } from "../forms/web/kyc.js"
import Web_HTML_Generator from "../page/html/web_html_generator.js"
import HTML_Builder from "../page/html/html_builder.js"
export default class Onboarding{
    constructor(){
        this.web_builder = new Web_HTML_Generator()
        this.html_generator = new HTML_Builder()
        this.forms = { organization: organization.fields, individual: individual.fields}
        this.taxes = {}
        this.modules = {}
        this.selected = []
        this.overall_totals = {}
        this.current_stage = 1
        this.freq = 1
        this.disc_rt = 0
        this.freq_in_word = "Monthly"
        this.$module_group_wrapper = $(".module-group-wrapper")
        this.$annual_discount = $(".annual-discount")
        this.$steps_wrapper = $("#steps-wrapper")

        this.$selected_module_list = $(".selected-module-list")
        this.$cost_per_user = $(".cost-per-user")
        this.$free_users = $(".free-users")
        this.$add_remove_user_btn = $(".add-remove-user-btn")
        this.$add_remove_user_input = $(".add-remove-user-input")
        this.$cost_per_user = $(".cost-per-user")
        this.$free_storage = $(".free-storage")
        this.$cost_per_storage = $(".cost-per-storage")
        this.$add_remove_storage_btn = $(".add-remove-storage-btn")
        this.$add_remove_storage_input = $(".add-remove-storage-input")

        this.$total_additional_user = $(".total-additional-users")
        this.$total_additional_storage = $(".total-additional-storage")
        this.$total_freq = $(".total-freq")
        this.$xclusive_amount = $(".exclusive-amount")
        this.$modules_xclusive_amount = $(".modules-exclusive-amount")
        this.$discount_amount = $(".discount-amount")
        this.$tax_amount = $(".tax-amount")
        this.$inclusive_amount = $(".inclusive-amount")

        this.totals = {
            freq:"",
            additional_users:{ qty:0, exclusive:0, tax_amount:0, inclusive:0 },
            additional_storage:{ qty:0, exclusive:0, tax_amount:0, inclusive:0 },
            modules:{},
            exclusive_amount:0,
            discount_amount:0,
            tax_amount:0,
            inclusive_amount:0

        }

       
        this.$kyc_fields_wrapper = $("#kyc-fields-wrapper")
        this.registration_type = "individual"

        this.$license_content = $("#license-content")
        this.$agree_to_license = $("#license-agreement")

        this.$submission_wrapper = $(".submission-wrapper")
        this.$submission_loader_wrapper = $(".submission-loader-wrapper")
        this.$success_wrapper = $(".success-wrapper")
        this.$failed_wrapper = $(".failed-wrapper")
    }

    init(data){
        this.data = data
        if(lite.utils.object_has_data(this.data)){
            this.module_group = lite.utils.ascend(this.data.module_group,"id")
            this.license = this.data.license
            this.billing_config = this.data.billing_config
            this.taxes = this.data.taxes
        }
        // initialize module selection
        this.init_module_selection()
        this.populate_defaults()
        this.populate_module_groups()
        this.init_freq_toggler()
        this.init_back_forward_actions()
        this.init_registration_type_actions()
    }

    populate_defaults(){
        this.$annual_discount.html(this.billing_config?.annual_discount)
        this.$free_users.html(this.billing_config?.total_free_users)
        this.$cost_per_user.html(lite.utils.currency(this.billing_config?.cost_per_additional_user || 0 * this.freq,1, this.billing_config.billing_currency))
        this.$free_storage.html(this.billing_config?.total_free_storage || 0)
        this.$cost_per_storage.html(lite.utils.currency(this.billing_config?.cost_per_additional_storage || 0 * this.freq,1, this.billing_config.billing_currency))
    }

    populate_module_groups(){
        if(lite.utils.array_has_data(this.module_group)){
            let content = ""
            $.each(this.module_group,(_,mg)=>{
                this.overall_totals[mg.name] = 0
                if(lite.utils.array_has_data(mg.modules)){
                    Object.assign(this.modules,lite.utils.array_to_object(mg.modules,"name"))
                    content += this.web_builder.create_module_group(mg,this.billing_config,_, this.freq_in_word)
                }
            })
            this.$module_group_wrapper?.html(content)
        }
    }


    init_module_selection(){
        $(document).on('click', '.add-remove-module-btn', e=> {
            const el = $(e.currentTarget), module_name = lite.utils.get_attribute(el,"module")
            const btn_el = $(`button.add-remove-module-btn[module="${module_name}"`)
            this.add_or_remove_module_selection(module_name)
            if(!btn_el?.hasClass("added")){
                btn_el.addClass("added bg-secondary_color")?.removeClass("bg-default")
                btn_el.find(".group-add-icon").html("cancel")
                btn_el.find(".add-remove-text").text("Remove")
            }
            else{
                btn_el.addClass("bg-default")?.removeClass("added bg-secondary_color")
                btn_el.find(".group-add-icon").html("add_task")
                btn_el.find(".add-remove-text").text("Add")
                $(`button.remove-module[module="${module_name}"`)?.parents(".selected-module-card")?.remove()
            }
            if(lite.utils.is_empty_array(this.selected)){
                $('.prev-next-action-btn[action="prev"]')?.trigger("click")
            }
        });
    }


    add_or_remove_module_selection(module_name){
        const selected_module = this.modules[module_name], group = selected_module?.module_group
        if(this.selected.includes(module_name)){
            this.selected = this.selected?.filter(mdl => mdl !== module_name)
            this.overall_totals[group] -= selected_module?.total_cost || 0
        }
        else{
            this.selected.push(module_name)
            this.overall_totals[group] += selected_module?.total_cost || 0
        }
        $(`.module-group[group-name="${group}"]`)?.find(".group-total").html(lite.utils.thousand_separator(this.overall_totals[group] * this.freq,2))
        this.calculate_totals()
    }


    // enable frequency toggler
    init_freq_toggler(){
        $(document).on('click', '.freq-toggler', e=> {
            const el = $(e.currentTarget)
            const freq = lite.utils.string_to_int(lite.utils.get_attribute(el,"freq")) || 1
            this.freq = freq === 1 ? 12 : 1
            this.freq_in_word = this.freq === 1 ? "Monthly" : "Annually"
            this.freq == 1 ? el.removeClass("float-right")?.addClass("float-left") : el.addClass("float-right")?.removeClass("float-left")
            el.attr("freq", this.freq)
            $(".group-frequency")?.html(this.freq_in_word)
            $.each(lite.utils.get_object_keys(this.overall_totals),(_,k)=>{$(`.module-group[group-name="${k}"]`)?.find(".group-total").html(lite.utils.thousand_separator(this.overall_totals[k]* this.freq,2))})
            $.each(lite.utils.get_object_keys(this.modules),(_,k)=>{
                $(`.module-cost[module="${k}"]`)?.html(lite.utils.currency(this.modules[k]?.total_cost * this.freq,2,this.billing_config?.billing_currency || "ZMW"))
            })
            this.calculate_totals()
        });
    }


    // enable next and back clicks
    init_back_forward_actions(){
        $(document).on("click",".prev-next-action-btn", async e=>{
            const el = $(e.currentTarget), action = el.attr("action")
            if(action == "next"){
                $('.prev-next-action-btn[action="prev"]')?.prop("disabled",false)
                if(this.current_stage === 1){
                    if(lite.utils.is_empty_object(this.selected)){
                        lite.alerts.toast({
                            toast_type:lite.status_codes.forbidden,
                            title:"Module Selection Required",
                            message:"Please select at least one module to proceed to the next stage!"
                        })
                    }
                    else{
                        this.current_stage += 1
                    }
                }
                else if(this.current_stage === 2){
                    this.current_stage += 1
                    this.init_kyc()
                }
                else if(this.current_stage == 3){
                    await this.get_form_data() ? this.current_stage += 1 : ""
                }
                else if(this.current_stage < 4){
                    this.current_stage += 1
                }
                if(this.current_stage ===4){
                    this.init_licensing()
                    if(!this.$agree_to_license.prop("checked")){
                        el.prop("disabled",true)
                    }
                    else{
                        this.current_stage += 1
                    }
                }
                if(this.current_stage ===5){
                    el.parent("div")?.addClass("hidden")
                    const {status, data, error_message} = await this.submit_kyc()
                    console.log(status)
                    this.$submission_wrapper.addClass("hidden")
                    if(status === lite.status_codes?.ok){
                        this.$success_wrapper.removeClass("hidden")
                    }
                    else{
                        this.$failed_wrapper.removeClass("hidden")
                    }
                }
                
                this.$steps_wrapper.find(`.step[step="${this.current_stage}"]`)?.addClass("bg-default text-theme_text_color")
                .removeClass("bg-gray-300")?.find(".icon-wrapper")
                .addClass("bg-white text-default").removeClass("bg-default text-theme_text_color")
            }
            else{
                if(this.current_stage > 1)
                this.$steps_wrapper.find(`.step[step="${this.current_stage}"]`)?.removeClass("bg-default text-theme_text_color").addClass("bg-gray-300")?.find(".icon-wrapper")
                    .removeClass("bg-white text-default").addClass("bg-default text-theme_text_color")
                    this.current_stage -= 1
                $('.prev-next-action-btn[action="next"]')?.prop("disabled",false)
            }
            if(this.current_stage <= 1){
                el.prop("disabled",true)
            }
            this.update_current_page()
        })
    }

    // update current page
    update_current_page(){
        $(".stage-content").addClass("hidden")
        $(`.stage-content[stage="${this.current_stage}"]`).removeClass("hidden")

        // populate selected modules
        if(this.current_stage === 2){
            let selected_modules = ""
            $.each(this.selected,(_,mdl)=>{
                selected_modules += this.web_builder.create_selected_module_card(this.modules[mdl],this.billing_config,this.freq)
            })
            this.$selected_module_list.html(selected_modules)


            // enable additional user actions
            this.$add_remove_user_btn?.off("click")?.click(e=>{
                const el = $(e.currentTarget), action = lite.utils.get_attribute(el,"action")
                let current_val = lite.utils.string_to_float(this.$add_remove_user_input.val()) || 0
                if(action === "add"){
                    current_val += 1
                }
                else if(current_val > 0){
                    current_val -= 1
                }
                this.$add_remove_user_input.val(current_val)
                this.$add_remove_user_input.trigger("change")
            })
            this.$add_remove_user_input?.off("change")?.change(e=>{
                this.calculate_totals()
            })


            // enable additional user actions
            this.$add_remove_storage_btn?.off("click")?.click(e=>{
                const el = $(e.currentTarget), action = lite.utils.get_attribute(el,"action")
                let current_val = lite.utils.string_to_float(this.$add_remove_storage_input.val()) || 0
                if(action === "add"){
                    current_val += 1
                }
                else if(current_val > 0){
                    current_val -= 1
                }
                this.$add_remove_storage_input.val(current_val)
                this.$add_remove_storage_input.trigger("change")
            })
            this.$add_remove_storage_input?.off("change")?.change(e=>{
                this.calculate_totals()
            })
        }
    }


    // calculate_totals

    calculate_additional_users(){
        const additional_user_item = this.billing_config.additional_user_item
        this.totals.additional_users.qty = lite.utils.string_to_int(this.$add_remove_user_input?.val()) || 0
        if(this.totals.additional_users.qty == 0){
            this.totals.additional_users.qty = 0
            this.totals.additional_users.exclusive = 0
            this.totals.additional_users.tax_amount = 0
            this.totals.additional_users.inclusive = 0
        }
        else{
            this.totals.additional_users.exclusive = (this.billing_config?.cost_per_additional_user * this.totals.additional_users.qty) * this.freq
            const tax_type = this.taxes[additional_user_item.tax_type]
            if(lite.utils.array_has_data(tax_type.tax_accounts)){
                $.each(tax_type.tax_accounts, (_, tax)=>{
                    if(tax.tax_rate){
                        this.totals.additional_users.tax_amount += (this.totals.additional_users.exclusive * tax.tax_rate) / 100
                    }
                })
            }
            this.totals.additional_users.tax_amount = lite.utils.fixed_decimals(this.totals.additional_users.tax_amount, 2)
            this.totals.additional_users.inclusive = this.totals.additional_users.exclusive + this.totals.additional_users.tax_amount
        }
    }

    calculate_additional_storage(){
        const additional_storage_item = this.billing_config.additional_storage_item
        this.totals.additional_storage.qty = lite.utils.string_to_int(this.$add_remove_storage_input?.val()) || 0
        if(this.totals.additional_storage.qty == 0){
            this.totals.additional_storage.qty = 0
            this.totals.additional_storage.exclusive = 0
            this.totals.additional_storage.tax_amount = 0
            this.totals.additional_storage.inclusive = 0
        }
        else{
            this.totals.additional_storage.exclusive = (this.billing_config?.cost_per_additional_storage * this.totals.additional_storage.qty) * this.freq
            const tax_type = this.taxes[additional_storage_item.tax_type]
            if(lite.utils.array_has_data(tax_type.tax_accounts)){
                $.each(tax_type.tax_accounts, (_, tax)=>{
                    if(tax.tax_rate){
                        this.totals.additional_storage.tax_amount += (this.totals.additional_storage.exclusive * tax.tax_rate) / 100
                    }
                })
            }
            this.totals.additional_storage.tax_amount = lite.utils.fixed_decimals(this.totals.additional_storage.tax_amount, 2)
            this.totals.additional_storage.inclusive = this.totals.additional_storage.exclusive + this.totals.additional_storage.tax_amount
        }
    }


    calculate_module_totals(mdl){
        this.totals.modules[mdl.name] = { qty:1, exclusive:0, tax_amount:0, inclusive:0 }
        const module_item = mdl.item
        console.log(mdl)
        this.totals.modules[mdl.name].exclusive = mdl.total_cost * this.freq
        this.totals.modules[mdl.name].discount_amount = lite.utils.fixed_decimals((this.totals.modules[mdl.name].exclusive * this.disc_rt) / 100)
        this.totals.modules[mdl.name].discounted_amount = this.totals.modules[mdl.name].exclusive - this.totals.modules[mdl.name].discount_amount
        
        const tax_type = this.taxes[module_item.tax_type]
        if(lite.utils.array_has_data(tax_type.tax_accounts)){
            $.each(tax_type.tax_accounts, (_, tax)=>{
                if(tax.tax_rate){
                    this.totals.modules[mdl.name].tax_amount += (this.totals.modules[mdl.name].discounted_amount * tax.tax_rate) / 100
                }
            })
        }
        
        this.totals.modules[mdl.name].tax_amount = lite.utils.fixed_decimals(this.totals.modules[mdl.name].tax_amount, 2)
        this.totals.modules[mdl.name].inclusive = this.totals.modules[mdl.name].discounted_amount + this.totals.modules[mdl.name].tax_amount

        this.totals.exclusive_amount += this.totals.modules[mdl.name].exclusive
        this.totals.discount_amount += this.totals.modules[mdl.name].discount_amount
        this.totals.tax_amount += this.totals.modules[mdl.name].tax_amount
        this.totals.inclusive_amount += this.totals.modules[mdl.name].inclusive
    }

    calculate_totals(){
        this.totals.freq = this.freq_in_word,
        this.totals.additional_users = { qty:0, exclusive:0, tax_amount:0, inclusive:0},
        this.totals.additional_storage = { qty:0, exclusive:0, tax_amount:0, inclusive:0 },
        this.totals.modules = {}
        this.totals.exclusive_amount = 0
        this.totals.discount_amount = 0
        this.totals.tax_amount = 0
        this.totals.inclusive_amount = 0


        this.totals.freq = this.freq_in_word
        this.disc_rt = this.freq == 12 ? this.billing_config?.annual_discount : this.billing_config?.monthly_discount
        this.totals.modules = {}
        this.calculate_additional_users()
        this.calculate_additional_storage()
        if(lite.utils.array_has_data(this.selected)){
            $.each(this.selected,(_,mdl)=>{
                this.calculate_module_totals(this.modules[mdl])
            })
        }
        this.modules_exclusive = this.totals.exclusive_amount
        this.totals.exclusive_amount += (this.totals.additional_users.exclusive + this.totals.additional_storage.exclusive)
        this.totals.tax_amount += (this.totals.additional_users.tax_amount + this.totals.additional_storage.tax_amount)
        this.totals.inclusive_amount += (this.totals.additional_users.inclusive + this.totals.additional_storage.inclusive)

        this.$cost_per_user.html(lite.utils.currency((this.billing_config?.cost_per_additional_user || 0) * this.freq,1, this.billing_config.billing_currency))
        this.$cost_per_storage.html(lite.utils.currency((this.billing_config?.cost_per_additional_storage || 0) * this.freq,1, this.billing_config.billing_currency))
        this.$total_freq.html(this.totals.freq)
        this.$total_additional_storage.html(lite.utils.currency(this.totals.additional_storage.exclusive,2,this.billing_config.billing_currency))
        this.$total_additional_user.html(lite.utils.currency(this.totals.additional_users.exclusive,2,this.billing_config.billing_currency))
        this.$modules_xclusive_amount.html(lite.utils.currency(this.modules_exclusive,2,this.billing_config.billing_currency))
        this.$xclusive_amount.html(lite.utils.currency(this.totals.exclusive_amount,2,this.billing_config.billing_currency))
        this.$discount_amount.html(lite.utils.currency(this.totals.discount_amount,2,this.billing_config.billing_currency))
        this.$tax_amount.html(lite.utils.currency(this.totals.tax_amount,2,this.billing_config.billing_currency))
        this.$inclusive_amount.html(lite.utils.currency(this.totals.inclusive_amount,2,this.billing_config.billing_currency))
    }



    // KYC
    init_registration_type_actions(){
        $(document).on("click",".registration-type",e=>{
            e.preventDefault()
            const el = $(e.currentTarget) 
            this.registration_type = el.attr("as")
            $(".registration-type")?.removeClass("bg-default text-theme_text_color").addClass("bg-gray-200")
            el?.addClass("bg-default text-theme_text_color").removeClass("bg-gray-200")
            this.fields = this.forms[this.registration_type]
            this.populate_kyc()
        })
    }

    init_kyc(){
        this.fields = this.forms[this.registration_type]
        this.populate_kyc()
    }


    populate_kyc(){
        this.$kyc_fields_wrapper.empty()
        if(lite.utils.array_has_data(this.fields)){
            $.each(this.fields,(_,f)=>{
                this.$kyc_fields_wrapper.append(this.html_generator.build_form_field(f))
            })
        }
        lite.lite_selector.init_selectors()
    }

    async get_form_data(){
        let obj = {}
        let validated = true
        const fields = this.$kyc_fields_wrapper.find(".form-field")
        if(lite.utils.array_has_data(fields)){
            $.each(fields,(_,f)=>{
                const 
                    field_type = lite.utils.get_attribute(f,"fieldtype"), 
                    field_name = lite.utils.get_attribute($(f).find(".lite-field"),"fieldname")
                let value = '', is_required = $(f).find("input").attr("is_required")
                switch (field_type) {
                    case "link":
                        value = lite.lite_selector.get_select_value(f)
                        break;
                    case "text":
                        value = $(f).find(".lite-field").val()
                        break;
                    case "read-only":
                        value = $(f).find(".lite-field").attr("value")
                        break;
                }
                if(!value?.trim() && is_required == "true"){
                    const errorWrapper = $(f).find('.field-error-wrapper')
                    if(errorWrapper){
                        $(errorWrapper).removeClass("hidden").find(".error-text").text("This Field is required")
                        setTimeout(() => {
                            $(errorWrapper).addClass("hidden")
                        }, 3000);
                        validated = false
                    }
                }
                obj[field_name] = value
                if(this.registration_type === "individual"){
                    obj.name = `${obj.first_name || ""} ${obj.other_name || ""} ${obj.last_name || ""}`
                }
            })
        }
        if(validated){
            this.kyc = obj
            return await this.validate_kyc()
        }
        return false
    }

    async validate_kyc(){
        const {status,data,error_message} = await lite.connect.x_post("validate_kyc",this.kyc)
        if(status == lite.status_codes.ok){
            return true
        }
        return false
    }



    // LICENSE
    init_licensing(){

        let license_content = `<div class="text-12">${this.license?.content}</div>`
        
        let modules = `<div class="w-[50%] grid grid-cols-2 gap-x-4">`
        $.each(this.selected,(_,mdl)=>modules += ` <div class="mb-2"><strong class="text-13">${_+1}. ${mdl}</strong></div> `)
        modules += "</div>"
        license_content = lite.utils.replace_chars(license_content, "{{client company}}", `<strong>${this.kyc?.name}</strong>`)
        license_content = lite.utils.replace_chars(license_content, "{{owner company}}", `<strong>${lite.system_settings?.default_company}</strong>`)
        license_content = lite.utils.replace_chars(license_content, "{{selected modules}}", modules)
        this.kyc.license = license_content
        this.$license_content.html(license_content)

        this.$agree_to_license?.off("change")?.change(e=>{
            $('.prev-next-action-btn[action="next"]')?.prop("disabled", $(this.$agree_to_license).prop("checked")? false : true)
            if($(this.$agree_to_license).prop("checked")){
                $('.license-agree-text').removeClass("bg-red-600").addClass("bg-default")
            }
            else{
                $('.license-agree-text').addClass("bg-red-600").removeClass("bg-default")
            }
        })
    }

    async submit_kyc(){
        const submit = await lite.connect.new_tenant({
            kyc:this.kyc,
            selected_modules:this.selected,
            totals:this.totals
        })
        return submit
    }
}