// 
import Core_HTML_Generator from "../../../page/html/core_html_generator.js"

export default class Core{
    constructor(){
        this.generator = new Core_HTML_Generator()
        this.$total_users = $(".total-users")
        this.$total_countries = $(".total-countries")
        this.$total_currencies = $(".total-currencies")
        this.$sector_list = $(".sector-list")
        this.$industry_list = $(".industry-list")
        this.$user_role_list = $(".user-role-list")
        this.$workflow_list = $(".workflow-list")
        this.$data_import_list = $(".data-imports-list")
        this.$series_list = $(".naming-series-list")
        this.init()
    }
    async init(){
        const dashboard_content = await lite.connect.dashboard("core")
        lite.utils.init_dashboard(true)
        if(dashboard_content?.status === lite.status_codes.ok){
            
            this.data = dashboard_content.data
            this.init_top_stats()
            this.populate_sectors()
            this.populate_industries()
            this.populate_roles()
            this.populate_workflows()
            this.populate_data_imports()
            this.populate_series()
        }
    }

    init_top_stats(){
        lite.utils.count_figure(this.$total_countries, this.data?.total_countries,false,0)
        lite.utils.count_figure(this.$total_currencies, this.data?.total_currencies,false,0)
        lite.utils.count_figure(this.$total_users, this.data?.total_users,false,0)
    }

    populate_sectors(){
        if(lite.utils.array_has_data(this.data?.sectors)){
            this.$sector_list?.empty()
            $.each(this.data?.sectors,(_,s)=>{
                this?.$sector_list.append(this.generator.create_sector_row(s))
            })
        }
    }
    populate_industries(){
        if(lite.utils.array_has_data(this.data?.industries)){
            this.$industry_list?.empty()
            $.each(this.data?.industries,(_,s)=>{
                this?.$industry_list.append(this.generator.create_industry_row(s))
            })
        }
    }
    populate_roles(){
        if(lite.utils.array_has_data(this.data?.user_roles)){
            this.$user_role_list?.empty()
            $.each(this.data?.user_roles,(_,s)=>{
                this?.$user_role_list.append(this.generator.create_user_role_row(s))
            })
        }
    }
    populate_workflows(){
        if(lite.utils.array_has_data(this.data?.workflows)){
            this.$workflow_list?.empty()
            $.each(this.data?.workflows,(_,s)=>{
                this?.$workflow_list.append(this.generator.create_workflow_row(s))
            })
        }
    }
    populate_data_imports(){
        if(lite.utils.array_has_data(this.data?.data_imports)){
            this.$data_import_list?.empty()
            $.each(this.data?.data_imports,(_,s)=>{
                this?.$data_import_list.append(this.generator.create_data_import_row(s))
            })
        }
    }
    populate_series(){
        if(lite.utils.array_has_data(this.data?.naming_series)){
            this.$series_list?.empty()
            $.each(this.data?.naming_series,(_,s)=>{
                this?.$series_list.append(this.generator.create_series_row(s))
            })
        }
    }
    
}