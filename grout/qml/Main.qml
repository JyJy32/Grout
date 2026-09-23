import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Window {
    id: root
    width: 900
    height: 600
    visible: true
    color: "#1e1e1e"
    title: "grout"

    GridView {
        anchors.fill: parent
        anchors.margins: 20
        cellWidth: 160
        cellHeight: 160
        model: ListModel {
            ListElement {
                name: "Firefox"
                color: "#e66000"
            }
            ListElement {
                name: "Terminal"
                color: "#2d2d2d"
            }
            ListElement {
                name: "Files"
                color: "#3a7bd5"
            }
            ListElement {
                name: "Vim"
                color: "#019833"
            }
        }
        delegate: Rectangle {
            width: 150
            height: 150
            color: model.color
            radius: 4

            Text {
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.margins: 10
                text: model.name
                color: "white"
                font.pixelSize: 16
            }

            MouseArea {
                anchors.fill: parent
                onClicked: console.log("launch:", model.name)
                // slight press-scale feedback, cheap and makes it feel alive
                onPressed: parent.scale = 0.96
                onReleased: parent.scale = 1.0
            }

            Behavior on scale {
                NumberAnimation {
                    duration: 80
                }
            }
        }
    }
}
