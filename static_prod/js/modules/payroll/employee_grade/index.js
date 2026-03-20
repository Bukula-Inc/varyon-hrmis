
import Payroll_HTML_Generator from '../../../page/html/payroll_html_generator.js'

class Employee_Grade {
    constructor(config) {   
        this.generator = new Payroll_HTML_Generator()
        // this.$employee_grade_stats = $("#employee-grade-stats")
        this.$employee_grade = $("#employee-grade")

        this.utils = config.utils
        this.page_controller = config.page_controller
        this.nav_manager = config.nav_manager
        this.charts = config.charts
        this.sessions = config.sessions
        this.connect = config.connection
        this.init_dashboard()
    }

    async init_dashboard() {
        const dashboard_content = await lite.connect.dashboard("employee_grade")
        if (dashboard_content.status == lite.status_codes.ok) {
            this.data = dashboard_content.data
            if (!this.data?.grade_data || this.data?.grade_data.length == 0) {
                lite.utils.add_empty_component ({$wrapper: this.$employee_grade, text: "No Content Found", color: "gray"})
            }else {
                this.$employee_grade.append(this.generator.employee_grade(this.data?.grade_data)) 

            }
            if (!this.data?.grade_data || this.data?.grade_data.length == 0) {
                lite.utils.add_empty_component ({$wrapper: this.$employee_grade, text: "No Content Found", color: "gray"})
            }else {
                this.init_charts(this.data?.grade_data)

            }
        }
        lite.utils.init_dashboard(true)
        
        
    }

    init_charts(data) {
        this.grade(data);
    }

    grade(data) {
        const grades = {}; 
        
        data.forEach(item => {
            const gradeName = item?.grade_name || "";
            const totalEmployees = item?.total_grade_emp || 0;
            
            if (grades[gradeName]) {
                grades[gradeName] += totalEmployees;
            } else {
                grades[gradeName] = totalEmployees;
            }
        });
    
        const chartData = {
            labels: Object.keys(grades).slice(0, 5),
            values: Object.values(grades).slice(0, 5)
        };
        
        this.charts.pie_chart('employee-grade-stats', chartData.labels, chartData.values, {
            // Additional chart options can be set here
            show_legend: false,
            height: 300
        });
    }
    
    
}

export default Employee_Grade