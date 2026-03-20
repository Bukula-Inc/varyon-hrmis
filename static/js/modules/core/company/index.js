
export default class Company {
    constructor() {
        this.$default_company_logo = $(".default-company-logo")
        this.$default_company = $(".default-company-name")
        this.$default_comp_reporting_currerncy = $(".default-company-reporting-currency")
        this.$default_comp_country = $(".default-company-country")
        this.$default_comp_tax_id = $(".default-company-tax-id")
        this.$default_comp_email = $(".default-company-email")
        this.$default_physical_address = $(".company-physical-address")
        this.set_default_data()
        lite.lite_file_picker.init_file_picker(this.handle_company_logo_chached, this)
    }

    set_default_data(){
        this.default_company = lite.defaults?.company
        if(!lite.utils.is_empty_object(this.default_company)){
            this.$default_company.html(this.default_company?.name)
            this.$default_comp_reporting_currerncy.html(this.default_company?.reporting_currency)
            this.$default_comp_country.html(this.default_company?.country)
            this.$default_comp_tax_id.html(this.default_company?.tax_identification_no)
            this.$default_comp_email.html(this.default_company?.email)
            this.$default_physical_address.html(this.default_company?.physical_address)
            this.$default_company_logo?.attr("src", this.default_company?.company_logo)
        }
    }

    async handle_company_logo_chached(data, cls){
        if(data && data.file){
            const updated = await lite.connect.upload({files: data.file})
            if(updated.status === lite.status_codes.ok){
                let company = cls.default_company?.name
                if(lite.form_data?.doctype === "Company"){
                    company = lite.form_data?.name
                }
                const loader_id = lite.alerts.loading_toast({ title: `Updating logo`,  message: `Updating logo for ${company}` })
                const update_url = await lite.connect.x_post("update_company_logo", {"url": updated?.data?.data?.path,"company": company})
                lite.alerts.destroy_toast(loader_id)
                if(update_url.status == lite.status_codes.ok){
                    cls.$default_company_logo?.attr("src", updated?.data?.data?.path)
                    lite.alerts.toast({
                        toast_type:lite.status_codes.ok,
                        title:"Update Successful",
                        message:"Company logo has been updated successfully!"
                    })
                }
            }
        }
    }
}