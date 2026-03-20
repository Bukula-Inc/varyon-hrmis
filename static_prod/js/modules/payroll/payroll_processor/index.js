
import Payroll_HTML_Generator from '../../../page/html/payroll_html_generator.js'
export default class Payroll_Processor {
    constructor() {
        this.generator = new Payroll_HTML_Generator()
        this.$payroll_history = $(".payroll-history")
        this.init_payroll_processor()
    }
    async init_payroll_processor(){
        // if (lite.form_state == "new") {
        //     console.log('====================================');
        //     console.log(lite);
        //     console.log('====================================');
        //     $(".page-actions-wrapper").prepend (`
        //         <button class="compare-payroll-btn mr-3 min-w-[200px] h-[47px] text-16 max-w-[max-content]  btn bg-purple-700 text-theme_text_color shadow-md ">
        //             Compare Payroll
        //         </button>
        //     `)

        //     $ ('.compare-payroll-btn').on ('click', async (e) => {
        //         e.preventDefault ()
        //         const $btn = $(e.target)
        //         $btn.attr ('disabled', true)
        //         const controller = lite.page_controller.form_controller
        //         const payroll_c = await lite.connect.x_post ("compare_payrolls", {...controller.get_form_data ()?.values})
        //         if (payroll_c.status == lite.status_codes.ok) {
        //             const cols = payroll_c.data.cols
        //             const compare_payroll = payroll_c.data.data
        //             const $processor_wrapper =  $ ("#payroll_processor")
        //             $processor_wrapper.addClass ("relative h-full w-full").append (`
        //             <div class="attached-child-compare fixed overflow-y-auto top-0 left-0 z-[100000] right-0 bottom-0 box">
        //                 <div class="h-full w-full overflow-y-auto px-3">
        //                     <div class="h-[50px] w-full flex justify-end items-center border-b">
        //                         <button class="btn close-btn-compare bg-rose-700 text-white">
        //                             <span class="material-symbols-outlined font-extrabold">
        //                                 close
        //                             </span>
        //                         </button>
        //                     </div>
        //                     <div class="h-[calc(100%-50px)]">
        //                         ${
        //                             !payroll_c.data.status ? `
        //                                 <div class="h-full w-full flex justify-center items-center">
        //                                     <p class="font-extrabold text-[450x] text-rose-500">
        //                                         <span class="material-symbols-outlined">
        //                                             no_adult_content
        //                                         </span> No Previous Payroll Found
        //                                     </p>
        //                                 </div>
        //                             `: `
        //                                 <div class="h-full w-full overflow-y-auto p-4">
        //                                     <div class="header h-[45px] w-full text-white">
        //                                         <div class="h-full w-full flex px-4">
        //                                             ${this.get_head (cols)}
        //                                         </div>
        //                                     </div>
        //                                     <div class="body h-[calc(100%-45px)] w-full">
        //                                         ${this.get_body (compare_payroll, cols)}
        //                                     </div>
        //                                 </div>
        //                             `
        //                         }
        //                     </div>
        //             </div>`)
        //             $ (".close-btn-compare").on ("click", (e) => {
        //                 e.preventDefault ()
        //                 $ ('.attached-child-compare').remove ()
        //                 $btn.attr ('disabled', false)
        //             })
        //         }
        //     })
        // }
    }

    get_head (cols) {
        return cols.map ((col, i) => {
            if (i > 0)
                return `
                    <div
                        class="min-w-[260px] ${i==0? 'rounded-l-md': i== cols.length ? 'rounded-r-md': ''} bg-indigo-950 flex justify-center items-center max-w-max px-2 font-semibold capitalize"
                    >
                        New ${col.t}
                    </div>
                    <div
                        class="min-w-[260px] ${i==0? 'rounded-l-md': i== cols.length ? 'rounded-r-md': ''} bg-indigo-950 flex justify-center items-center max-w-max px-2 font-semibold capitalize"
                    >
                        Old ${col.t}
                    </div>
                `
            else
                return `
                    <div
                        class="min-w-[260px] ${i==0? 'rounded-l-md': i== cols.length ? 'rounded-r-md': ''} bg-indigo-950 flex justify-center items-center max-w-max px-2 font-semibold capitalize"
                    >
                        ${col.t}
                    </div>
                `
        }).join ('')
    }
    get_body (data, cols) {
        return data.map (dt => {
            return `
                <div class="h-[45px] w-full">
                    <div class="h-full w-full flex px-4">
                        ${
                            cols.map ((col, i) => {
                                if (i > 0)
                                    return `
                                        <div class="min-w-[260px] flex justify-center items-center max-w-max px-2 font-semibold capitalize">
                                            ${lite.utils.thousand_separator(dt.new[col.l], 2)}
                                        </div>

                                        <div class="min-w-[260px] flex justify-center items-center max-w-max px-2 font-semibold capitalize">
                                            ${lite.utils.thousand_separator(dt.old[col.l], 2)}
                                        </div>
                                    `
                                else
                                    return `
                                        <div class="min-w-[260px] flex justify-center items-center max-w-max px-2 font-semibold capitalize">
                                            ${dt.new[col.l]}
                                        </div>
                                    `
                            }).join ('')
                        }
                    </div>
                </div>
            `
        }).join ('')
    }
}