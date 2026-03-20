
export default class Lite_File_Picker{
    constructor(file_types=[],min_size=1,max_size=102400, convert_to_binary=false){
        this.file_types = file_types
        this.min_size = min_size
        this.max_size = max_size
        this.byte_to_mbs = 1
        // this.byte_to_mbs = 1048576
        this.convert_to_binary = convert_to_binary
        this.lite_form_files = {}
        this.processed_form_files = {}
        this.on_file_changed = []
    }
    create_file_attachment_option(file_name, total_files=1, idx=0, url, add_download=false, is_processed=false, add_remove_btn=true){
        return `
            <div  filename="${file_name}" is-processed="${is_processed}" class="file-row relative w-full py-1 grid grid-cols-10 ${idx === 0? "border-t":""} ${idx !== total_files - 1 ? "border-b":""}  border-default/50 border-dotted pb-1"> 
                <span class="col-span-1 w-[15px] h-[15px] text-10 bg-default text-white rounded-full mr-1 flex items-center justify-center">${idx+1}</span>
                <div class="col-span-${add_download && add_remove_btn?7:8} text-10 w-full whitespace-normal text-left">${file_name}</div>
                <div class="col-span-${add_download && add_remove_btn?2:1} grid grid-cols-${add_download && is_processed && add_remove_btn ? 2 : 1} gap-x-2 ">
                    ${
                        add_download ? `
                            <a href="${url}"  filename="${file_name}" class="w-full max-w-[40px] h-[25px] bg-default text-white flex items-center justify-center rounded-md" > 
                                <span class="material-symbols-outlined"> download </span>
                            </a>
                        `: ''
                    }
                    ${
                        add_remove_btn ? `
                            <button filename="${file_name}" is-processed="${is_processed}" file-url="${url}" class="w-full max-w-[40px]  h-[25px] remove-single-field-file bg-orange-300 text-orange-700 rounded-md flex items-center justify-center " >
                                <span class="material-symbols-outlined"> close </span>
                            </button>
                        `: ''
                    }
                    
                </div>
            </div>
        `
    }
    init_file_picker(on_file_changed=null,cls=null){
        if(on_file_changed)
            this.on_file_changed.push({fun:on_file_changed,cls:cls})
        this.cls = cls
        const file_fields = $('.lite-field.lite-file-picker')
        if(lite.utils.array_has_data(file_fields)){
            $.each(file_fields, (_,f)=>{
                const lite_id = lite.utils.unique(70), value = $(f)?.attr("value")
                this.lite_form_files[lite_id] = { field:f, field_id:lite_id, files:[] }
                $(f).attr("lite-id",lite_id)
                if(value){
                    this.processed_form_files[lite_id] = value
                }
            })
        }
    }

    process_file_content(field){
        const lite_id = $(field)?.attr("lite-id")
        let file_name = ""
        const max = lite.utils.string_to_int($(field).attr("max-length") || 5)
        if(!this.lite_form_files[lite_id]){
            this.lite_form_files[lite_id] = {field:field, files:[]}
        }
        this.lite_form_files[lite_id].files = []
        const files = $(field)?.prop("files")
        if(lite.utils.array_has_data(files)){
            if(!$(field)?.prop("multiple") && files.length > 1){
                lite.alerts.toast({
                    toast_type:lite.status_codes.unprocessable_entity,
                    title:"Too many files pasted",
                    message:"You can only add/drop 1 file!"
                })
            }
            else if(files.length > max){
                lite.alerts.toast({
                    toast_type:lite.status_codes.unprocessable_entity,
                    title:"Too many files pasted",
                    message:`You can only add/drop up to ${max} files!`
                })
                $(field).parents("label")?.find(".file-title")?.html($(field).parents("label")?.find(".file-title")?.attr("arial-title"))
            }
            else if(files.length > 10){
                lite.alerts.toast({
                    toast_type:lite.status_codes.unprocessable_entity,
                    title:"Too many files pasted",
                    message:`You can only add/drop up to ${10} files!`
                })
                $(field).parents("label")?.find(".file-title")?.html($(field).parents("label")?.find(".file-title")?.attr("arial-title"))
            }
            else{
                $.each(files,(_,fl)=>{
                    file_name += this.create_file_attachment_option(fl?.name, files, _ ,null,false,false,true)
                    this.lite_form_files[lite_id].files.push({
                        file_name: fl?.name?.substring(0, 30),
                        file_type: fl?.type?.split("/")[0],
                        file_size: fl?.size / this.byte_to_mbs,
                        file_ext : fl?.type?.split("/")[1],
                        file: fl,
                        has_new_file:true
                    })
                })
            }
        }
        $(field).parents("label")?.find(".file-title")?.html(file_name)
        this.handle_file_change(field, lite_id,  this.lite_form_files[lite_id].files)
        // this.handle_remove_file_from_list()
    }


    handle_file_change(field, lite_id, values){
        if(this.on_file_changed && lite.utils.array_has_data(this.on_file_changed)){
            $.each(this.on_file_changed,(_,ofc)=>{
                ofc?.fun({
                    field: field,
                    lite_id: lite_id,
                    files: values
                }, ofc?.cls)
            })
        }
    }

    clear_input_file_content(field){
        const lite_id = $(field)?.attr("lite-id")
        this.lite_form_files[lite_id].files = []
        
        $(field).parents("label")?.find(".file-title")?.html($(field).parents("label")?.find(".file-title")?.attr("arial-title"))
        this.handle_file_change(field, lite_id,  this.lite_form_files[lite_id].files)
    }

    async remove_file_from_file_list(btn){
        const el = $(btn?.currentTarget), lite_id = el?.parents("label")?.find("input[type='file']")?.attr("lite-id"), file_row = el?.parents(".file-row"), url = el.attr("file-url")
        if(el?.attr("is-processed") === "false"){
            file_row?.remove()
        }
        else if(url){
            file_row?.removeClass("grid")?.addClass("flex items-center justify-center")
            file_row?.append(lite.utils.generate_loader({
                classnames:"deletion-loader transition duration-1000 absolute flex-row flex items-center justify-center h-full w-full top-0 left-0 bg-orange-400 text-white rounded-md",
                text_classnames:"ml-2",
                light_mode:true,
                size:20, text:`Deleting File`
            }))
            const {status, data, error_message} = await lite.connect.core("delete_files",{"files": [url]})
            if(status === lite.status_codes.ok){
                file_row.find(".deletion-loader")?.removeClass("bg-orange-400").addClass("bg-default").html(`
                    <span class="material-symbols-outlined text-20 pr-2 intro-x"> task_alt </span>
                    <span class="intro-x">File Deleted Successfully.</span>
                `)
                let new_files = ""
                $.each(this.processed_form_files[[lite_id]]?.split(" &== "),(_,file)=>{
                    if(url?.trim() !==file?.trim()){
                        new_files += `${file} &== `
                    }
                }) 
                this.processed_form_files[[lite_id]] = lite.utils.remove_last_characters(new_files,4)?.trim()
                lite?.form_controller?.update_doc(false)
                setTimeout(() => { file_row?.remove() }, 2000);
                if(new_files === ""){
                    file_row.parents("label").find(".file-title").html(file_row.parents("label").find(".file-title")?.attr("arial-title"))
                }
            } 
            else{
                file_row.find(".deletion-loader")?.html(`
                    <span class="material-symbols-outlined text-20 pr-2 intro-x"> block </span>
                    <span class="intro-x">File Deletion Failed!</span>
                `)
                setTimeout(() => {
                    file_row?.find(".deletion-loader")?.remove()
                    file_row?.addClass("grid")?.removeClass("flex items-center justify-center")
                }, 2000);
            }
        }
        else{
            lite.alerts.toast({
                toast_type:lite.status_codes.unprocessable_entity,
                title:"File URL Missing",
                message:"The url for the file being deleted is not found!"
            })
        }
        
    }

    get_file_content(field){
        return this.lite_form_files[$(field)?.attr("lite-id")] || {}
    }

    get_processed_file_content(field){
        return this.processed_form_files[$(field)?.attr("lite-id")] || ""
    }

    async upload_form_files(params){
        let files = {}
        if(this.lite_form_files && lite.utils.object_has_data(this.lite_form_files)){
            $.each(lite.utils.get_object_keys(this.lite_form_files),(_,key)=>{
                if(this.lite_form_files[key] && this.lite_form_files[key]?.files && lite.utils.array_has_data(this.lite_form_files[key]?.files)){
                    let field_files = []
                    $.each(this.lite_form_files[key]?.files,(_,fl)=>{
                        field_files.push(fl.file)
                    })
                    if(lite.utils.array_has_data(field_files)){
                        files[key] = field_files
                    }
                }
            })
        }
        if(lite.utils.object_has_data(files)){
            const loader_id = lite.alerts.loading_toast({ title: "Uploading Form Files", message:`Please wait while files get uploaded.`})
            const {status, data} = await lite.connect.upload({files: files})
            lite.alerts.destroy_toast(loader_id)
            if(status == lite.status_codes.ok){
                if(lite.utils.object_has_data(data)){
                    $.each(lite.utils.get_object_keys(data),(_,fl)=>{
                        if(lite.utils.array_has_data(data[fl])){
                            let processed_name = ""
                            $.each(data[fl],(_,processed)=>{
                                processed_name += `${processed} &== `
                            })
                            this.processed_form_files[fl] = lite.utils.remove_last_characters(processed_name,4)
                        }
                    })
                }
                return true
            }
            return false
        }
        return true
    }

    async delete_form_files(){

    }

}