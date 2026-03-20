import HR_HTML_Generator from '../../../page/html/hr_html_generator.js'
export default class Skills_Distribution {
    constructor(config) {
        this.generator = new HR_HTML_Generator ()
        this.$skills_category = $("#skills_category")
        this.$skills_by_department = $("#skills_by_department")
        this.$emp_turnover = $("#emp_turnover")
        this.$skills_vs_performance = $("#skills_vs_performance")
        this.$training_program = $("#training_program_attendee")
        this.$top_employees = $("#top_employees")
        this.$total_departments = $("#total_departments")
        this.init_dashboard()
    }

    async init_dashboard(){
        
        const dashboard_content = await lite.connect.dashboard("employee_skills_dashboard")
        if(dashboard_content.status == lite.status_codes.ok){
            this.data = dashboard_content.data
            lite.utils.count_figure(this.$top_employees, this.data?.skilled_employees?.total_employees)
            lite.utils.count_figure(this.$total_departments, this.data?.get_departments)            
            this.#emp_turnover()
            this.#skills_gap_by_department()
            this.#skills_category()
            this.#skills_vs_performance()
            this.#training_programs()
        }
        lite.utils.init_dashboard(true)
    }

    #emp_turnover () {
        const emp_turnover_ = this.data?.get_employee_infor.data;
        const labels = emp_turnover_.map(item => item.designation || "");
        const values = emp_turnover_.map(item => item.employee_count || 0);
        lite.charts.donut_chart('emp_turnover', labels, values, {
            show_legend: false,
            plot_show: true,
            width: "60%",
            height: "60%"
        });
    }
    #skills_gap_by_department () {
        const skills_gap_by_department = this.data?.departmental_skill_gap;
        const departments = Object.keys(skills_gap_by_department);
        const designations = Object.keys(Object.values(skills_gap_by_department)[0]);
        const dataValues = designations.map(designation => {
            return {
                name: designation,
                data: departments.map(department => skills_gap_by_department[department][designation])
            };
        });
        const data = {
            values: dataValues,
            labels: departments
        };
        lite.charts.multi_line_chart('skills_by_department', data.labels, data.values, {
            enable_markers: true,
            stroke_size: 2,
            height: "90%"
        });
    }
    #skills_category () {
        const qualification_cate = this.data?.employee_certifications || []
        const labels = qualification_cate.map(item => item.file_name)
        const values = qualification_cate.map(item => item.count)
        const data = {
            values,
            labels
        }
        lite.charts.column_chart_with_negatives ('skills_category', data.labels, data.values, {
            enable_markers: true,
            stroke_size: 2,
            height: "90%"
        })
    }
    #skills_vs_performance () {
        const skill_vs_perform = this.data?.self_appraisal || []
        const data = {
            values: skill_vs_perform.values,
            labels: skill_vs_perform.labels
        }
        
        lite.charts.stacked_bar_chart('skills_vs_performance', data.labels, data.values, {
            enable_markers: true,
            stroke_size: 2,
            height: "90%"
        })
    }
    
    #training_programs() {
        const training_program = this.data?.open_training_programs || []
        
        if (!training_program || !lite.utils.object_has_data(training_program)){
            lite.utils.add_empty_component({ $wrapper: this.$training_program, text: "No Employee On Training Program", color: "default", classnames: "absolute" })
        }
        this.$training_program.append(this.generator.training_program(training_program))
    }
}

