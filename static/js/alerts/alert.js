
class Alerts {
    constructor(config) {
        this.utils = config.utils
        this.body = $('body')
        this.last_toast_y_position = 0
        this.structures = {
            200: {
                response: "Successful",
                color: 'default',
                icon: 'check_circle'
            },
            201: {
                response: "Created Successfully",
                color: 'indigo',
                icon: 'task_alt'
            },
            204: {
                response: "No Content Found",
                color: 'orange',
                icon: 'filter_list_off'
            },
            301: {
                response: "Moved Permanently",
                color: 'yellow',
                icon: 'arrows_outward'
            },
            302: {
                response: "Found",
                color: 'orange',
                icon: 'search_check'
            },
            304: {
                response: "Not Modified",
                color: 'blue',
                icon: 'edit'
            },
            400: {
                response: "Bad Request",
                color: 'red',
                icon: 'link_off'
            },
            401: {
                response: "Unauthorized",
                color: 'orange',
                icon: 'private_connectivity'
            },
            403: {
                response: "Forbidden",
                color: 'orange',
                icon: 'lock'
            },
            404: {
                response: "Not Found",
                color: 'orange',
                icon: 'check_box_outline_blank'
            },
            405: {
                response: "Method Not Allowed",
                color: 'red',
                icon: 'block'
            },
            422: {
                response: "Unprocessed Entry",
                color: 'emerald',
                icon: 'developer_board_off'
            },
            500: {
                response: "Internal Server Error",
                color: 'red',
                icon: 'warning'
            },
            501: {
                response: "Not Implemented",
                color: 'orange',
                icon: 'pending'
            },
            502: {
                response: "Bad Request",
                color: 'orange',
                icon: 'assignment_late'
            },
            503: {
                response: "Service Unavailable",
                color: 'yellow',
                icon: 'cloud_off'
            },
        }
    }
    

    toast({ toast_type, title, message, x_position = 'right', y_position = 'top', timer = 15000, persist=false }) {
        const struct = this.structures[toast_type]
        const toast_id = this.utils.unique(40)
        const btn_id = this.utils.unique(40)
        if (this.last_toast_y_position === 0)
            this.last_toast_y_position += 10
        else {
            this.last_toast_y_position += (10 + 90)
        }
        this.body.prepend(`
            <div id="${toast_id}" class="toast fixed z-[100] ${x_position}-[6px] ${y_position}-[${this.last_toast_y_position}px] min-w-[300px] gap-y-3 max-w-[600px] w-[max-content] min-h-[50px] rounded-md shadow-darker bg-white border border-${struct?.color}/80 grid grid-template-columns-[1fr_5fr]" style="z-index:3000">
                <div class="w-full h-full flex items-center justify-start py-1 bg-${struct?.color} bg-${struct?.color}-600 px-2 rounded-t-md">
                    <div class="flex items-center justify-start w-full">
                        <span class="material-symbols-outlined text-[30px] text-theme_text_color mr-2">
                            ${struct?.icon}
                        </span>
                        <h5 class="font-semibold text-15 text-theme_text_color">${title}</h5>
                    </div>
                    <button id="${btn_id}" class="close-toast txt-30">
                        <span class="material-symbols-outlined text-15 text-theme_text_color btn border-none"> close </span>
                    </button>
                </div>
                <div class="col-span-[5] w-full h-full max-h-[500px] overflow-y-auto pl-4 pb-5">
                    <div class="text-12">${message}</div>
                </div>
            </div>
        `)
        $(`#${btn_id}`)?.off("click")?.click(()=> $(`#${toast_id}`)?.remove())
        if(!persist)
            setTimeout(() => {
                if (this.last_toast_y_position === 10)
                    this.last_toast_y_position -= 10
                else {
                    this.last_toast_y_position -= (10 + 90)
                }
                $(`#${toast_id}`).remove()
            }, timer);
    }

    loading_toast({ title, message, x_position = 'right', y_position = 'top', timer = 15000 }) {
        const toast_id = this.utils.unique(40)
        if (this.last_toast_y_position === 0)
            this.last_toast_y_position += 10
        else {
            this.last_toast_y_position += (10 + 90)
        }

        this.body.prepend(`
            <div id="${toast_id}" class="toast fixed ${x_position}-[6px] ${y_position}-[${this.last_toast_y_position}px] w-[300px] min-h-[50px] rounded-md shadow-darker bg-white border border-default/60 p-2 flex items-center justify-between" style="z-index:3000">
                <div class="w-[50px] h-full flex items-center justify-center">
                    <span class="material-symbols-outlined text-[30px] text-default">
                        ${this.utils.generate_loader({size:25})}
                    </span>
                </div>
                <div class="w-[90%] h-full pl-4 border-l ">
                    <h5 class="font-semibold text-13 text-default">${title}</h5>
                    <span class="text-12">${message}</span>
                </div>
            </div>
        `)
        return toast_id
    }

    destroy_toast(id){
        this.last_toast_y_position =  (10 + 90)
        $(`#${id}`)?.remove()
    }

}

export default Alerts