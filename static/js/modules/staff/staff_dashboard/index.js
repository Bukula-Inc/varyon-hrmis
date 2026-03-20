import HTML_Builder from "../../../page/html/html_builder.js";
import Staff_HTML_Generator from "../../../page/html/staff_html_generator.js";
export default class Staff_Dashboard {
  constructor() {
    this.builder = new Staff_HTML_Generator();
    this.months = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ];

    this.employee_no = $(".employee-no");
    this.employee_status = $(".employee-status");
    this.full_name = $(".full-names");
    this.designation = $(".designation");
    this.department = $(".department");
    this.email = $(".email");
    this.contact_no = $(".contact-no");
    this.gender = $(".gender");
    this.profile_img = $(".profile-img");
    this.employee_files = $("#employee-files");
    this.recent_payslips = $("#recent-payslips");
    this.leave_cumulative_stats = $("#leave-cumulative-stats");
    this.task_summary = $("#task-summary");
    this.todays_pending_tasks = $("#todays-pending-tasks");

    this.init();
  }

  async init() {
    const { status, data, error_message } = await lite.connect.dashboard(
      "staff",
      { emp: lite?.employee_info?.name || " " },
    );
    if (status === lite.status_codes.ok) {
      this.data = data;
      lite.utils.count_figure(
        $("#leave_balance"),
        this.data?.hr?.leave_info?.balance || 0,
      );
      $("#application_stats").html(this.data?.hr?.leave_info?.leave_stats);

      lite.utils.count_figure(
        $("#basic"),
        this.data?.payroll?.ytd_summary?.basic_pay || 0.0,
      );
      lite.utils.count_figure(
        $("#gross"),
        this.data?.payroll?.ytd_summary?.gross || 0.0,
      );
      lite.utils.count_figure(
        $("#net"),
        this.data?.payroll?.ytd_summary?.net || 0.0,
      );
      lite.utils.count_figure(
        $("#deductions"),
        this.data?.payroll?.ytd_summary?.total_deductions || 0.0,
      );
      lite.utils.count_figure(
        $("#balance_advance"),
        this.data?.payroll?.advance_amount || 0.0,
      );
      lite.utils.count_figure(
        $("#repaid-advance"),
        this.data?.payroll?.advance_repaid || 0.0,
      );
      lite.utils.count_figure(
        $("#completed_tasks"),
        this.data?.hr?.work_plan?.today?.completed || 0.0,
      );
      lite.utils.count_figure(
        $("#total_tasks"),
        this.data?.hr?.work_plan?.today?.total_tasks || 0.0,
      );

      if (!this.data?.hr?.employee_files)
        lite.utils.add_empty_component({
          $wrapper: $("#employee-files"),
          text: "No Content Found",
          color: "gray",
        });
      else
        $("#employee-files").html(
          this.builder.emp_files(this.data?.hr?.employee_files || []),
        );

      if (this.data?.payroll?.recent_payslip.length <= 0)
        lite.utils.add_empty_component({
          $wrapper: $("#recent-payslips"),
          text: "No Content Found",
          color: "gray",
        });
      else {
        $("#recent-payslips").html(
          this.builder.emp_recent_payslip(
            this.data?.payroll?.recent_payslip || [],
          ),
        );
        $.each($("[payslip-download-btn]") || [], (_, btn) => {
          $(btn).on("click", (e) => {
            const payslip = $(btn).attr("payslip-download-btn");
            if (!payslip) {
              lite.alerts.toast({
                toast_type: lite.status_codes.no_content,
                title: "Not Found",
                message: `Payslip Not Found`,
              });
              return;
            }
            const print_format = "Payslip Standard Format",
              model = "Payslip";
            const r = lite.utils.print_doc(print_format, model, payslip, 1);
          });
        });
      }

      if (this.data?.hr?.work_plan?.today?.tasks.length <= 0)
        lite.utils.add_empty_component({
          $wrapper: $("#todays-pending-tasks"),
          text: "No Content Found",
          color: "gray",
        });
      else
        $("#todays-pending-tasks").html(
          this.builder.emp_todays_tasks(
            this.data?.hr?.work_plan?.today?.tasks || [],
          ),
        );
    }

    this.init_employee_profile();
    lite.utils.init_dashboard(true);

    this.init_leave_stats_chart();
    this.ytd_earnings_and_deductions();
  }

  init_employee_profile() {
    console.log(this.profile_img);
    const img_dp = "";
    if (this.data?.hr?.employee_info) {
      const emp = this.data?.hr?.employee_info;
      this.employee_no.html(emp.name);
      this.gender.html(emp.gender);
      this.employee_status
        .html(emp.status)
        .addClass(`!text-[${emp?.status_inner_color}]`);
      this.profile_img.attr(
        "src",
        `${img_dp ? img_dp : "/static/images/avata/default-avata.png"}`,
      );
      this.full_name.html(emp.full_name);
      this.designation.html(emp.designation);
      this.department.html(emp.department);
      this.email.html(emp.email);
      this.contact_no.html(emp.contact_no);
    }
  }

  init_leave_stats_chart() {
    const leave_stats = this.data?.hr?.leave_info?.leave_status;
    const data = {
      labels: leave_stats?.labels,
      values: [
        {
          name: "Days Accrued",
          data: leave_stats?.days || [],
        },
        {
          name: "Days Taken",
          data: leave_stats?.apps || [],
        },
      ],
    };
    console.log(data);
    lite.charts.column_chart(
      "leave-cumulative-stats",
      data.labels,
      data.values,
      {
        height: "90%",
        curve: "smooth",
        enable_markers: true,
        markers_size: 4,
        stroke_size: 5,
        colors: [
          lite?.defaults?.company?.default_theme_color,
          "#da2877",
          "#032a49",
        ],
        formatter: (val) =>
          lite.utils.thousand_separator(
            val,
            lite.system_settings?.currency_decimals,
          ),
      },
    );
  }
  ytd_earnings_and_deductions() {
    const work_plan = this.data?.hr?.work_plan?.Summary;
    const data = {
      labels: ["Completed", "Pending", "Overdue", "Total"],
      values: [
        work_plan?.completed || 0,
        work_plan?.pending || 0,
        work_plan?.overdue || 0,
        work_plan?.total || 0,
      ],
    };
    lite.charts.pie_chart("task-summary", data.labels, data.values, {
      width: "130%",
      height: "100%",
      colors: [
        lite?.defaults?.company?.default_theme_color,
        "#032a49",
        "#0F8890",
      ],
      title_align: "left",
      show_legend: false,
      legend_position: "right",
      formatter: (val) =>
        lite.utils.thousand_separator(
          val,
          lite.system_settings?.currency_decimals,
        ),
    });
  }
}
