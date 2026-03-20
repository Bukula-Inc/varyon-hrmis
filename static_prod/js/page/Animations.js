class Animations {
    constructor(config) {
    }

    get_element(class_name) {
        const el = ($(`#${class_name}`) && $(`#${class_name}`).length > 0 ? $(`#${class_name}`) : $(`.${class_name}`)) || null
        return el !== null && el.length > 0 ? el : null
    }
    add_element_class(el, class_name) {
        $(el).addClass(class_name)
    }
    remove_element_class(el, class_name) {
        $(el).removeClass(class_name)
    }

    init_card_slider(cards_wrapper, cards_class_name, prev_btn, next_btn, config = {
        allow_rotation: true,
        auto_slide: false
    }) {
        const cls = this
        this.card_wrapper_name = cards_wrapper
        this.card_wrapper = this.get_element(cards_wrapper?.trim())
        this.cards = this.get_element(cards_class_name?.trim())
        this.cards_prev = this.get_element(prev_btn?.trim())
        this.cards_next = this.get_element(next_btn?.trim())
        this.auto_slide = config?.auto_slide || false
        this.allow_rotation = config?.allow_rotation || true
        this.allow_slide_next = true
        if (this.card_wrapper && this.cards && this.cards_prev) {
            this.inclue_card_style_classes()
            $(this.card_wrapper).mouseenter(() => this.allow_slide_next = false).mouseleave(() => this.allow_slide_next = true)
            this.cards_next && this.cards_next.click(() => this.on_card_slide('right'))
            this.cards_prev && this.cards_prev.click(() => this.on_card_slide('left'))
        }
        else console.error("ANIMATIONS ERROR:: Please provide required parameters for Card Animations to work!!")
    }

    inclue_card_style_classes() {
        this.card_wrapper.addClass('ani-cards-wrapper')
        this.add_element_class(this.cards, 'ani-card')
        this.add_element_class(this.cards[0], 'active')
        this.remove_element_class(this.cards, 'hidden')
        this.cards.map((_, card) => {
            $(card).css({ zindex: this.cards.length - _ })
        })
        this.allow_rotation && this.add_element_class(this.cards, 'rotate')
        this.auto_slide && this.auto_run_card_flip()

    }
    update_cards() {
        this.cards = this.get_element(this.card_wrapper_name).children()
        this.cards.map((_, card) => {
            $(card).css({ zindex: this.cards.length - _ })
        })
    }
    on_card_slide(direction) {
        const cls = this
        cls.cards.addClass('seperate')
        let active = $('.ani-card.active')
        setTimeout(function () {
            cls.card_wrapper.append(active)
            setTimeout(() => {
                cls.cards.removeClass('seperate last').addClass('overwrap')
                $(active).removeClass('active overwrap').addClass('last')
                cls.update_cards()
                $(cls.cards[0]).addClass('active ani-selection')
                $(active).removeClass('seperate')
                setTimeout(() => {
                    $(cls.cards[0]).removeClass('ani-selection')
                    cls.update_cards()
                }, 200);
            }, 40);
        }, 300)
    }
    auto_run_card_flip(interval = 3000) {
        setInterval(() => {
            this.allow_slide_next && this.on_card_slide('right')
        }, interval);
    }
}

// new Animations().init_card_slider('c_wrapper', 'c', 'prev', 'nxt', {
//     auto_slide: true
// })

export default Animations