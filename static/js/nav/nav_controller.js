export default class NavigationController {
    constructor() {
        this.keys = {
            sidebar: 'varyon_sidebar',
            accordion: 'varyon_accordion',
            sublink: 'varyon_sublink'
        }

        this.events = {
            namespace: '.navigationController',
            outsideNamespace: '.navigationControllerOutside'
        }

        this.cache()
        this.restore()
    }

    cache() {
        this.$doc = $(document)
        this.$sidebar = $('[data-sidebar]')
        this.$collapse = $('[data-collapse-toggle]')
        this.$modules = $('[data-modules]')
        this.$searchWrapper = $('[data-search-wrapper]')
        this.$searchPanel = $('[data-search]')
    }

    refresh() {
        this.cache()
    }

    getActiveClasses() {
        return {
            group: 'bg-default rounded-2xl shadow-[0_10px_30px_rgba(37,99,235,0.18)]',
            toggle: 'font-semibold text-white',
            sublink: 'font-semibold text-white translate-x-[-5px] bg-white/10 border-l-2 border-white'
        }
    }

    restore() {
        this.refresh()
        this.restoreSidebar()
        this.restoreAccordion()
        this.restoreSublink()
    }

    restoreSidebar() {
        const collapsed = localStorage.getItem(this.keys.sidebar) === 'true'
        this.$sidebar.toggleClass('collapsed', collapsed)
        this.$collapse.attr('aria-expanded', String(!collapsed))
    }

    restoreAccordion() {
        const accordion = localStorage.getItem(this.keys.accordion)
        if (!accordion) {
            return
        }

        const $toggle = $(`[data-accordion-toggle][data-accordion="${accordion}"]`)
        if (!$toggle.length) {
            return
        }

        this.openAccordion($toggle, false)
    }

    restoreSublink() {
        const sublink = localStorage.getItem(this.keys.sublink)
        if (!sublink) {
            return
        }

        const $link = $(`.sub-link[data-subroute="${sublink}"]`)
        if (!$link.length) {
            return
        }

        this.activateSublink($link)
    }

    bind() {
        this.refresh()

        const ns = this.events.namespace
        const outsideNs = this.events.outsideNamespace

        this.$collapse.off(`click${ns}`).on(`click${ns}`, () => {
            this.toggleSidebar()
        })

        this.$doc.off(`click${ns}`, '[data-accordion-toggle]')
            .on(`click${ns}`, '[data-accordion-toggle]', e => {
                e.preventDefault()
                e.stopPropagation()

                const $toggle = $(e.currentTarget)
                this.toggleAccordion($toggle)
            })

        this.$doc.off(`click${ns}`, '.sub-link')
            .on(`click${ns}`, '.sub-link', e => {
                const $link = $(e.currentTarget)
                this.activateSublink($link)
            })

        this.$doc.off(`click${ns}`, '[data-modules-toggle]')
            .on(`click${ns}`, '[data-modules-toggle]', e => {
                e.stopPropagation()
                this.toggleModules()
            })

        this.$doc.off(`click${ns}`, '[data-search-btn]')
            .on(`click${ns}`, '[data-search-btn]', e => {
                e.stopPropagation()
                this.toggleSearch()
            })

        this.$doc.off(`click${outsideNs}`)
            .on(`click${outsideNs}`, e => {
                const target = $(e.target)

                if (this.shouldCloseModules(target)) {
                    this.closeModules()
                }

                if (this.shouldCloseSearch(target)) {
                    this.closeSearch()
                }
            })
    }

    toggleSidebar() {
        this.$sidebar.toggleClass('collapsed')
        const collapsed = this.$sidebar.hasClass('collapsed')
        localStorage.setItem(this.keys.sidebar, collapsed)
        this.$collapse.attr('aria-expanded', String(!collapsed))
    }

    toggleAccordion($toggle) {
        const $content = $toggle.next('.nav-sub')
        const key = $toggle.data('accordion')
        const isOpen = $content.is(':visible')

        this.closeAllAccordions()

        if (!isOpen) {
            this.openAccordion($toggle, true)
            if (key) {
                localStorage.setItem(this.keys.accordion, key)
            }
        } else {
            localStorage.removeItem(this.keys.accordion)
        }
    }

    closeAllAccordions() {
        const activeClasses = this.getActiveClasses()
        $('.nav-sub').stop(true, true).slideUp(180)
        $('.chevron').removeClass('rotate-180')
        $('.nav-group').removeClass(activeClasses.group)
        $('.nav-toggle').removeClass(activeClasses.toggle)
    }

    openAccordion($toggle, animate = true) {
        const activeClasses = this.getActiveClasses()
        const $group = $toggle.closest('.nav-group')
        const $content = $toggle.next('.nav-sub')

        $group.addClass(activeClasses.group)
        $toggle.addClass(activeClasses.toggle)
        $toggle.find('.chevron').addClass('rotate-180')

        if (animate) {
            $content.stop(true, true).slideDown(180)
        } else {
            $content.show()
        }
    }

    activateSublink($link) {
        const activeClasses = this.getActiveClasses()
        $('.sub-link').removeClass(activeClasses.sublink)

        $link.addClass(activeClasses.sublink)

        const $group = $link.closest('.nav-group')
        const $toggle = $group.find('[data-accordion-toggle]').first()
        const key = $toggle.data('accordion')

        this.closeAllAccordions()
        this.openAccordion($toggle, false)

        localStorage.setItem(this.keys.sublink, $link.data('subroute'))
        if (key) {
            localStorage.setItem(this.keys.accordion, key)
        }
    }

    shouldCloseModules($target) {
        if (!this.$modules.length) {
            return false
        }

        return !$target.closest('[data-modules], [data-modules-toggle]').length
    }

    shouldCloseSearch($target) {
        if (!this.$searchWrapper.length && !this.$searchPanel.length) {
            return false
        }

        return !$target.closest('[data-search-wrapper], [data-search], [data-search-btn]').length
    }

    toggleModules() {
        const willOpen = this.$modules.hasClass('hidden')
        this.$modules.toggleClass('hidden')

        if (willOpen) {
            this.closeSearch()
        }
    }

    closeModules() {
        this.$modules.addClass('hidden')
    }

    toggleSearch() {
        const willOpen = this.$searchPanel.hasClass('hidden')
        this.$searchPanel.toggleClass('hidden')

        if (willOpen) {
            this.closeModules()
        }
    }

    closeSearch() {
        this.$searchPanel.addClass('hidden')
    }
}
