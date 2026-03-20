// export default class NavigationController {
//     constructor() {
//         this.keys = {
//             sidebar: 'varyon_sidebar',
//             accordion: 'varyon_accordion',
//             sublink: 'varyon_sublink'
//         }

//         this.cache()
//         this.restore()
//         this.bind()
//     }

//     cache() {
//         this.$doc = $(document)
//         this.$sidebar = $('[data-sidebar]')
//         this.$collapse = $('[data-collapse-toggle]')
//         this.$modules = $('[data-modules]')
//         this.$modulesToggle = $('[data-modules-toggle]')
//         this.$searchBtn = $('[data-search-btn]')
//         this.$SearchWrapper = $('[data-search-wrapper]')
//         this.$searchPinnal = $('[data-search]')
//     }
    
//     restore() {
//         const collapsed = localStorage.getItem(this.keys.sidebar) === 'true'
//         this.$sidebar.toggleClass('collapsed', collapsed)

//         const accordion = localStorage.getItem(this.keys.accordion)
//         if (accordion) {
//             const $toggle = $(`[data-accordion-toggle][data-accordion="${accordion}"]`)
//             const $content = $toggle.next('.nav-sub')
//             $content.show()
//             $toggle.find('.chevron').addClass('rotate-180')
//             $toggle.closest('.nav-group').addClass('bg-default/10 rounded-md')
//         }

//         const sublink = localStorage.getItem(this.keys.sublink)
//         if (sublink) {
//             const $link = $(`.sub-link[data-subroute="${sublink}"]`)
//             if ($link.length) {
//                 $link.addClass('font-semibold text-default translate-x-[-5px]')
//                 const $group = $link.closest('.nav-group')
//                 $group.find('.nav-sub').show()
//                 $group.find('.chevron').addClass('rotate-180')
//                 $group.addClass('bg-default/10 rounded-md')
//             }
//         }
//     }

//     bind() {
//         this.$collapse.on('click', () => {
//             this.$sidebar.toggleClass('collapsed')
//             localStorage.setItem(this.keys.sidebar, this.$sidebar.hasClass('collapsed'))
//         })

//         this.$doc.on('click', '[data-accordion-toggle]', e => {
//             e.preventDefault()
//             e.stopPropagation()

//             const $toggle = $(e.currentTarget)
//             const $content = $toggle.next('.nav-sub')
//             const key = $toggle.data('accordion')
//             const isOpen = $content.is(':visible')

//             $('.nav-sub').slideUp(200)
//             $('.chevron').removeClass('rotate-180')
//             $('.nav-group').removeClass('bg-default/10 rounded-md')
//             localStorage.removeItem(this.keys.accordion)

//             if (!isOpen) {
//                 $content.slideDown(200)
//                 $toggle.find('.chevron').addClass('rotate-180')
//                 $toggle.closest('.nav-group').addClass('bg-default/10 rounded-md')
//                 localStorage.setItem(this.keys.accordion, key)
//             }
//         })

//         this.$doc.on('click', '.sub-link', e => {
//             const $link = $(e.currentTarget)

//             $('.sub-link').removeClass('font-semibold text-default translate-x-[-5px]')

//             $link.addClass('font-semibold text-default translate-x-[-5px]')

//             const $group = $link.closest('.nav-group')
//             $group.find('.nav-sub').show()
//             $group.find('.chevron').addClass('rotate-180')
//             $group.addClass('bg-default/10 rounded-md')

//             localStorage.setItem(this.keys.sublink, $link.data('subroute'))
//             const key = $group.find('[data-accordion-toggle]').data('accordion')
//             if (key) localStorage.setItem(this.keys.accordion, key)
//         })

//         this.$modulesToggle.on('click', e => {
//             e.stopPropagation()
//             this.toggleModules()
//         })

//         this.$searchBtn.on('click', e => {
//             e.stopPropagation()
//             this.toggleSearch()
//         })

//         this.$doc.on('click', e => {
//             const t = e.target

//             if (this.$modules.length && !this.$modules.is(t) && !this.$modules.has(t).length && !this.$modulesToggle.is(t)) {
//                 this.closeModules()
//             }

//             if (this.$SearchWrapper.length && !this.$SearchWrapper.is(t) && !this.$SearchWrapper.has(t).length && !this.$searchBtn.is(t)) {
//                 this.closeSearch()
//             }
//         })
//     }

//     toggleModules() {
//         this.$modules.toggleClass('hidden')
//     }

//     closeModules() {
//         this.$modules.addClass('hidden')
//     }

//     toggleSearch() {
//         this.$searchPinnal.toggleClass('hidden')
//     }

//     closeSearch() {
//         this.$searchPinnal.addClass('hidden')
//     }
// }

export default class NavigationController {
    constructor() {
        this.keys = {
            sidebar: 'varyon_sidebar',
            accordion: 'varyon_accordion',
            sublink: 'varyon_sublink'
        }

        this.cache()
        this.restore()
    }

    cache() {
        this.$doc = $(document)
        this.$sidebar = $('[data-sidebar]')
        this.$collapse = $('[data-collapse-toggle]')
        this.$modules = $('[data-modules]')
        this.$SearchWrapper = $('[data-search-wrapper]')
        this.$searchPinnal = $('[data-search]')
    }

    restore() {
        // Sidebar collapse
        const collapsed = localStorage.getItem(this.keys.sidebar) === 'true'
        this.$sidebar.toggleClass('collapsed', collapsed)

        // Restore accordion
        const accordion = localStorage.getItem(this.keys.accordion)
        if (accordion) {
            const $toggle = $(`[data-accordion-toggle][data-accordion="${accordion}"]`)
            const $content = $toggle.next('.nav-sub')
            $content.show()
            $toggle.find('.chevron').addClass('rotate-180')
            $toggle.closest('.nav-group').addClass('bg-default/10 rounded-md')
        }

        // Restore active sublink
        const sublink = localStorage.getItem(this.keys.sublink)
        if (sublink) {
            const $link = $(`.sub-link[data-subroute="${sublink}"]`)
            if ($link.length) {
                $link.addClass('font-semibold text-default translate-x-[-5px]')
                const $group = $link.closest('.nav-group')
                $group.find('.nav-sub').show()
                $group.find('.chevron').addClass('rotate-180')
                $group.addClass('bg-default/10 rounded-md')
            }
        }
    }

    bind() {
        // Sidebar collapse
        this.$collapse.on('click', () => {
            this.$sidebar.toggleClass('collapsed')
            localStorage.setItem(this.keys.sidebar, this.$sidebar.hasClass('collapsed'))
        })

        // Accordion toggle (delegated)
        this.$doc.on('click', '[data-accordion-toggle]', e => {
            e.preventDefault()
            e.stopPropagation()

            const $toggle = $(e.currentTarget)
            const $content = $toggle.next('.nav-sub')
            const key = $toggle.data('accordion')
            const isOpen = $content.is(':visible')

            // Close all accordions
            $('.nav-sub').slideUp(200)
            $('.chevron').removeClass('rotate-180')
            $('.nav-group').removeClass('bg-default/10 rounded-md')
            localStorage.removeItem(this.keys.accordion)

            // Open current if it was closed
            if (!isOpen) {
                $content.slideDown(200)
                $toggle.find('.chevron').addClass('rotate-180')
                $toggle.closest('.nav-group').addClass('bg-default/10 rounded-md')
                localStorage.setItem(this.keys.accordion, key)
            }
        })

        // Sublink click (delegated)
        this.$doc.on('click', '.sub-link', e => {
            const $link = $(e.currentTarget)

            // Remove all previous active
            $('.sub-link').removeClass('font-semibold text-default translate-x-[-5px]')

            // Set active
            $link.addClass('font-semibold text-default translate-x-[-5px]')

            // Ensure parent accordion stays open
            const $group = $link.closest('.nav-group')
            $group.find('.nav-sub').show()
            $group.find('.chevron').addClass('rotate-180')
            $group.addClass('bg-default/10 rounded-md')

            // Persist sublink and accordion
            localStorage.setItem(this.keys.sublink, $link.data('subroute'))
            const key = $group.find('[data-accordion-toggle]').data('accordion')
            if (key) localStorage.setItem(this.keys.accordion, key)
        })

        // Modules toggle (delegated)
        this.$doc.on('click', '[data-modules-toggle]', e => {
            e.stopPropagation()
            this.toggleModules()
        })

        // Search toggle (delegated)
        this.$doc.on('click', '[data-search-btn]', e => {
            e.stopPropagation()
            this.toggleSearch()
        })

        // Close modules/search on outside click
        this.$doc.on('click', e => {
            const t = e.target

            // Modules
            if (this.$modules.length && !this.$modules.is(t) && !this.$modules.has(t).length &&
                !$(t).is('[data-modules-toggle]')) {
                this.closeModules()
            }

            // Search
            if (this.$SearchWrapper.length && !this.$SearchWrapper.is(t) && !this.$SearchWrapper.has(t).length &&
                !$(t).is('[data-search-btn]')) {
                this.closeSearch()
            }
        })
    }

    // -------------------------
    // Modules / Search
    // -------------------------
    toggleModules() {
        this.$modules.toggleClass('hidden')
    }

    closeModules() {
        this.$modules.addClass('hidden')
    }

    toggleSearch() {
        this.$searchPinnal.toggleClass('hidden')
    }

    closeSearch() {
        this.$searchPinnal.addClass('hidden')
    }
}
