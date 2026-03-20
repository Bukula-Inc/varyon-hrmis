
import Web_HTML_Generator from "../page/html/web_html_generator.js"
import HTML_Builder from "../page/html/html_builder.js"
import Careers from "./careers.js"
import Integrations from "./integrations.js"
import Onboarding from "./onboarding.js"
import About from "./about.js"
import Job_Offer from "./job_offer.js"
import Upload_medical_clearance from "./upload_medical_clearance.js"
import Appointment_Letter from "./appointment_letter.js"
export default class Web{
    constructor(){
        this.$hero_title = $(".hero-title")
        this.$hero_message = $(".hero-message")
        this.$active_menu_items = $(".active-menu-item")
        this.$mobile_menu_items = $(".mobile-nav-menus")
        this.$mobile_menus_btn = $("#mobile-menus-btn")
        this.html_generator = new HTML_Builder()
        this.generator = new Web_HTML_Generator()
        this.page = lite.utils.get_current_app()
        this.init_page()
        this.careers = new Careers ()
        this.integrations = new Integrations()
        this.about = new About()
        this.onboarding = new Onboarding()
        this.upload_medical_clearance = new Upload_medical_clearance ()
        // this.Job_Offer =new Job_Offer()
        this.Appointment_Letter =new Appointment_Letter()
    }

    async init_page(){
        this.init_nav_controller()
        const {status, data, error_message} = await lite.connect.x_fetch("web_content")
        lite.utils.init_dashboard(true)
        if(status === lite.status_codes.ok){
            this.web_content = data
            this.config =  this.web_content.billing_config
            this.license = this.web_content.license
            this.currency = this.config.linked_fields?.billing_currency
        }   
        switch (this.page) {
            case "onboarding":
                this.onboarding.init(this.web_content)
                break;
            case "integrations":
                this.integrations.init()
                break;
            case "about":
                this.about.init()
                break;
            case "careers":
                this.careers.init()
                break;
            case 'upload_medical_clearance':
                this.upload_medical_clearance.init ()
                break;
            default:
                break;
        }
    }



    init_nav_controller(){
        let app = lite.utils.get_current_app()
        this.$active_menu_items?.addClass("hidden")
        // activate nav item
        if(!app) app = "home"
        $(`.nav-item-wrapper[item=${lite.utils.lower_case(app)}`).find(".active-menu-item").removeClass("hidden")
        if(app !== "home"){
            $("nav").addClass("bg-default")
        }
        else{
            if($(window).width() > 720){
                $("nav").removeClass("bg-default lg:xl:bg-default")
            }
            $(window).on('scroll', e=>{
                const scroll_position = $(window).scrollTop()
                if(scroll_position >= 190){
                    $("nav").addClass("bg-default lg:xl:bg-default")
                }
                else if($(window).width() > 720){
                    $("nav").removeClass("bg-default lg:xl:bg-default")
                }
            })
        }
        this.enable_menus_btn()
        this.enable_sliders()
        
    }

    enable_menus_btn(){
        this.$mobile_menus_btn?.off("click").click(e=>{
            e.preventDefault()
            if(!this.$mobile_menus_btn?.hasClass("expanded")){
                this.$mobile_menus_btn?.addClass("expanded")
                this.$mobile_menu_items?.removeClass("hidden")
                $("body").addClass("overflow-hidden")
            }
            else{
                this.$mobile_menus_btn?.removeClass("expanded")
                this.$mobile_menu_items?.addClass("hidden")
                $("body").removeClass("overflow-hidden")
            }
        })
    }

    enable_sliders(){
        this.slide_index = 0
        this.slider_context = [
            {
                title:"Eliminate manual processes and simplify your complexity.",
                message:"Automate manual or routine tasks, implement smarter workflows and gain efficiency"
            },
            {
                title:"Empowering Micro & Medium Enterprises in Africa.",
                message:"Startapp ERP is a system used to manage and intergrate the important parts of the business enterprise. It is important to your business."
            },
            {
                title:"Varyon is built to simplify your business complexity.",
                message:"Startapp ERP is a system used to manage and intergrate the important parts of the business enterprise. It is important to your business."
            },
        ]
        // enable swiper
        const swiper = new Swiper('.swiper', {
            effect: 'cube', // Options: 'slide', 'fade', 'cube', 'coverflow', 'flip'
            spaceBetween: 30,
            direction: 'horizontal',
            loop: true,
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
        });

        this.$hero_title.html(`<div class="intro-y hero-text transition duration-1000">${this.slider_context[0].title}</div>`)
        this.$hero_message.html(`<div class="intro-y hero-text transition duration-1000">${this.slider_context[0].message}</div>`)
        setInterval(() => {
            if(this.slide_index == 2)
                this.slide_index = 0
            else this.slide_index ++
            this.$hero_title.html(`<div class="intro-y">${this.slider_context[this.slide_index].title}</div>`)
            this.$hero_message.html(`<div class="intro-y">${this.slider_context[this.slide_index].message}</div>`)
        }, 5505);
    }

    
}