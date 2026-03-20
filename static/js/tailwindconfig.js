class e{constructor(){this.configureTailwind()}async configureTailwind(){
    let colors = {default:"#151030", theme_text_color:"#ffffff", secondary_color:"#d35611"}
    try{
        const Utils = await import("./utils/utils.js")
        const utils = new Utils.default()
        const content = await utils.delay_until(()=>{
            if(utils.object_has_data(lite?.user) || utils?.object_has_data(lite?.system_settings)){
                return lite
            }
        },70000)
        if(lite?.user?.company){
            if(lite?.user?.company?.default_theme_color){
                colors.default = lite?.user?.company?.default_theme_color
            }
            if(lite?.user?.company?.default_theme_text_color){
                colors.theme_text_color = lite?.user?.company?.default_theme_text_color
            }
            if(lite?.user?.company?.default_secondary_color){
                colors.secondary_color = lite?.user?.company?.default_secondary_color
            }
        }
    }
    catch(e){}
    tailwind.config={theme:{fontSize:this.generateFontSizes(9,80),extend:{gridTemplateColumns:this.generateGridColumns(10,150),gridColumn:{13:"span 13"},colors:{"default":colors?.default,theme_text_color: colors.theme_text_color, secondary_color:colors.secondary_color,defaulthover:"#1f1847",lightgray:"#eeeeee",draftstatus:"#FAA593"},boxShadow:{darker:"rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.05) 0px 4px 6px -2px",lighter:"rgba(0, 0, 0, 0.1) 0px 4px 6px -1px, rgba(0, 0, 0, 0.06) 0px 2px 4px -1px"},zIndex:this.generateZIndexes(70,100)}}}}generateFontSizes(r,t){const n={};for(let e=t;e>=r;e--){n[e]=`${e}px`}return n}generateGridColumns(r,t){const n={};for(let e=r;e<=t;e++){n[e]=`repeat(${e}, minmax(0, 1fr))`}return n}generateZIndexes(r,t){const n={};for(let e=t;e>=r;e-=10){n[e]=`${e}`}return n}}new e;