import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Window {
    id: root
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
    width: Screen.width
    height: Screen.height
    x: 0
    y: 0
    visible: true
    color: "#1e1e1e"
    title: "grout"

    TextField {
        id: searchField
        width: parent.width
        placeholderText: "search ..."
        focus: true
        Keys.onEscapePressed: root.setVisible(false)
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

    GridLayout {
        id: pinnedGrid
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.margins: 20
        anchors.topMargin: 60
        columns: 4
        rowSpacing: 8
        columnSpacing: 8

        Repeater {
            model: pinnedTiles
            delegate: Item {
                id: tileRoot
                required property string name
                required property int colSpan
                required property int rowSpan
                required property var payload
                required property url qmlSource

                Layout.columnSpan: colSpan
                Layout.rowSpan: rowSpan
                Layout.preferredWidth: 150 * colSpan + 8 * (colSpan - 1)
                Layout.preferredHeight: 150 * rowSpan + 8 * (rowSpan - 1)

                Loader {
                    anchors.fill: parent
                    onStatusChanged: if (status === Loader.Error)
                        console.log("Loader error:", sourceComponent)
                    Component.onCompleted: {
                        setSource(tileRoot.qmlSource, {
                            "name": tileRoot.name,
                            "payload": tileRoot.payload
                        });
                    }
                }
            }
        }
    }
}
