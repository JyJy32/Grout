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

    TextField {
        id: searchField
        width: parent.width
        placeholderText: "search ..."
        focus: true
        onTextChanged: {
            searchModel.setFilterFixedString(text);
            resultsPopup.open();
            if (text.length === 0)
                resultsPopup.close();
        }
    }

    Popup {
        id: resultsPopup
        y: searchField.height + 4
        width: searchField.width
        height: Math.min(resultsList.implicitHeight, 300)
        padding: 0
        closePolicy: Popup.NoAutoClose

        background: Rectangle {
            color: "#2d2d2d"
            radius: 4
            border.color: "#3a3a3a"
        }

        ListView {
            id: resultsList
            anchors.fill: parent
            model: searchModel
            clip: true
            implicitHeight: Math.min(contentHeight, 300)
            delegate: Rectangle {
                width: resultsList.width
                height: 44
                color: ListView.isCurrentItem ? "#3a3a3a" : "transparent"
                Text {
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    anchors.margins: 12
                    text: name
                    color: "white"
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: console.log("launch: ", exec_)
                }
            }
        }
    }

    GridView {
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.topMargin: 60
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
