import './src_min/ace'
import './src_min/ext-beautify'
export default class Code_Editor{
    constructor(){
        this.code_fields = {}
        this.preloaded_code = {}
        this.beautify_options = {
            indent_size: 4,
            indent_char: '\t',
            unformatted: ['a', 'sub', 'sup', 'b', 'i', 'u'],
            wrap_line_length: 0
          };
    }
    init_code_editors(){
        delete this.code_fields
        this.code_fields = {}
        const code_fields = $('.lite-code-editor')
        if(!lite.utils.is_empty_array(code_fields)){
            $.each(code_fields,(i,f)=>{
                const 
                    id = lite.utils.get_attribute(f,"id"),
                    fieldname = lite.utils.get_attribute(f,"fieldname"),
                    lite_id = lite.utils.get_attribute(f,"lite-id"),
                    language = lite.utils.lower_case(lite.utils.get_attribute(f,"language") || 'html'),
                    theme = lite.utils.get_attribute(f,"theme") || 'tomorrow'
                    this.code_fields[lite_id] = ""
                if(lite_id && language){
                    $(f).attr("id",lite_id)
                    ace.config.set('basePath', '/static/js/components/code_editor/src_min')
                    const editor = ace.edit(lite_id)
                    editor.setTheme(`ace/theme/${theme}`)
                    editor.session.setMode(`ace/mode/${language}`)
                    editor.session.setValue(lite.preloaded_code[lite_id] || "")
                    editor.setOptions({});
                    // const beautify = ace.require("ace/ext/beautify");
                    // beautify.beautify(editor.session, this.beautify_options)
                    editor.getSession().on('change', (delta) => this.code_fields[lite_id] = editor.getSession().getValue() || "")
                }
            })
        }
    }

    get_editor_code(id){
        return this.code_fields[id] || ""
    }
}