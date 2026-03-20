

import HR_HTML_Generator from '../../../page/html/hr_html_generator.js'

export default class Dashboard {
    constructor() {   
        this.generator = new HR_HTML_Generator ()
        this.$total_programs =$(".total-programs")
        this.$ongoing_training_programs = $("#ongoing-training-programs")
        this.$scheduled_training_programs = $("#scheduled-training-programs")
        this.$rejected_training_programs = $("#rejected-training-programs")
        this.$completed_training_programs = $("#completed-training-programs")
        // this.$total_attendees = $(".total_attendees")
        // this.$training_summary_chart = $('#training-summary-chart')
       
        this.init_dashboard()
    }

    async init_dashboard() {
        try {
            
            const training_program_sideview = await lite.connect.dashboard("training_program");
            
            if (training_program_sideview.status == lite.status_codes.ok) {
                this.data = training_program_sideview.data;

                if (this.data) {
                    lite.utils.count_figure(this.$total_programs, this.data.total_programs);
                    lite.utils.count_figure(this.$ongoing_training_programs, 0);
                    lite.utils.count_figure(this.$scheduled_training_programs, 0);
                    lite.utils.count_figure(this.$rejected_training_programs, 0);
                    lite.utils.count_figure(this.$completed_training_programs, 0);

                    // CHART DATA
                    if (this.data.participation_metric.labels.length >0){
                        const info = {
                            "labels": this.data.participation_metric.labels,
                            "values": this.data.participation_metric.value,
                        }   
                        this.populate_training_summary_chart(info)
                    }else{
                        lite.utils.add_empty_component({$wrapper:$("#training-summary-chart"),text:"No Data Available", color:"gray", classnames:"absolute"})                        
                    }
                } else {
                    throw new Error("Data is undefined");
                }
            } else {
                throw new Error("Failed to fetch dashboard data");
            }
        } catch (error) {
            console.error("Error initializing dashboard:", error);
        }
    }

    populate_training_summary_chart(info) {        

        lite.charts.pie_chart('training-summary-chart', info.labels, info.values,  {
            height: 370,
            enable_markers: true, stroke_size: 1,
            title: 'Participation Metrics',
            series_title: '',
            formatter_decimals: 0,
            width: 250,
            title_align: 'right',
            curve: 'curve' | 'smooth',
        })
        // }/
    }
}