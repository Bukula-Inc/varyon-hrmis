import { on_approval_preload } from '../../overrides/form/staff/core.js';
export default {
    setup: {
        info_form_id: 'approval-info',
        title: "Document Approval",
        model: "Approval",
        allow_update:false,
        allow_submit:false,
        allow_delete:false,
        allow_disable:false,
        allow_duplicate:false,
        allow_download:false,
        allow_print:false,
        allow_preview:false
    },
    form_customizer: on_approval_preload,
    fields: [],
}