import QtQuick 2.15

Rectangle {
    property string name
    property var payload

    color: "#2d2d2d"
    radius: 4

    Text {
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.margins: 10
        width: parent.width - 20
        wrapMode: Text.WordWrap
        text: name
        color: "white"
        font.pixelSize: 16
    }

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
