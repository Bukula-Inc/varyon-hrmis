export default class Barcode{
    constructor(){
        this.on_scan = {}
        this.current_code = ""
        this.scan_buffer = ""
        this.scan_timeout = ""
        this.scanned_values = []
        this.cached_values = {}
        this.init()
    }

    add_scanner_event(fun,controller){
        if(fun && typeof fun === "function"){
            this.on_scan[fun.name] = {fun:fun, controller:controller}
        }
        else{
            console.error("Failed to initialize scanner: Scanner event is not a function!")
        }
    }

    init(){
        document.addEventListener('keydown', async (e) => {
        // Check for Enter key to process the scan
        if (e.key === 'Enter') {
            if (this.current_code.length > 0) {
                // Handle scanned code
                const scannedCode = this.current_code.trim()
                this.current_code = scannedCode
                
                // run necessary functions to handle scanner
                try{
                    if(lite.utils.object_has_data(this.on_scan)){
                        await Promise.all(lite.utils.get_object_values(this.on_scan).map( async f=>{
                            await f.fun(this.current_code, f.controller)
                        }))
                    }
                }
                catch(e){
                    console.error(`An error occurred while executing scanner function:${e}`)
                }

                // Clear the buffer
                this.current_code = ''
            }
        } else if (e.key.length === 1) { 
            this.current_code += e.key
            // Reset the buffer after 100ms if no new input is detected
            clearTimeout(this.scan_timeout);
            this.scan_timeout = setTimeout(() => {
                this.current_code = ''
            }, 100);
        }
        });
    }

    cache_value(model, key, value){
        if(!this.cached_values[model]){
            this.cached_values[model] = {}
            this.cached_values[model][key] = value
        }
        else if(this.cached_values[model]){
            this.cached_values[model][key] = value
        }
    }

    get_cached_value(model, key){
        if(this.cached_values && this.cached_values[model] && this.cached_values[model][key]){
            return this.cached_values[model][key]
        }
        return null
    }
}