export default class Scanner_HTML_Generator{
    constructor(){

    }

    create_camera_scanner(){
        return `
        <div class="">
            <div id="scanner-container">
                <video id="barcode-video" autoplay></video>
                <audio id="beep" preload="auto">
                    <source src="/static/audio/scanner_2.mp3" type="audio/mpeg">
                </audio>
            </div>
            <div id="barcode-result"></div>
        </div>
        `
    }
}