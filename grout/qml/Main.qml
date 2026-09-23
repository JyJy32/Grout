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

    Rectangle {
        id: gridBackground
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.topMargin: 60
        color: "transparent"

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.RightButton
            onClicked: emptySpaceMenu.popup()
        }

        Menu {
            id: emptySpaceMenu

            MenuItem {
                text: "Add tile"
                onTriggered: {
                    addTileSearchField.text = "";
                    addTilePopup.open();
                    addTileSearchField.forceActiveFocus();
                }
            }
        }
    }

    Popup {
        id: addTilePopup
        anchors.centerIn: parent
        width: 400
        height: 360
        modal: true
        focus: true
        padding: 12

        background: Rectangle {
            color: "#2d2d2d"
            radius: 6
            border.color: "#3a3a3a"
        }

        Column {
            anchors.fill: parent
            spacing: 8

            TextField {
                id: addTileSearchField
                width: parent.width
                placeholderText: "Search apps to add..."
                onTextChanged: addTileSearchModel.setFilterFixedString(text)
                Keys.onEscapePressed: addTilePopup.close()
            }

            ListView {
                width: parent.width
                height: parent.height - 40
                clip: true
                model: addTileSearchModel
                delegate: Rectangle {
                    id: addDelegateRoot
                    required property string name
                    required property string exec_
                    required property string icon

                    width: parent ? parent.width : 0
                    height: 40
                    color: "transparent"

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        anchors.margins: 8
                        text: addDelegateRoot.name
                        color: "white"
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            pinnedTiles.addAppTile({
                                "name": addDelegateRoot.name,
                                "exec": addDelegateRoot.exec_,
                                "icon": addDelegateRoot.icon
                            });
                            addTilePopup.close();
                        }
                    }
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
                required property int index
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
                            "payload": tileRoot.payload,
                            "colSpan": tileRoot.colSpan,
                            "rowSpan": tileRoot.rowSpan
                        });
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.RightButton
                    onClicked: tileMenu.popup()
                }

                Menu {
                    id: tileMenu
                    MenuItem {
                        text: "Resize"
                        onTriggered: {
                            var shapes = [[1, 1], [2, 1], [1, 2], [2, 2]];
                            var cur = 0;
                            for (var i = 0; i < shapes.length; i++) {
                                if (shapes[i][0] === tileRoot.colSpan && shapes[i][1] === tileRoot.rowSpan) {
                                    cur = i;
                                    break;
                                }
                            }
                            var next = shapes[(cur + 1) % shapes.length];
                            pinnedTiles.resizeTile(tileRoot.index, next[0], next[1]);
                        }
                    }
                    MenuItem {
                        text: "Remove"
                        onTriggered: pinnedTiles.removeTile(tileRoot.index)
                    }
                }
            }
        }
    }
}
