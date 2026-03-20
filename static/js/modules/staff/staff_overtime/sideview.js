
// import Staff_HTML_Generator from '../../../page/html/staff_html_generator.js'

// class Staff_Overtime {
//     constructor(config) {   
//         this.generator = new Staff_HTML_Generator()
//         this.$staff_overtime = $("#stafff-overtime")
//         // this.$staff_overtime_stats = $("#staff-overtime-stats")

//         // this.utils = config.utils
//         // this.page_controller = config.page_controller
//         // this.nav_manager = config.nav_manager
//         // this.charts = config.charts
//         // this.sessions = config.sessions
//         // this.connect = config.connectin
//         this.init_dashboard()
//     }

//     async init_dashboard() {
//         const emp_name = lite.employee_info.name
//         const dashboard_content = await lite.connect.x_post("staff_overtime", {name: emp_name, employee:lite.employee_info.name})
       
//         if (dashboard_content.status == lite.status_codes.ok) {
       
//             this.data = dashboard_content.data
//             if (!this.data?.overtime_info || this.data?.overtime_info.length == 0) {
//                 lite.utils.add_empty_component ({$wrapper: this.$staff_overtime, text: "No Content Found", color: "gray"})
//             }else {
    
//                 this.$staff_overtime.append(this.generator.overtime(this.data.overtime_info));          
//             }

//             if (!this.data?.overtime_stats || this.data?.overtime_stats.length == 0) {
//                 lite.utils.add_empty_component ({$wrapper: this.$staff_overtime_stats, text: "No Content Found", color: "gray"})
//             }else {
//                 const data = this.data.overtime_stats;
//                         let labels = [];
//                         let values = [];

//                         data.forEach(item => {
//                             const status = item?.status || "";
//                             const count = item?.count || 0;

//                             labels.push(status);
//                             values.push(count);
//                         });


//                         lite.charts.pie_chart('staff-overtime-stats', labels, values, {
//                             show_legend: false,
//                             height: 300,
//                              colors: [
//                     lite.charts.colors[1],
//                     lite.charts.colors[0],
//                     lite.charts.negative_colors[1],
//                     lite.charts.colors[5]
//                 ]
//                         });
//             }
           
           
//         }
//         lite.utils.init_dashboard(true)
//     }
// }

// export default Staff_Overtime
