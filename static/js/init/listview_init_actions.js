export default class Listview_Actions{
    constructor(){
        this.scroll_percentage = 0
        this.has_scrolled_to_70 = false;
        this.has_reached_the_end = false;
        this.last_scroll_height = 0
        this.ini_on_list_scroll_event()
    }

    ini_on_list_scroll_event(){
        document.addEventListener('scroll', async e => {
            if ($(e.target).hasClass("lbody")) {
                var $el = $(e.target);
                var scrollTop = $el.scrollTop();
                var scrollHeight = $el[0].scrollHeight;
                var clientHeight = $el[0].clientHeight;

                // Calculate the percentage of scrollable content that has been scrolled
                this.scroll_percentage = (scrollTop / (scrollHeight - clientHeight)) * 100;

                // Trigger log once when 70% scrolled
                if (this.scroll_percentage >= 80 && !this.has_scrolled_to_70) {
                    this.has_scrolled_to_70 = true;
                    await this.prefetch_next_listview_content()
                }

                // Trigger log again when the end is reached
                if (this.scroll_percentage >= 100 && !this.has_reached_the_end) {
                    // console.log('You have reached the end of the content!', lite.listview_controller);
                    this.has_reached_the_end = true;
                    this.last_scroll_height = $el[0].scrollHeight
                }
                // console.log($el[0].scrollHeight)
            }
        }, true);
    }

    async prefetch_next_listview_content(){
        if(lite.listview_controller.current_page && lite.listview_controller.total_pages &&lite.listview_controller.current_page < lite.listview_controller.total_pages){
            lite.listview_controller.current_page += 1
            // const loader_id = lite.alerts.loading_toast({
            //     title: `Adding more rows`, 
            //     message:`Auto Expanding list rows.`
            // })
            $(".lbody").addClass("loading-more-content")
            const {status} = await lite.listview_controller.populate_list(false)
            // lite.alerts.destroy_toast(loader_id)
            $(".lbody").removeClass("loading-more-content")
            if (status && lite.status_codes.ok){
                this.has_scrolled_to_70 = false
            }
        }
    }
}