import HTML_Builder from "./html_builder.js"
export default class Procurement{
    constructor(){
        this.builder = new HTML_Builder()
    }     

    generate_table_of_evaulation = (data) => {  
        return `<table id="bid-evaluation-table" class="min-w-full">
                    <thead id="table-header">
                        
                    </thead>
                    <tbody id="bid-table">
                        
                    </tbody>
                </table>

        `
    } 

}

