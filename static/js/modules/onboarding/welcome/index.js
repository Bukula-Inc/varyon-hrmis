export default class Welcome{
    constructor(){
        this.$wrapper = $(".wrapper")
        this.$onboarding_action = $(".onboarding-action-btn")
        this.$onboarding_stage = $(".onboarding-stage")
        this.$stage_circle = $(".stage-circle")
        this.$company_logo = $(".company-logo")
        this.has_updated_password = 0
        this.$user_names = $(".user-names")

        this.$password_wrapper_fields = $(".password-field-wrapper")

        this.$role_description = $("#description")


        this.current_stage=1
        this.stage_exec = [null, this.set_welcome_info, this.update_password, this.explain_roles,this.onboarding_completed]
        this.init()
    }

    generate_color(){
        return lite.color_codes[Math.floor(Math.random() * lite.color_codes.length)]
    }

    async get_user_content(){
        const {status, data, error} = await lite.connect.x_fetch("get_onboarding_content")
        if(status === lite.status_codes.ok){
            this.data = data
            this.user = this.data.user
            this.company = this.data.company
            this.onboarding = this.data.onboarding
            this.role = this.data.role
            this.menus = this.data.menus
            this.default_dashboard = this.data.default_dashboard
            this.has_updated_password = this.user.has_changed_default_password
        }
        return status
    }

    async init(){
        const user_content = await this.get_user_content()
        if(user_content == lite.status_codes.ok){
            this.$wrapper?.removeClass("hidden")
            lite.utils.init_dashboard(true)
            this.current_stage = this.onboarding.current_stage
            this.splashed = this.onboarding.splashed || 0

            if(this.company?.company_logo)
                this.$company_logo?.attr("src", this.company?.company_logo)

            // if(this.current_stage  == 1 && this.splashed == 0){
            //     this.init_congratulatory_flowers()
            // }

            this.stage_exec[this.current_stage](this)
            this.update_circle_stage()

            this.$onboarding_action?.click(async e=>{
                this.$onboarding_stage?.addClass("hidden")
                if(lite.utils.get_attribute(e.currentTarget, "action") === "next"){
                    if(this.current_stage <= 4)
                        this.current_stage += 1
                }
                else{
                    if(this.current_stage > 1)
                        this.current_stage -= 1
                }
                this.onboarding.current_stage = this.current_stage
                this.onboarding.splashed = 1
                const {status, data, error_message} = await lite.connect.patch({model:"Onboarding", data:this.onboarding})
                if(status === lite.status_codes.ok){
                    this.onboarding = data.data
                    this.stage_exec[this.current_stage](this)
                    this.update_circle_stage()
                }
                else{
                    lite.alerts.toast({
                        toast_type:lite.status_codes.ok,
                        title:"Updated Successfully",
                        message:"Your new password has been set successfully!"
                    })
                }
                
            })
        }
        
    }

    init_congratulatory_flowers(){
        const end = Date.now() + 15 * 200;
        const colors = lite.colors;
        (function frame() {
            confetti({
                particleCount: 20,
                angle: 20,
                spread: 55,
                origin: { x: 0 },
                colors: colors,
            });

            confetti({
                particleCount: 20,
                angle: 120,
                spread: 55,
                origin: { x: 1 },
                colors: colors,
            });

            if (Date.now() < end) {
                requestAnimationFrame(frame);
            }
        })();
    }

    update_circle_stage(){
        $.each(this.$stage_circle, (_,el)=>{
            if($(el)?.attr("stage") <= this.current_stage){
                $(el).addClass("bg-default text-theme_text_color").removeClass("bg-gray-100 text-black")
            }
            else{
                $(el).removeClass("bg-default text-theme_text_color").addClass("bg-gray-100 text-black")
            }
        })
    }

    set_welcome_info(cls){
        $(`.onboarding-stage[stage="${cls.current_stage}"]`).removeClass("hidden")
        cls.$user_names?.html(`${cls.user?.first_name || ""}`)

    }
    update_password(cls){
        $(`.onboarding-stage[stage="${cls.current_stage}"]`).removeClass("hidden")
        cls.$password_wrapper_fields.html(lite.html_generator.build_form_field({
            id:"old-password",
            fieldlabel:"Old Password",
            fieldname:"old_password",
            placeholder:"Enter Old Password (From your email.)",
            fieldtype:"password",
            classnames:"mb-3"
        }))
        cls.$password_wrapper_fields.append(lite.html_generator.build_form_field({
            id:"new-password",
            fieldlabel:"New Password",
            fieldname:"new_password",
            placeholder:"Enter New Password",
            fieldtype:"password",
            classnames:"mb-3"
        }))
        cls.$password_wrapper_fields.append(lite.html_generator.build_form_field({
            id:"rpt-new-password",
            fieldlabel:"Repeat New Password",
            fieldname:"repeat_new_password",
            placeholder:"Repeat New Password",
            fieldtype:"password",
        }))
        lite.utils.init_password_fields()

        $("#update-password")?.off("click")?.click(async e=>{
            const btn = $(e.currentTarget)
            const old_pwd_field = $(".lite-field#old-password"), pwd_field = $(".lite-field#new-password"), rpwd_field = $(".lite-field#rpt-new-password")
            const old_pwd = old_pwd_field?.val(), pwd = pwd_field?.val(), rpwd = rpwd_field?.val()
            if (!old_pwd){
                cls.show_error(old_pwd_field, "This field is required!")
            }
            if (!pwd){
                cls.show_error(pwd_field, "This field is required!")
            }
            if (!rpwd){
                cls.show_error(rpwd_field, "This field is required!")
            }
            if(old_pwd && pwd && rpwd){
                if(pwd !== rpwd){
                    cls.show_error(pwd_field, "Passwords do not match!")
                    cls.show_error(rpwd_field, "Passwords do not match!")
                }
                else{
                    const html = $(btn).html()
                    btn.html(`Updating Password &nbsp;
                        ${lite.utils.generate_loader ({light_mode: true, loader_type: 'dots'})}
                    `).prop("disabled", true)

                    const {status, data, error_message} = await lite.connect.x_post("update_user_password", {
                        "old_password": old_pwd?.trim(),
                        "new_password": pwd?.trim(),
                        "rpt_password": rpwd?.trim()
                    })
                    if(status === lite.status_codes.ok){
                        btn.html(html)
                        lite.alerts.toast({
                            toast_type:lite.status_codes.ok,
                            title:"Updated Successfully",
                            message:"Your new password has been set successfully!"
                        })
                        cls.current_stage += 1
                        cls.onboarding.current_stage = cls.current_stage
                        const {status, data, error_message} = await lite.connect.patch({model:"Onboarding", data: cls.onboarding})
                        if(status === lite.status_codes.ok){
                            cls.update_circle_stage()
                            cls.$onboarding_stage?.addClass("hidden")
                            cls.stage_exec[cls.current_stage](cls)
                        }
                        else{
                            lite.alerts.toast({
                                toast_type:lite.status_codes.unprocessable_entity,
                                title:"Failed to update stage",
                                message:"Failed to update current stage!"
                            })
                        }
                    }
                    else{
                        btn.html(html).prop("disabled", false)
                    }
                
                }
            }
        })
    }



    show_error(field, error_message){
        field?.siblings(".field-error-wrapper ").removeClass("hidden").addClass("shake").find(".error-text").text(error_message)
        setTimeout(() => {
            field?.siblings(".field-error-wrapper ").removeClass("shake").addClass("hidden").find(".error-text").text("")
        }, 4000);
    }

    explain_roles(cls){
        $(`.onboarding-stage[stage="${cls.current_stage}"]`).removeClass("hidden")
        if(cls.role.description){
            cls.$role_description.html(cls.role.description)
        }
        if(lite.utils.object_has_data(cls.menus)){
            let current = ""
            $.each(lite.utils.get_object_keys(cls.menus),(_, k)=>{
                const random_color = cls.generate_color()
                const key = lite.utils.capitalize(lite.utils.replace_chars(k,"_"," "))
                $.each(cls.menus[k]?.reverse(),(_,feature)=>{
                    if(current === ""){
                        current = k
                        $('.allowed-features-list').append(`<div class="col-span-4 intro-y border-b font-semibold my-5 border-b-[${random_color.inner}] text-[${random_color.inner}]">${key}</div>`)
                    }
                    else if(current !== k){
                        current = k
                        $('.allowed-features-list').append(`<div class="col-span-4 intro-y border-b font-semibold my-5 border-b-[${random_color.inner}] text-[${random_color.inner}]">${key}</div>`)
                    }
                    $('.allowed-features-list').append(`
                        <a target="__blank" href="/app/${feature.module}/${feature.app}?module=${feature.module}&app=${feature.app}&page=${feature.page_type}&content_type=${feature.content_type}" class="w-full h-full bg-[${random_color.base}] rounded-md p-1 min-h-[40px] flex items-center justify-start border border-[${random_color.inner}] intro-y">
                            <span class="material-symbols-outlined text-17 ml-2"> ${feature.icon} </span>
                            <div class="flex flex-col ml-2">
                                <span class="font-semibold text-11">${feature.title}</span>
                                <small class="text-gray-500">Module: ${key}</small>
                            </div>
                        </a>
                    `)
                })
            })
        }



        $(".role-btn")?.off("click")?.click(e=>{
            $(".role-btn").removeClass("bg-default text-theme_text_color")
            $(e.currentTarget).addClass("bg-default text-theme_text_color")
            $(".role-description").addClass("hidden")
            $(`.role-description#${$(e.currentTarget).attr("for")}`).removeClass("hidden")
        })
    }


    async onboarding_completed(cls){
        $(`.onboarding-stage`).addClass("hidden")
        $(".onboarding-actions")?.remove()
        const {status, data, error_message} = await lite.connect.x_post("certify_user", {user:cls.user})
        if(status === lite.status_codes.ok){
            cls.certificate = data
            $(`.onboarding-stage[stage="${cls.current_stage}"]`).removeClass("hidden")
            cls.init_congratulatory_flowers()
            $(".completion-action-btn")?.off("click")?.click(e=>{
                const action = $(e.currentTarget).attr("for")
                if(action === "download certificate"){
                    // lite.utils.print_doc(cls.certificate?.default_print_format,cls.certificate?.doctype,cls.certificate?.id, 1)
                    $(e.currentTarget)?.remove()
                    lite.alerts.toast({
                        toast_type: status,
                        title: "Coming Soon",
                        message: "This feature is unavailable at the moment."
                    })
                }
                else{
                    window.location.replace(cls.default_dashboard?.url)
                }
            })
        }
        else{
            lite.alerts.toast({
                toast_type: status,
                title: "Certificate Generation Failed",
                message: error_message
            })
        }

        
    }
}