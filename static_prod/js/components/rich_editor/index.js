
export default class Rich_Editor{
    constructor(){
    }
    init_rich_editors(){
        const rich_editor = $('textarea[type="rich"]')
        
        if(!lite.utils.is_empty_array(rich_editor)){
            $.each(rich_editor,(_,re)=>{
                const lite_id = lite.utils.get_attribute(re,"lite-id"), height = lite.utils.get_attribute(re,"height") || 200
                $(re).summernote({
                    height: parseInt(height),
                    toolbar: [
                        ['style', ['bold', 'italic', 'underline', 'clear']],
                        ['font', ['strikethrough', 'superscript', 'subscript']],
                        ['fontsize', ['fontsize']],
                        ['color', ['forecolor', 'backcolor']],
                        ['para', ['ul', 'ol', 'paragraph',"table"]],
                        ['insert', ['picture']],
                    ]
                })
                $(re).attr("initialized",true)
                
                if(!lite.rich_editor_values[lite_id]){
                    lite.rich_editor_values[lite_id] = {field:re, value:""}
                }
                else {
                    lite.rich_editor_values[lite_id].field = re
                }
                const value = lite.rich_editor_values[lite_id]?.value
                if(value){ $(re).summernote('code', value); }
            })
            $(".note-editor.note-frame .btn.btn-primary.note-btn.note-btn-primary,.note-toolbar, .note-toolbar  button").addClass("bg-default")
        }
    }

    get_content(field){
        const lite_id = lite.utils.get_attribute(field,"lite-id")
        return $(lite.rich_editor_values[lite_id]?.field).summernote('code')
    }

    // get_text(field){
    //     return $(field).summernote('getText') || ''
    // }
}