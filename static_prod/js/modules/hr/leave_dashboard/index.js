import HR_HTML_Generator from '../../../page/html/hr_html_generator.js'

export default class leave_Dashboard {
    constructor() {
        this.generator = new HR_HTML_Generator ()
        this.$leave_utilization = $ ("#leave_utilization")
        this.$leave_designation = $ ("#leave_designation")
        this.$recent_applications = $ ("#recent_applications")
        this.$leave_department = $ ("#leave_department")
        this.onLeaveCalender = {}
        this.date = new Date()
        this.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        this.init_dashboard()
    }

    async init_dashboard(){
        const dashboard_content = await lite.connect.dashboard("leave_dashboard")
        lite.utils.init_dashboard(true)

        lite.utils.add_empty_component ({$wrapper: this.$recent_applications, text: "No Content Found", color: "slate", classnames:"h-full h-full"})

        if(dashboard_content.status === lite.status_codes.ok){
            this.data = dashboard_content.data
            this.init_charts()
            $.each ($('.currency'), (_, place) => {
                $(place).html (lite.user.company.default_currency)
            })
            lite.utils.count_figure("#used_days", this.data?.leave_values?.days_stats?.days?.used || 0)
            lite.utils.count_figure("#unused_days", this.data?.leave_values?.days_stats?.days?.unused || 0)
            lite.utils.count_figure("#Unused_days_value", this.data?.leave_values?.days_stats?.values?.unused || 0)
            lite.utils.count_figure("#used_days_value", this.data?.leave_values?.days_stats?.values?.used || 0)
            if (this.data?.recent_applications && this.data.recent_applications.length > 0) {
                this.$recent_applications.html ("")
                this.$recent_applications.html (this.generateRL (this.data.recent_applications))
            }
        }
        lite.utils.init_dashboard(false)
    }
    init_charts() {
        this.#leave_utilization ()
        this.#leave_by_designation ()
        this.#leave_by_department ()
        this.generate ()
    }
    generateRL (data) {
        let list = `
            <div class="w-full grid grid-cols-6 h-[50px] rounded-t-md bg-purple-700 text-12 font-semibold">
                <div class="w-full flex items-center justify-start h-full col-span-2 pl-2">
                    <span class="material-symbols-outlined mr-1 text-orange-600">
                        person
                    </span>
                    Applicant
                </div>
                <div class="w-full flex items-center justify-start col-span-3 h-full">
                    <span class="material-symbols-outlined mr-2">
                        event_available
                    </span>
                    from - to
                </div>

                <div class="w-full flex items-center justify-start h-full">
                    <span class="material-symbols-outlined mr-1">
                        functions
                    </span>
                    days
                </div>

            </div>
        `
        $.each (data, (_, la) => {
            list += `
                <div class="w-full grid grid-cols-6 h-[60px] rounded-t-md border-b text-12 font-semibold">
                    <div class="w-full flex items-center justify-start h-full col-span-2 pl-2">
                        <span class="material-symbols-outlined mr-1 text-orange-600">
                            person
                        </span>
                        ${la.employee_name}
                    </div>
                    <div class="w-full flex items-center justify-start col-span-3 h-full">
                        <span class="material-symbols-outlined mr-2">
                            event_available
                        </span>
                        <span class="">${moment(la?.from_date).format('Do MMM, YYYY') || la?.from_time} - ${moment(la?.to_date).format('Do MMM, YYYY') || la?.to_time}</span>
                    </div>
                    <div class="w-full flex items-center justify-start h-full">
                        <span class="material-symbols-outlined mr-1">
                            functions
                        </span>
                        ${la?.time_duration_formatted || ''}
                    </div>
                </div>
            `
        })
        return list
    }
    #leave_utilization () {
        if (this.data?.leave_utilization?.labels?.length <= 0) {
            lite.utils.add_empty_component ({$wrapper: $("#leave_utilization"), text: "No Content Found"})
        }else {
            const data = {
                values: this.data?.leave_utilization?.vals || [],
                labels: this.data?.leave_utilization?.labels || []
            }
            lite.charts.stacked_bar_chart ('leave_utilization', data.labels, data.values, {
                enable_markers: true,
                stroke_size: 2,
                height: "90%",
            })
        }
    }
    #leave_by_designation () {
        if (this.data?.leave_values?.days_stats?.used_vs_unused?.length <= 0) {
            lite.utils.add_empty_component ({$wrapper: $("#leave_designation"), text: "No Content Found"})
        }else {
            const data = {
                values: this.data?.leave_values?.days_stats?.used_vs_unused?.value || [],
                labels: this.data?.leave_values?.days_stats?.used_vs_unused?.label || []
            }
            lite.charts.donut_chart ('leave_designation', data.labels, data.values, {
                show_legend: false,
                plot_show: true,
                width: "90%",
                height: "90%"
            })
        }
    }
    #leave_by_department () {
        if (this.data.leave_department.label.length <= 0) {
            lite.utils.add_empty_component ({$wrapper: this.$leave_department, text: "No Content Found", color: "slate", classnames:"h-full h-full"})
        }else {
            const data = {
                values: this.data.leave_department.value || [],
                labels: this.data.leave_department.label || []
            }
            lite.charts.donut_chart ('leave_department', data.labels, data.values, {
                show_legend: false,
                plot_show: true,
                width: "90%",
                height: "90%"
            })
        }
    }
    renderCalendar(year, month) {
        $("#c_mo").html (`${this.months[month]} ${year}`)
        const calendar_data = this.data?.leave_calendar || null
        const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const prevMonthDays = new Date(year, month, 0).getDate();
        const $calendar = $("#calendar");
        $calendar.empty();

        daysOfWeek.forEach(day => {
            $calendar.append(
                `<div class="h-[30px] flex justify-center items-center font-semibold text-xs sm:text-sm md:text-xl">${day}</div>`
            );
            });
            for (let i = firstDay - 1; i >= 0; i--) {
            $calendar.append(
                `<div class="h-[90px] sm:h-[110px] md:h-[130px] bg-gray-100 text-gray-400 text-xs sm:text-sm flex justify-center items-start pt-1 sm:pt-2">
                ${prevMonthDays - i}
                </div>`
            );
            }
            for (let i = 1; i <= daysInMonth; i++) {
                let calendar = ''
                if (calendar_data[i]) {
                    this.onLeaveCalender[i] = []
                    let _ = 1
                    let plus = 0
                    for (const data_c of calendar_data[i]) {
                        this.onLeaveCalender[i].push(data_c)
                        if (_ < 3) {
                            calendar += `
                                <div class="relative group">
                                    <img
                                        src="${data_c.image ? data_c.image : '/media/defaults/avatas/dp.jpeg'}"
                                        class="w-10 h-10 rounded-full border-2 border-white cursor-pointer hover:scale-105 transition view_leave"
                                        data="${data_c.employee_name}"
                                        place="${i}"
                                    />
                                    <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 bg-default text-white text-xs rounded px-2 py-1 whitespace-nowrap opacity-0 group-hover:opacity-100 transition duration-200 z-50">
                                        ${data_c.employee_name}
                                    </div>
                                </div>
                            `
                        }else {
                            plus += 1
                        }
                    }
                    calendar += plus > 0 ? `
                    <div class="w-10 h-10 flex items-center justify-center rounded-full bg-gray-300 text-sm font-medium text-gray-700 border-2 border-white">
                        +${plus}
                    </div>
                    `: ''
                }
                $calendar.append(
                    `<div calendar_leave="${i}" class="openLM cursor-pointer h-[90px] sm:h-[110px] md:h-[130px] bg-slate-200 text-white text-xs sm:text-sm flex justify-center items-start pt-1 sm:pt-2">
                        <div class="h-full w-full relative pointer-events-none">
                            <div class="openLM absolute top-1 pointer-events-none left-1 h-[50px] w-[50px] rounded-full cursor-pointer text-white bg-default font-semibold text-2xl flex justify-center items-center">${i}</div>
                                <div class="h-full w-full flex flex-col items-end justify-end">
                                    <div class="h-[50%] pointer-events-none flex items-end justify-end w-full"></div>
                                    <div class="h-[50%] pointer-events-none flex items-end justify-end w-full">
                                        <div class="flex items-center -space-x-4">
                                            ${ calendar }
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>`
                );
            }
            const totalCells = firstDay + daysInMonth;
            const nextMonthDays = 42 - totalCells;
            for (let i = 1; i <= nextMonthDays; i++) {
            $calendar.append(
                `<div class="h-[90px] sm:h-[110px] md:h-[130px] bg-gray-100 text-gray-400 text-xs sm:text-sm flex justify-center items-start pt-1 sm:pt-2">
                ${i}
                </div>`
            );

            this.openModal_card()
        }
    }
    generate () {
        this.renderCalendar(this.date.getFullYear(), this.date.getMonth());
    }

    openModal_card() {
        $.each ($(".openLM"), (_, ol_btn) => {
            const $btn = $(ol_btn)
            $btn.on ('click', (e)=> {
                const $onL = $(e.target)
                const data = this.onLeaveCalender[$onL.attr ('calendar_leave')]
                let onLeave = `<h6 class="text-rose-500 font-extrabold capitalize text-3xl">No Employee is Going On Leave On ${$onL.attr ('calendar_leave')} ${this.months[this.date.getMonth()]}, ${this.date.getFullYear ()}</h6>`
                if (data && data.length > 0) {
                    const modal = $("#userModal")
                    onLeave = ""
                    for (const eol of data) {
                        onLeave += `
                            <div class="flex flex-col max-w-lg p-6 space-y-6 overflow-hidden rounded-lg shadow-md dark:bg-gray-50 dark:text-gray-800 close_model">
                                <div class="flex space-x-4">
                                    <div class="flex flex-col space-y-1">
                                        <a rel="noopener noreferrer" href="#" class="text-sm font-semibold">${eol.employee_name}</a>
                                        <span class="text-xs">Applied For <b class="text-sm text-emerald-600">${eol.time_duration_formatted}</b> Of ${eol.leave_type}</span>
                                    </div>
                                </div>
                                <div>
                                    <img src="${eol.image ? eol.image : '/media/defaults/avatas/dp.jpeg'}" alt="${eol.employee_name}" class="object-cover w-full mb-4 h-60 sm:h-96 dark:bg-gray-500">
                                    <h2 class="mb-1 text-xl text-default font-semibold">${eol.employee_name}</h2>
                                    <p class="text-sm dark:text-gray-600 p-2">
                                        <b>Leave type: </b> ${eol.leave_type}
                                    </p>
                                    <p class="text-sm dark:text-gray-600 p-2">
                                        <b>From Date: </b> ${eol.leave_mode == 'Days Leave' ? moment (eol.from_date).format('Do MMM, YYYY') : eol.from_time}
                                    </p>
                                    <p class="text-sm dark:text-gray-600 p-2">
                                        <b>To Date: </b> ${eol.leave_mode == 'Days Leave' ? moment (eol.to_date).format('Do MMM, YYYY') : eol.to_time}
                                    </p>
                                    <p class="text-sm dark:text-gray-600">
                                        <b>Total Days Taken: </b> ${eol.time_duration_formatted}
                                    </p>
                                </div>
                            </div>
                        `
                    }
                    modal.removeClass ('hidden')
                    modal.addClass('flex gap-4 flex-wrap')
                    modal.html (onLeave)
                    this.closeModal ()
                }
            })
        })
    }

    closeModal() {
        $.each ($(".model"), (_, mdl) => {
            const $mdl = $(mdl)
            $mdl.on ('click', (e) => {
                $(e.target).removeClass('flex').addClass ('hidden')
            })
        })
    }
}