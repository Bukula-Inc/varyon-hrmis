export default class QRCodeReaderAndGenerator {
    constructor(config) {
        this.$code_field = $ (config.lite_file_picker) || ''
        this.$video_area = $ (config.lite_video_area) || ''
        this.$canvas_area = $ (config.lite_canvas_area) || ''
    }

    QRCode_reader (field = false, video = false, screen = false) {
        if (field) {
            this.#readQRCodeFromStaticImage ()
        }else if (video) {
            this.#readQRCodeFromVideoInput ()
        }else if (screen) {
            this.#readQRCodeFromScreen ()
        }
    }

    #readQRCodeFromStaticImage () {
        this.$code_field.on ('change', (event) => {
            const file = $ (event.target).prop ('files')[0]
            if (file) {
                const reader = new FileReader ()
                reader.onload = () => {
                    const image = new Image ()
                    image.onload = () => {
                        const canvas = document.createElement ('canvas')
                        canvas.width = image.width
                        canvas.height = image.height
                        const context = canvas.getContext ('2d')
                        context.drawImage (image, 0, 0, canvas.width, canvas.height)
                        this.#scanQRCodeFromImage (context.getImageData (0, 0, canvas.width, canvas.height))
                    }
                    image.src = reader.result
                }
                reader.readAsDataURL (file)
            }
        })
    }

    #readQRCodeFromVideoInput () {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia ({ video: { facingMode: 'environment' } })
                .then ((stream) => {
                    this.$video_area.srcObject = stream
                })
                .catch ((error) => {
                    console.error ('Error accessing camera:', error)
                })

            this.$video_area.on ('loadeddata', () => {
                setInterval (() => {
                    this.#scanQRCodeFromVideo ()
                }, 1000)
            })
        } else {
            console.error ('getUserMedia not supported, cannot perform real-time video scanning.')
        }
    }

    #readQRCodeFromScreen() {
        const canvas = this.$canvas_area
        const context = canvas.getContext('2d')

        canvas.width = window.innerWidth
        canvas.height = window.innerHeight
        context.drawWindow(window, 0, 0, canvas.width, canvas.height, 'rgb(255,255,255)')
        this.#scanQRCodeFromImage(context.getImageData(0, 0, canvas.width, canvas.height))
    }

    #scanQRCodeFromImage (imageData) {
        const code = jsQR (imageData.data, imageData.width, imageData.height)

        if (code) {
            console.log ('QR Code detected:', code.data)
        }
    }

    #scanQRCodeFromVideo () {
        const context = this.$canvas_area .getContext ('2d')
        this.$canvas_area .width = this.$video_area.videoWidth
        this.$canvas_area .height = this.$video_area.videoHeight
        context.drawImage (this.$video_area, 0, 0, this.$canvas_area .width, this.$canvas_area .height)
        this.#scanQRCodeFromImage (context.getImageData (0, 0, this.$canvas_area .width, this.$canvas_area .height))
    }
}