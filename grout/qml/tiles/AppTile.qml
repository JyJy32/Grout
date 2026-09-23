import QtQuick 2.15

Rectangle {
    property string name
    property var payload
    property int colSpan
    property int rowSpan

    color: "#2d2d2d"
    radius: 4

    Text {
        id: tileName
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.margins: 10
        width: parent.width - 20
        wrapMode: Text.WordWrap
        text: name
        color: "white"
        font.pixelSize: 20
    }

    Image {
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        source: "image://icons/" + payload.icon
    }

    states: [
        State {
            name: "small"
            when: colSpan === 1 && rowSpan === 1
            PropertyChanges {
                tileName.font.pixelSize: 20
            }
        },
        State {
            name: "big"
            when: colSpan === 2 && rowSpan === 2
            PropertyChanges {
                tileName.font.pixelSize: 36
            }
        }
    ]

    MouseArea {
        anchors.fill: parent
        onClicked: {
            launcher.launch(payload.exec);
            mainWindow.setVisible(false);
        }
        onPressed: parent.scale = 0.96
        onReleased: parent.scale = 1.0
    }
    Behavior on scale {
        NumberAnimation {
            duration: 80
        }
    }
}
