export default class Retail_HTML_Generator{
    constructor(){

    }

    create_pos_stock_list_item(data){
        return `
            <div id="${data?.barcode || data?.item_code}" class="stock-item-wrapper w-full min-h-[260px] max-h-[300px] bg-white rounded-md flex flex-col items-center justify-center border border-orange-400 border-dotted intro-y">
                <div class="flex items-center justify-center h-[50%] w-[80%] mt-3">
                    <img class="stock-item-img w-full h-full object-contain" src="${data?.product_img || "/static/images/others/generic_store.jpeg"}" alt="">
                </div>
                <div class="stock-item-name font-semibold mt-2 w-[90%] truncate overflow-ellipsis text-center text-13 border-t border-dotted pb-2 mt-1"> ${data?.name} </div>
                <div class="stock-item-price font-semibold mt-2 w-[90%] truncate overflow-ellipsis text-center text-11 text-orange-500"> ${lite.utils.currency(data?.unit_price,2,lite?.defaults?.currency?.symbol)} </div>
                <button class="add-stock-item-to-cart flex items-center mb-3 justify-center rounded-md btn bg-secondary_color text-theme_text_color w-[80%] h-[30px] mt-5 text-11">
                    <span class="material-symbols-outlined"> add_circle </span>
                    Add To Cart
                </button>
            </div>
        `
    }

    create_stock_cart_item(data){
        return `
            <div id="${data?.item_code}" class="cart-stock-item w-full intro-x rounded-md bg-gray-50/20 border-default/50 border border-dotted h-[60px] px-2 mb-3">
                <div class="w-full h-full grid grid-cols-12 gap-x-2">
                    <div class="w-full h-[90%] flex items-center justify-center col-span-1">
                        <img class="stock-item-img w-full h-full object-contain" src="${data?.product_img}" alt="">
                    </div>
                    <div class="w-full h-full flex items-start justify-center flex-col col-span-5 truncate overflow-ellipsis">
                        <span class="font-bold text-13">${data?.item_name}</span>
                        <small class="text-gray-800 font-semibold">QTY: <span class="cart-stock-item-qty">${data?.qty || 0}</span></small>
                    </div>
                    <div class="w-full h-full flex items-center justify-end col-span-6">
                        <div class="">
                            <div class="cart-stock-item-inclusive-amount font-bold">${data?.inclusive_total_amount || 0}</div>
                            <small class="text-orange-700 cart-stock-item-discount font-semibold">Disc: 255.99</small>
                        </div>
                        <button class="remove-item_from_cart flex items-center justify-center rounded-md bg-orange-700 text-theme_text_color ml-3">
                            <span class="material-symbols-outlined text-19"> close </span>
                        </button>
                    </div>
                </div>
            </div>
        `
    }
}