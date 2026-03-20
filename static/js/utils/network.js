class NetworkMonitorService {
    constructor () {
        this.connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection
        this.connectionTypeMap = {
            'slow-2g': "Slow 2G",
            '2g': "2G",
            '3g': "3G",
            '4g': "4G",
            '5g': "5G",
            'unknown': "Unknown"
        }
    }

    updateConnectionInfo () {
        this.effectiveType = this.connection.effectiveType || 'unknown'
        this.downlink = this.connection.downlink || 0
        this.downlinkMbps = (this.downlink * 0.001).toFixed (2)
    }

    getConnectionType () {
        return this.connectionTypeMap[this.effectiveType] ||'unknown'
    }

    getConnectionQuality () {
        if (this.downlink >= 4) {
            return 'Excellent';
        } else if (this.downlink >= 2) {
            return 'Good';
        } else if (this.downlink >= 1) {
            return 'Moderate';
        } else {
            return 'Poor';
        }
    }

    alertUser () {
        this.updateConnectionInfo();
        const connectionType = this.getConnectionType();
        const connectionQuality = this.getConnectionQuality();
        alert(`You are connected to a ${connectionType} network.\nConnection Speed: ${this.downlinkMbps} Mbps\nConnection Quality: ${connectionQuality}`);
    }

    getNetworkConnection () {
        this.updateConnectionInfo();
        const connectionType = this.getConnectionType();
        const connectionQuality = this.getConnectionQuality();
        return {
            'connectionType': connectionType,
            'connectionQuality': connectionQuality,
            'mbps': this.downlinkMbps
        }
    }

    startMonitoring() {
        this.connection.addEventListener('change', () => {
            this.updateConnectionInfo();
            this.alertUser();
        });
    }
}

export default NetworkMonitorService 