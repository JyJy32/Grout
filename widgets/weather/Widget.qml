import QtQuick 2.15

Rectangle {
    id: weatherRoot
    property string name
    property var payload: ({})
    property int colSpan
    property int rowSpan

    property real latitude: payload.latitude !== undefined ? payload.latitude : 51.2194
    property real longitude: payload.longitude !== undefined ? payload.longitude : 4.4025
    property int refreshIntervalMs: payload.refreshIntervalMs !== undefined ? payload.refreshIntervalMs : 600000 // 10 min

    property real temperature: NaN
    property bool loading: true
    property string errorText: ""

    color: "#2d2d2d"

    function fetchWeather() {
        console.log("fetching weather");
        loading = true;
        errorText = "";
        var xhr = new XMLHttpRequest();
        var url = "https://api.open-meteo.com/v1/forecast?latitude=" + latitude + "&longitude=" + longitude + "&current=temperature_2m,weather_code";
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                loading = false;
                if (xhr.status === 200) {
                    try {
                        var data = JSON.parse(xhr.responseText);
                        temperature = data.current.temperature_2m;
                        // weatherCode = data.current.weather_code;
                    } catch (e) {
                        console.log("parse error");
                        errorText = "Parse error";
                    }
                } else {
                    console.log("fetch failed");
                    errorText = "Fetch failed";
                }
            }
        };
        xhr.open("GET", url);
        xhr.send();
    }
    Timer {
        interval: weatherRoot.refreshIntervalMs
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: weatherRoot.fetchWeather()
    }

    Text {
        visible: weatherRoot.loading && isNaN(weatherRoot.temperature)
        text: "..."
        color: "white"
        font.pixelSize: 16
    }

    Text {
        visible: !isNaN(weatherRoot.temperature)
        text: Math.round(weatherRoot.temperature) + "°C"
        color: "white"
        font.pixelSize: 16
    }

    Text {
        visible: weatherRoot.errorText !== ""
        text: weatherRoot.errorText
        color: "#ffcccc"
        font.pixelSize: 16
    }
}
