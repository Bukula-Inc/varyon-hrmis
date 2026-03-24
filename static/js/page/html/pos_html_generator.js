import HTML_Builder from "./html_builder.js"

export default class POS_HTML_Generator{
    constructor(){
        this.builder = new HTML_Builder()
    }

    checkout_form_fields(payment_model){
        const form_fields =[
            this.builder.build_form_field({
                id: "show_override_approval",
                fieldlabel: "show_override_approval",
                fieldname: "show_override_approval",
                fieldtype: "check",
                columns: 1,
                required: false,
                hidden: true,
                default: "0.00",
            }),
            this.builder.build_form_field({
                id: "override_approval",
                fieldlabel: "POS Override / Approval Code",
                fieldname: "override_approval",
                fieldtype: "text",
                columns: 1,
                placeholder: "Enter the Override/Approve Code",
                required: false,
                hidden: false,
                displayon: ["show_override_approval", 1],
            }),
            this.builder.build_form_field({
                id:"payment_method",
                fieldlabel:"Payment Method",
                fieldname:"payment_method",
                fieldtype:"select",
                options: [ "Cash", "Card", "Mobile Money" ],
                required: true,
                placeholder:"Select a Payment Method",
                default: payment_model,
            }),
            this.builder.build_form_field({
                id: "amount_paid",
                fieldlabel: "Amount Paid",
                fieldname: "amount_paid",
                fieldtype: "float",
                columns: 1,
                placeholder: "Enter Amount Paid",
                required: false,
                hidden: false,
                default: "0.00",
                displayon: ["payment_method", "Cash"],
            }),
            this.builder.build_form_field({
                id: "mobile_money_acc",
                fieldlabel: "Mobile Money Account",
                fieldname: "mobile_money_acc",
                fieldtype:"text",
                columns: 1,
                required: false,
                hidden: false,
                placeholder: "260 912 345678",
                displayon: ["payment_method", "Mobile Money"],
            }),
        ]
        return form_fields 
    }

    box_view(content_title, content_text, button) {
        return `
            <div class="w-full h-full intro-y flex items-center justify-center">
                <div class="box p-3 h-[30%] w-[20%] flex flex-col mx-auto mt-[15%]">
                    <!-- Title at the top -->
                    <div class="w-full flex items-center justify-between">
                        <h4 class="font-semibold text-slate-600">${content_title}</h4>
                    </div>

                    <!-- Divider -->
                    <div class="my-5 bg-gray-300 w-full h-[3px] rounded-full"></div>

                    <!-- Text in the middle -->
                    <p class="text-gray-600 mb-4 flex-grow">${content_text}.</p>

                    <!-- Button at the bottom and full width -->
                    ${button}
                </div>
            </div>`
    }

    create_till_record_stats() {
        return `
            <!-- first row -->
            <span class="font-semibold col-span-2">Cashier : </span> <span class="font-semibold cashier-names col-span-3"></span>
            <span class="font-semibold col-span-2">Till No : </span> <span class="font-semibold till-no col-span-3">N/A</span>
            <span class="font-semibold col-span-2">Starting Float : </span> <span class="font-semibold starting-float col-span-3">0.00</span>
            <span class="font-semibold col-span-2">Total Sold Value : </span> <span class="font-semibold total-sold-value col-span-3">0.00</span>
            <span class="font-semibold col-span-2">Mobile Money Total : </span> <span class="font-semibold mobile-money-total col-span-3">0.00</span>
            <!-- second row -->
            <span class="font-semibold col-span-2">Sale Point : </span> <span class="font-semibold sale-point col-span-3"></span>
            <span class="font-semibold col-span-2">Total Qty Sold : </span> <span class="font-semibold total-sold-qty col-span-3">0</span>
            <span class="font-semibold col-span-2">Cash on Hand : </span> <span class="font-semibold cash-on-hand col-span-3">0.00</span>
            <span class="font-semibold col-span-2">Cash Payment Total : </span> <span class="font-semibold cash-payment-total col-span-3">0.00</span>
            <span class="font-semibold col-span-2">Card Payment Total : </span> <span class="font-semibold card-payment-total col-span-3">0.00</span>
        `
    }

    create_pos_items() {
        return `
            <div class="skeleton filters-wrapper w-full rounded-lg bg-default text-theme_text_color min-h-[60px] flex items-center justify-between p-2 px-3 mt-3 border">
                <div class="filter-fields flex items-center justify-start w-[80%]">
                    <div class="">
                        <h3 class="font-bold">Stock Items</h3>
                        <small class="text-12">Select items to add them to cart</small>
                    </div>
                </div>
                <div class="list-actions grid grid-cols-2 gap-x-3 pos-filters-wrapper"></div>
            </div>
            <div class="skeleton w-full h-[62vh] report-box  mt-2">
                <div class="w-full  h-full intro-y box p-3 overflow-hidden overflow-y-auto overflow-y-auto">
                    <div class="w-full listview-wrapper item-list grid grid-cols-5 gap-3"></div>
                </div>
            </div>
        `
    }

    create_cart_checkout() {
        return `
            <div class="w-full h-[70vh] grid gri-rows-3 gap-y-5">
                <div class="w-full report-box mt-3 intro-y">
                    <div class="box p-3 h-[40vh] cart-checkout">
                        <div class="pos-cart-items w-full h-full">
                            <div class="w-full border-b pb-3 flex items-center justify-between">
                                <div class="flex flex-col">
                                    <strong>Cart | Selected Items</strong>
                                    <small>All selected items are displayed below</small>
                                </div>
                                <div class="flex items-center justify-end relative pos-currency-filters-wrapper"></div>
                            </div>
                            <div class="pos-cart w-full h-[77%] overflow-hidden overflow-y-auto mt-3"></div>
                        </div>
                    </div>
                </div>


                <div class="w-full report-box mt-3 intro-y h-[250px]">
                    <div class="box p-3 h-full overflow-y-auto">
                        <div class="w-full flex items-center justify-center flex-col">
                            <div class="pos-totals w-full grid grid-cols-2 gap-x-8">
                                <div class="w-full intro-y flex items-center justify-between mb-4 border-b pb-2">
                                    <strong class="text-gray-600 text-12">Customer</strong>
                                    <strong class="text-gray-600 text-12 pos-customer"></strong>
                                </div>
                                <div class="w-full intro-y flex items-center justify-between mb-4 border-b pb-2">
                                    <strong class="text-gray-600 text-12">Total Quantity</strong>
                                    <strong class="text-gray-600 text-12 pos-total-qty">0</strong>
                                </div>
                                <div class="w-full intro-y flex items-center justify-between mb-4 border-b pb-2">
                                    <strong class="text-gray-600 text-12">Sub Total</strong>
                                    <strong class="text-gray-600 text-12 pos-sub-total">0.00</strong>
                                </div>
                                <div class="w-full intro-y flex items-center justify-between mb-4 border-b pb-2">
                                    <strong class="text-gray-600 text-12">Discount Total</strong>
                                    <strong class="text-gray-600 text-12 pos-discount-total">0.00</strong>
                                </div>
                                <div class="w-full intro-y flex items-center justify-between mb-4 border-b pb-2">
                                    <strong class="text-gray-600 text-12">Total Taxes</strong>
                                    <strong class="text-gray-600 text-12 pos-taxes-total">0.00</strong>
                                </div>
                                <div class="w-full intro-y flex items-center justify-between mb-4 border-b pb-2">
                                    <strong class="text-gray-600 text-12">Inclusive Total</strong>
                                    <strong class="text-gray-600 text-12 pos-inclusive-total">0.00</strong>
                                </div>
                            </div>
                            <div  class="pos-actions w-full grid grid-cols-2 gap-x-5 mt-3">
                                <button action="clear" class="pos-action w-full intro-y  h-[40px] btn border border-orange-500 text-orange-500 rounded-md flex items-center justify-center">
                                    <span class="material-symbols-outlined mr-2 text-20">
                                        remove_shopping_cart
                                    </span>
                                    Clear Cart
                                </button>
                                <button  action="checkout" class="pos-action w-full intro-y  h-[40px] btn rounded-md bg-default text-theme_text_color flex items-center justify-center">
                                    <span class="material-symbols-outlined mr-2 text-20">
                                        shopping_cart_checkout
                                    </span>
                                    Checkout 
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
    }
    payment_method() {
        return `
            <div class="w-full h-[70vh] grid gri-rows-3 gap-y-5">
                <div class="w-full report-box mt-3 intro-y">
                    <div class="box p-3 h-[40vh] payment_method">
                        <div class="pos-cart-items w-full h-full">
                            <div class="w-full border-b pb-3 flex items-center justify-between">
                                <div class="flex flex-col">
                                    <strong>Cart | Selected Items</strong>
                                    <small>All selected items are displayed below</small>
                                </div>
                                <div class="flex items-center justify-end relative pos-currency-filters-wrapper"></div>
                            </div>
                            <div class="pos-cart w-full h-[77%] overflow-hidden overflow-y-auto mt-3"></div>
                        </div>
                    </div>
                </div>


                <div class="w-full report-box mt-3 intro-y h-[250px]">
                    <div class="box p-3 h-full overflow-y-auto">
                        <div class="w-full flex items-center justify-center flex-col">
                            <div class="pos-totals w-full grid grid-cols-2 gap-x-8">
                                <div class="w-full intro-y flex items-center justify-between mb-4 border-b pb-2">
                                    <strong class="text-gray-600 text-12">Customer</strong>
                                    <strong class="text-gray-600 text-12 pos-customer"></strong>
                                </div>
                                <div class="w-full intro-y flex items-center justify-between mb-4 border-b pb-2">
                                    <strong class="text-gray-600 text-12">Total Quantity</strong>
                                    <strong class="text-gray-600 text-12 pos-total-qty">0</strong>
                                </div>
                                <div class="w-full intro-y flex items-center justify-between mb-4 border-b pb-2">
                                    <strong class="text-gray-600 text-12">Sub Total</strong>
                                    <strong class="text-gray-600 text-12 pos-sub-total">0.00</strong>
                                </div>
                                <div class="w-full intro-y flex items-center justify-between mb-4 border-b pb-2">
                                    <strong class="text-gray-600 text-12">Discount Total</strong>
                                    <strong class="text-gray-600 text-12 pos-discount-total">0.00</strong>
                                </div>
                                <div class="w-full intro-y flex items-center justify-between mb-4 border-b pb-2">
                                    <strong class="text-gray-600 text-12">Total Taxes</strong>
                                    <strong class="text-gray-600 text-12 pos-taxes-total">0.00</strong>
                                </div>
                                <div class="w-full intro-y flex items-center justify-between mb-4 border-b pb-2">
                                    <strong class="text-gray-600 text-12">Inclusive Total</strong>
                                    <strong class="text-gray-600 text-12 pos-inclusive-total">0.00</strong>
                                </div>
                            </div>
                            <div  class="pos-actions w-full grid grid-cols-2 gap-x-5 mt-3">
                                <button action="clear" class="pos-action w-full intro-y  h-[40px] btn border border-orange-500 text-orange-500 rounded-md flex items-center justify-center">
                                    <span class="material-symbols-outlined mr-2 text-20">
                                        remove_shopping_cart
                                    </span>
                                    Clear Cart
                                </button>
                                <button  action="checkout" class="pos-action w-full intro-y  h-[40px] btn rounded-md bg-default text-theme_text_color flex items-center justify-center">
                                    <span class="material-symbols-outlined mr-2 text-20">
                                        shopping_cart_checkout
                                    </span>
                                    Checkout 
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
    }

    generate_wrappers() {
        return `<div class="row-span-6 grid grid-cols-3 grid-rows-2 gap-3 p-3 w-full h-full menu-card-wrapper box"></div>`
    }

    generate_title(title, content, currentUrl, selected) {
        let path = content.url;
        let isSelected = selected;
        let card = `<a href="${path}" class="h-full flex items-center box justify-center text-xl font-bold uppercase ${isSelected ? 'text-white bg-default' : 'text-slate-600 hover:text-white hover:bg-default'} rounded-md transition duration-200">${title.toUpperCase()}</a>`
        return `<div class="p-2 w-[30%]">${card}</div>`
    }

    generate_card(title, card_items) {
        let html_card_items = ``
        card_items.forEach((item) => {
            let html_sub_card_items = ``
            if (lite.utils.array_has_data(item.child_items)) {
                item.child_items.forEach((child) => {
                    html_sub_card_items += `
                        <div class="w-[98%] mb-1 ml-1 flex items-center justify-between">
                            <a href="/app/${child.module}/${child.app_name}?loc=${child.app_name}&type=${child.page_type}&document=${child.document}" class="navigation-link flex items-center text-gray-800 justify-start transition duration-100 hover:translate-x-[-5px] h-[30px] hover:text-default">
                                <span class="material-symbols-outlined text-[#720ecf] mr-1 text-20 .material-symbols-outlined-hidden">${child.icon}</span>
                                ${child.title}
                            </a>
                            <input type="checkbox" id="9eFAGGjwpnuHQ1xE4Bs3HUkTbPQFDZJ5J2wpx4k_yewQJKUmDqfnjfyVHpvIpgJnlEBOS9" class="sub-link-toggler hidden">
                            <label for="9eFAGGjwpnuHQ1xE4Bs3HUkTbPQFDZJ5J2wpx4k_yewQJKUmDqfnjfyVHpvIpgJnlEBOS9" class="sub-nav-toggler border-none px-3 cursor-pointer expanded"><span class="material-symbols-outlined text-gray-600 text-[18px] .material-symbols-outlined-hidden"> expand_more </span>
                            </label>
                        </div>
                    `
                })
            }
            html_card_items += `
                <div class="navigation-wrapper w-full mb-1 flex items-center justify-start flex-col">
                    <div class="w-[98%] mb-1 ml-1 flex items-center justify-between">
                        <a href="/app/${item.module}/${item.app}?loc=${item.app}&type=${item.page_type}&document=${item.document}" class="navigation-link flex items-center text-gray-800 justify-start transition duration-100 hover:translate-x-[-5px] h-[30px] hover:text-default">
                            <span class="material-symbols-outlined text-[#720ecf] mr-1 text-20 .material-symbols-outlined-hidden">${item.icon}</span>
                            ${item.title} 
                        </a>
                        <input type="checkbox" id="xyAwfwbQY7gZSYdCdl9PumggpzxGk9W9oFS4MA09JZfNvLyZpJi31RLjYXrKnefb706M1e" class="sub-link-toggler hidden">
                        <label for="xyAwfwbQY7gZSYdCdl9PumggpzxGk9W9oFS4MA09JZfNvLyZpJi31RLjYXrKnefb706M1e" class="sub-nav-toggler border-none px-3 cursor-pointer">
                        </label>
                    </div>
                    <div class="sub-links hidden w-[97%] bg-gray-100 p-1 rounded-md">${html_sub_card_items}</div>
                </div>
            `
        })

        return `
            <div class="w-full h-full nav-card-wrapper text-white rounded-md">
                <div class="text-white mb-2 bg-default font-semibold text-14 w-[100%] flex items-center justify-between cursor-pointer p-2 rounded-t-md">
                    ${title}
                    <span class="material-symbols-outlined text-[16px] text-black mr-2 .material-symbols-outlined-hidden">expand_more</span>
                </div> 
                <div class="w-full h-full mt-3 text-13 overflow-y-scroll">
                    ${html_card_items}
                </div>
            </div>
        `
    }

    truncateText(text, maxLength) {
        if (text != null && text.length > maxLength) {
          text = text.substring(0, maxLength) + '...';
        }
        if (text == null) return "..."
        else return text
    }

    add_open_till_button() {
        let open_till = `
        <div class="ml-2">
            <button for="" class="open-till-action-btn w-[170px] btn bg-white text-white shadow-md border border-green-500 text-green-500">
                <span class="material-symbols-outlined text-20 mr-2">point_of_sale</span>
                Open till
            </button>
        </div>`

        return open_till
    }

    add_right_action_buttons() {
        let request_cash = `<div class="ml-2">
            <button for="" class="request-cash-action-btn w-[170px] btn bg-white text-white shadow-md border border-green-500 text-green-500">
                <span class="material-symbols-outlined text-20 mr-2">request_quote</span>
                Request Cash
            </button>
        </div>`
        let cashout = `<div class="ml-2">
            <button for="" class="cashout-action-btn w-[170px] btn bg-white text-white shadow-md border border-red-500 text-red-500">
                <span class="material-symbols-outlined text-20 mr-2">mintmark</span>
                Cashout
            </button>
        </div>`
        let close_till = `<div class="ml-2">
            <button for="" class="close-till-action-btn w-[170px] btn bg-default text-theme_text_color shadow-md ">
                <span class="material-symbols-outlined text-20 mr-2">done_all</span>
                Close till
            </button>
        </div>`

        return `${request_cash} ${cashout} ${close_till}`
    }

    retail_dashboard_action_buttons(sale_point_state) {
        let open_sale_point = `
        <div class="ml-2">
            <button for="" class="open-sale-point-action-btn w-[170px] btn bg-white text-white shadow-md border border-green-500 text-green-500">
                <span class="material-symbols-outlined text-20 mr-2">door_open</span>
                Open Sale Point
            </button>
        </div>`
        let close_sale_point = `
        <div class="ml-2">
            <button for="" class="close-sale-point-action-btn w-[170px] btn bg-white text-white shadow-md border border-red-500 text-red-500">
                <span class="material-symbols-outlined text-20 mr-2">door_front</span>
                Close Sale Point
            </button>
        </div>`
        if (sale_point_state == 0) return open_sale_point
        else return close_sale_point
    }

    create_sale_data_table() {
        return `<div class="sales-wrapper border border-dashed rounded-md min-h-[40px] !important"></div>`;
    }

    create_cashier_table() {
        return `<div class="cashier-wrapper rounded-md min-h-[40px] !important"></div>`;
    }

    create_log_table() {
        return `<div class="log-wrapper rounded-md min-h-[40px] !important"></div>`;
    }

    create_sales_titles() {
        return `
            <div class="w-full h-[30px] bg-default flex flex-row text-white rounded-tl-md col-span-7 grid grid-cols-8 sales-titles">
                <div class="w-full flex font-semibold col-span-1 border-r text-12">
                    <p class="m-auto">Time</p>
                </div>
                <div class="w-full flex font-semibold col-span-1 border-r text-12">
                    <p class="m-auto">Customer</p>
                </div>
                <div class="w-full flex font-semibold col-span-1 border-r text-12">
                    <p class="m-auto">Currency</p>
                </div>
                <div class="w-full flex font-semibold col-span-1 border-r text-12">
                    <p class="m-auto">Items</p>
                </div>
                <div class="w-full flex font-semibold col-span-1 border-r text-12">
                    <p class="m-auto">Discounted amount</p>
                </div>
                <div class="w-full flex font-semibold col-span-1 border-r text-12">
                    <p class="m-auto">Taxes amount</p>
                </div> 
                <div class="w-full flex font-semibold col-span-1 border-r text-12">
                    <p class="m-auto">Exclusive amount</p>
                </div>
                <div class="w-full flex font-semibold col-span-1 border-r text-12">
                    <p class="m-auto">Inclusive amount</p>
                </div>                              
            </div>
            <div class="sales-table-data max-h-[400px] overflow-y-scroll"></div>`;
    }

    create_cashier_titles() {
        return `
            <div class="text-slate-500 mb-2 font-semibold">Cashiers</div>
            <div class="w-full h-[30px] bg-default text-theme_text_color rounded-tl-md col-span-7 grid grid-cols-3 cashier-titles">
                <div class="w-full font-semibold col-span-1 border-r text-12 text-start p-1">
                    <p class="m-auto p-1">User</p>
                </div>
                <div class="w-full font-semibold col-span-1 border-r text-12 text-start p-1">
                    <p class="m-auto p-1">First Name</p>
                </div>
                <div class="w-full font-semibold col-span-1 border-r text-12 text-start p-1">
                    <p class="m-auto p-1">Last Name</p>
                </div>
            </div>
            <div class="cashier-table-data max-h-[400px] overflow-y-scroll"></div>`;
    }

    create_log_titles() {
        return `
            <div class="text-slate-500 mb-2 font-semibold">Logs</div>
            <div class="w-full h-[30px] bg-default text-theme_text_color rounded-tl-md col-span-7 grid grid-cols-7 cashier-titles">
                <div class="w-full font-semibold col-span-1 border-r text-12 text-start p-1">
                    <p class="m-auto p-1">Time</p>
                </div>
                <div class="w-full font-semibold col-span-1 border-r text-12 text-start p-1">
                    <p class="m-auto p-1">Type</p>
                </div>
                <div class="w-full font-semibold col-span-1 border-r text-12 text-start p-1">
                    <p class="m-auto p-1">Amount</p>
                </div>
                <div class="w-full font-semibold col-span-4 border-r text-12 text-start p-1">
                    <p class="m-auto p-1">Description</p>
                </div>
            </div>
            <div class="log-table-data max-h-[400px] overflow-y-scroll"></div>`;
    }

    create_sales_item(data) {
        let rows = '';
        data.forEach(item => {
            let line_items = '';
            Object.entries(item.line_items).forEach(([key, value]) => {
                if (line_items === '') line_items = value.name;
                else line_items += `, ${value.name}`;
            });
            rows += `
            <div class="w-full h-[30px] bg-white rounded-t-md grid grid-cols-8 border-b text-center">
                <div class="w-full h-full font-semibold text-12 border-r">
                    <p class="m-auto px-2">${item.current_time || "--" }</p>
                </div>
                <div class="w-full h-full font-semibold text-12 border-r">
                    <p class="m-auto px-2">${item.customer || "Walk-In"}</p>
                </div>
                <div class="w-full h-full font-semibold text-12 border-r">
                    <p class="m-auto px-2">${item.currency}</p>
                </div>
                <div class="w-full h-full font-semibold text-12 border-r">
                    <p class="m-auto px-2">${this.truncateText(line_items, 10)}</p>
                </div>
                <div class="w-full h-full font-semibold text-12 border-r">
                    <p class="m-auto px-2">${lite.utils.thousand_separator(item.base_total_discount_amount, 2)}</p>
                </div>
                <div class="w-full h-full font-semibold text-12 border-r">
                    <p class="m-auto px-2">${lite.utils.thousand_separator(item.base_total_taxes_amount, 2)}</p>
                </div>
                <div class="w-full h-full font-semibold text-12 border-r">
                    <p class="m-auto px-2">${lite.utils.thousand_separator(item.base_tax_exclusive_total_amount, 2)}</p>
                </div>
                <div class="w-full h-full font-semibold text-12 border-r">
                    <p class="m-auto px-2">${lite.utils.thousand_separator(item.base_inclusive_total_amount, 2)}</p>
                </div>
            </div>`;
        });
        return rows;
    }

    create_cashier_item(data) {
        let rows = '';
        data.forEach(cashier => {
            rows += `
            <div class="w-full h-[30px] bg-white rounded-t-md grid grid-cols-3 border-b text-start p-1">
                <div class="w-full h-full font-semibold text-12 border-r px-1">
                    <p class="m-auto px-2">${cashier.user}</p>
                </div>
                <div class="w-full h-full font-semibold text-12 border-r px-1">
                    <p class="m-auto px-2">${cashier.first_name}</p>
                </div>
                <div class="w-full h-full font-semibold text-12 border-r px-1">
                    <p class="m-auto px-2">${cashier.last_name}</p>
                </div>
            </div>`;
        });
        return rows;
    }

    create_log_item(data) {
        let rows = '';
        data.forEach(log => {
            rows += `
            <div class="w-full h-[30px] bg-white rounded-t-md grid grid-cols-7 border-b text-start p-1">
                <div class="w-full h-full col-span-1 font-semibold text-12 border-r px-1">
                    <p class="m-auto px-2">${log.time}</p>
                </div>
                <div class="w-full h-full col-span-1 font-semibold text-12 border-r px-1">
                    <p class="m-auto px-2">${log.type}</p>
                </div>
                <div class="w-full h-full col-span-1 font-semibold text-12 border-r px-1">
                    <p class="m-auto px-2">${lite.utils.thousand_separator(log.amount, 2)}</p>
                </div>
                <div class="w-full h-full col-span-4 font-semibold text-12 border-r px-1">
                    <p class="m-auto px-2">${log.description}</p>
                </div>
            </div>`;
        });
        return rows;
    }

    create_filters(customer){
        return `
            <div class="flex items-center justify-end relative w-full pos-customer-filter">
                <span class="material-symbols-outlined absolute left-3 text-20 text-gray-300 z-[50]">search</span>
                <select id="customer" type="link" for="Customer" linkfield="name" fieldname="customer" value="${customer?.name || ""}" class="lite-selector lite-field w-[300px] bg-white/20 text-white px-2 pl-8" placeholder="Search Customer"></select>
            </div>
            <div class="flex items-center justify-end relative w-full pos-item-filter">
                <span class="material-symbols-outlined absolute left-3 text-20 text-gray-300 z-[50]"> search </span>
                <select id="item" type="link" for="Stock_Item" linkfield="name" fieldname="item" class="lite-selector lite-field w-[300px] bg-white/20 text-white px-2 pl-8" placeholder="Search Item"></select>
            </div>
        `
    }

    create_option(item){
        return `<option value="${item}" class="option intro-yy hover:bg-default hover:text-white border-b"><div class="flex flex-col">${item}</div></option>`
    }
    create_currency_filter(currency){
        return `
            <span class="material-symbols-outlined absolute left-3 text-20 text-gray-300 z-[50]">search</span>
            <select id="currency" type="link" for="Currency" linkfield="name" fieldname="currency" value="${currency || ''}" fetch-from="customer" fetch-if-has-value="true" fetch-field="reporting_currency" class="lite-selector lite-field w-[200px] border px-2 pl-8" placeholder="Choose Sales Currency"></select>
        `
    }

    create_item(item, idx) {
        console.log("Item Details",item);
        
        let image_or_icon = '';
        if (item.product_img == null || item.product_img == "") {
            image_or_icon = `<span class="material-symbols-outlined text-[50px] mb-2 text-default">shopping_cart</span>`;
        } else {
            image_or_icon = `<img class="border border-grey-700 rounded-lg w-full h-full" style="object-fit: cover;" src="${item.product_img}" alt="${item.name}">`;
        }
        return `
            <div id="${lite.utils.unique()}${idx}" 
                 class="w-full h-[200px] pos-item cursor-pointer transition transform hover:translate-x-1 hover:bg-gray-100 border rounded-md p-1 flex items-center justify-center flex-col bg-gray-50 intro-y relative col-span-1" 
                 lite-value="${item.name}">
                <div class="w-full h-[150px] flex items-center justify-center">
                    ${image_or_icon}
                </div>
                <div class="w-full flex items-center justify-between mt-2">
                    <small class="font-semibold text-gray-600">${this.truncateText(item.name, 10)}</small>
                    <small class="font-semibold bg-default rounded-md px-2 text-white">${lite.utils.thousand_separator(item.selling_price, 2)}</small>
                </div>
                <div lite-value="${item.name}" class="absolute w-full h-full z-3 val-wrapper"></div>
            </div>
        `;
    }    

    create_cart_item(item,id){
        return `
            <div id="${id}" lite-value="${item.item_name}" class="cart-item w-full min-h-[70px] flex items-center justify-between intro-x my-3 mr-4">
                <div class="w-[99%] border min-h-[70px] flex items-center justify-between rounded-md px-4 py-1 relative overflow-hidden">
                    <div class="flex items-center justify-start">
                        <div class="w-[37px] h-[37px] rounded-full bg-default flex items-center justify-center">
                            <span class="material-symbols-outlined text-[20px] text-white">shopping_cart</span>
                        </div>
                        <div class="flex flex-col items-start ml-3">
                            <strong class="text-start text-13">${item.item_name?.trim()}</strong>
                            <small>${this.truncateText(item.description, 40)}</small>
                        </div>
                    </div>
                    <div class="flex flex-col items-end ml-3">
                        <small class="text-center text-13 text-[11px]">Unit Price: <span class="cart-xclusive-by-qty">0.00 x 0</span></small>
                        <strong class="text-center text-13 ">Total  + Tax: <span class="cart-inclusive-total"></span></strong>
                        <div class="w-full flex items-center justify-center my-1 mt-3">
                            <input type="number" lite-item="${item.item_name}" class="lite-field item-discount-amount focus:outline-none border text-13 text-center  w-[100px] h-[30px] form-control rounded-0 mx-2" value="${item.discount_amount}" placeholder="Disc (A)" min="0">
                            <input type="number" lite-item="${item.item_name}" class="lite-field item-discount-percentage focus:outline-none border text-13 text-center  w-[100px] h-[30px] form-control rounded-0 mx-2" value="${item.discount_percentage}" placeholder="Disc %" min="0">
                            
                            <button class="cart-q-action btn bg-white w-[30px] h-[30px] shadow-none" action="-">
                                <span class="material-symbols-outlined"> remove </span>
                            </button>
                            <input type="number" lite-item="${item.item_name}" value="${item.qty}" class="lite-field item-quantity focus:outline-none border text-13 text-center w-[80px] h-[30px] form-control rounded-0 mx-2" placeholder="Qty">
                            <button class="cart-q-action btn bg-white w-[30px] h-[30px] shadow-none" action="+">
                                <span class="material-symbols-outlined"> add </span>
                            </button>
                        </div>
                    </div>
                    <div
                    <button lite-value="${item.name}" class="remove-item-from-cart absolute cursor-pointer w-[20px] h-[20px] top-0 right-0 rounded-bl-md bg-danger text-white flex items-center justify-center font-bold">
                        <span class="material-symbols-outlined">close</span>
                    </button>
                </div>
                <div class="w-1"></div>
            </div>
        `
    }

    checkout_card() {
        return `<div class="pos-checkout w-full h-[77%] overflow-hidden overflow-y-auto mt-3">
                    <!-- Hidden select element -->
                    <select class="checkout-options hidden" name="payment_method">
                        <option value="Card">Card</option>
                        <!--  <option value="Voucher">Voucher</option> -->
                        <option value="Cash">Cash</option>
                        <option value="Mobile Money">Mobile Money</option>
                    </select>

                    <!-- Options divs -->
                    <div class="w-full flex flex-col items-center justify-center mt-3">
                        <div class="grid grid-cols-4 gap-3 w-full checkout-options">
                            <div class="w-full h-[80px] cursor-pointer transition transform hover:translate-x-1 hover:bg-gray-100 border rounded-md p-2 flex items-center justify-center flex-col bg-gray-50 intro-y relative option" data-value="Card">
                                <div class="w-full h-[50px] flex items-center justify-center">
                                    <span class="material-symbols-outlined text-[50px] text-default">credit_card</span>
                                </div>
                                <small class="font-semibold text-gray-600">Card</small>
                            </div>
                            <!-- <div class="w-full h-[80px] cursor-pointer transition transform hover:translate-x-1 hover:bg-gray-100 border rounded-md p-2 flex items-center justify-center flex-col bg-gray-50 intro-y relative option" data-value="Voucher">
                                <div class="w-full h-[50px] flex items-center justify-center">
                                    <span class="material-symbols-outlined text-[50px] text-default">confirmation_number</span>
                                </div>
                                <small class="font-semibold text-gray-600">Voucher</small>
                            </div> -->
                            <div class="w-full h-[80px] cursor-pointer transition transform hover:translate-x-1 hover:bg-gray-100 border rounded-md p-2 flex items-center justify-center flex-col bg-gray-50 intro-y relative option" data-value="Cash">
                                <div class="w-full h-[50px] flex items-center justify-center">
                                    <span class="material-symbols-outlined text-[50px] text-default">payments</span>
                                </div>
                                <small class="font-semibold text-gray-600">Cash</small>
                            </div>
                            <div class="w-full h-[80px] cursor-pointer transition transform hover:translate-x-1 hover:bg-gray-100 border rounded-md p-2 flex items-center justify-center flex-col bg-gray-50 intro-y relative option" data-value="Mobile Money">
                                <div class="w-full h-[50px] flex items-center justify-center">
                                    <span class="material-symbols-outlined text-[50px] text-default">mobile_friendly</span>
                                </div>
                                <small class="font-semibold text-gray-600">Mobile Money</small>
                            </div>
                        </div>
                        <div class="checkout-options-list w-full h-full mt-2"></div>
                    </div>
                </div>`
    }

    checkout_actions() {
        return `<button action="cancel" class="w-full intro-y  h-[40px] btn border border-orange-500 text-orange-500 rounded-md flex items-center justify-center">
                    <span class="material-symbols-outlined mr-2 text-20">
                        cancel
                    </span>
                    Cancel
                </button>
                <button  action="complete" class="checkout-action-completew-full intro-y  h-[40px] btn rounded-md bg-default text-theme_text_color flex items-center justify-center">
                    <span class="material-symbols-outlined mr-2 text-20">
                        shopping_cart_checkout
                    </span>
                    Complete Sale
                </button>`
    }

    checkout_options_list(checkout_option) {
        let fields = ''
        if (checkout_option === "Mobile Money") {
            let phone_number = this.builder.build_form_field({
                id: "phone_number",
                fieldtype: "text",
                fieldlabel: "Phone Number",
                placeholder: "260 096 123456",
                classnames: "w-full h-full justify-center",
            });
            fields = phone_number
        }
        else if (checkout_option === "Cash") {
            let change = this.builder.build_form_field({
                id: "change",
                fieldtype: "read-only",
                fieldlabel: "Change",
                placeholder: "Change",
                classnames: "w-full h-full justify-center pos-change",
                is_figure: true,
            });
            let amount_to_paid = this.builder.build_form_field({
                id: "amount_paid",
                fieldtype: "text",
                fieldlabel: "Amount Paid",
                placeholder: "Amount Paid",
                classnames: "w-full h-full justify-center pos-amount-paid",
                is_figure: true,
            });
            fields = `${change} ${amount_to_paid}`
        }
        // else if (checkout_option === "Voucher") {
        //     let voucher_no = this.builder.build_form_field({
        //         id: "voucher_no",
        //         fieldtype: "text",
        //         fieldlabel: "Voucher No",
        //         placeholder: "Voucher No",
        //         classnames: "w-full h-full justify-center",
        //         is_figure: true,
        //     });
        //     fields = voucher_no
        // }
        return fields
    }

    create_cash_log(data) {
        let bg_color = null
        if (data.closed_at == null) bg_color = 'bg-red-100'
        else bg_color = 'bg-greed-100'
        return `
            <div class="${bg_color} w-full h-full flex items-center justify-start col-span-2 pl-4">${data.linked_fields.user.first_name} ${data.linked_fields.user.last_name}</div>
            <div class="${bg_color} w-full h-full flex items-center justify-start col-span-2">${data.opened_at || ''}</div>
            <div class="${bg_color} w-full h-full flex items-center justify-start col-span-2">${lite.utils.thousand_separator(data.cash_on_hand, 2 || '0.00')}</div>
        `;
    }

    create_supplier_row(data){
        return `
            <div class="w-full h-[30px] flex justify-between mt-2">
                <h4 class="font-semibold">${data.name}</h4>
                <small>${data.registration_type}</small>
            </div>
        `;
    }
    create_top_selling_item(data){
        return `
            <div class="w-full h-[30px] flex justify-between mt-2">
                <h4 class="font-semibold">${data.name}</h4>
                <small>${data.quantity_sold}</small>
            </div>
        `;
    }

    create_top_selling_item(data) {
        return `
            <div class="w-full h-full flex items-center justify-start pl-4">${data.item}</div>
            <div class="w-full h-full flex items-center justify-center">${lite.utils.thousand_separator(data.opening, 0 || '0')}</div>
            <div class="w-full h-full flex items-center justify-center">${lite.utils.thousand_separator(data.sold, 0 || '0')}</div>
            <div class="w-full h-full flex items-center justify-center">${lite.utils.thousand_separator(data.current, 0 || '0')}</div>
        `;
    }
}