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
    color: palette.background
    title: "grout"

    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        // ---- header ----
        Item {
            Layout.fillWidth: true
            Layout.preferredHeight: 60

            RowLayout {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 16

                Text {
                    id: clockText
                    color: palette.text
                    font.pixelSize: 40
                    text: Qt.formatTime(new Date(), "hh:mm")

                    Timer {
                        interval: 1000
                        running: true
                        repeat: true
                        onTriggered: clockText.text = Qt.formatTime(new Date(), "hh:mm")
                    }
                }

                TextField {
                    id: searchField
                    Layout.fillWidth: true
                    placeholderText: "search ..."
                    placeholderTextColor: palette.accent
                    focus: true
                    font.pixelSize: 32
                    background: Rectangle {
                        color: palette.background
                    }
                    color: palette.accent
                    onTextChanged: {
                        searchModel.setFilterFixedString(text);
                        resultsPopup.open();
                        if (text.length === 0)
                            resultsPopup.close();
                    }
                    Keys.onEscapePressed: root.setVisible(false)
                    Keys.onDownPressed: {
                        if (resultsList.count > 0)
                            resultsList.forceActiveFocus();
                    }
                    Keys.onReturnPressed: {
                        if (resultsList.currentItem) {
                            launcher.launch(resultsList.currentItem.exec_);
                            root.setVisible(false);
                            resultsPopup.close();
                            searchField.text = "";
                        }
                    }
                }

                Rectangle {
                    Layout.preferredWidth: 36
                    Layout.preferredHeight: 36
                    radius: 18
                    color: palette.surface
                    Text {
                        anchors.centerIn: parent
                        text: "👤"
                        font.pixelSize: 18
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: accountMenu.popup()
                    }

                    Menu {
                        id: accountMenu
                        MenuItem {
                            text: "Log out"
                            onTriggered: systemActions.logout()
                        }
                        MenuItem {
                            text: "Shut down"
                            onTriggered: systemActions.shutdown()
                        }
                    }
                }

                Rectangle {
                    Layout.preferredWidth: 36
                    Layout.preferredHeight: 36
                    radius: 18
                    color: palette.surface
                    Text {
                        anchors.centerIn: parent
                        text: "⚙"
                        font.pixelSize: 18
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: console.log("settings clicked")
                    }
                }

                Popup {
                    id: resultsPopup
                    parent: searchField
                    x: 0
                    y: searchField.height + 4
                    width: searchField.width
                    height: Math.min(resultsList.implicitHeight, 300)
                    padding: 0
                    closePolicy: Popup.NoAutoClose

                    background: Rectangle {
                        color: palette.surface
                        radius: 4
                        border.color: palette.surfaceBorder
                    }

                    ListView {
                        id: resultsList
                        anchors.fill: parent
                        model: searchModel
                        clip: true
                        implicitHeight: Math.min(contentHeight, 300)
                        keyNavigationEnabled: true
                        Keys.onEscapePressed: searchField.forceActiveFocus()
                        Keys.onUpPressed: {
                            if (currentIndex === 0)
                                searchField.forceActiveFocus();
                            else
                                currentIndex--;
                        }
                        Keys.onReturnPressed: {
                            if (currentItem) {
                                launcher.launch(currentItem.exec_);
                                root.setVisible(false);
                                resultsPopup.close();
                                searchField.text = "";
                            }
                        }
                        delegate: Rectangle {
                            required property string name
                            required property string exec_
                            width: resultsList.width
                            height: 44
                            color: ListView.isCurrentItem ? palette.surfaceBorder : "transparent"
                            Text {
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.left: parent.left
                                anchors.margins: 12
                                text: name
                                color: palette.text
                            }
                            MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    launcher.launch(exec_);
                                    root.setVisible(false);
                                    resultsPopup.close();
                                    searchField.text = "";
                                }
                            }
                        }
                    }
                }
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true

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

                    MenuItem {
                        text: "Add Widget"
                        onTriggered: {
                            addWidgetSearchField.text = "";
                            addWidgetPopup.open();
                            addWidgetSearchField.forceActiveFocus();
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
                    color: palette.surface
                    radius: 6
                    border.color: palette.surfaceBorder
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
                                color: palette.text
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

            Popup {
                id: addWidgetPopup
                anchors.centerIn: parent
                width: 400
                height: 360
                modal: true
                focus: true
                padding: 12

                background: Rectangle {
                    color: palette.surface
                    radius: 6
                    border.color: palette.surfaceBorder
                }

                Column {
                    anchors.fill: parent
                    spacing: 8

                    TextField {
                        id: addWidgetSearchField
                        width: parent.width
                        placeholderText: "Search apps to add..."
                        onTextChanged: addTileSearchModel.setFilterFixedString(text)
                        Keys.onEscapePressed: addTilePopup.close()
                    }

                    ListView {
                        width: parent.width
                        height: parent.height - 40
                        clip: true
                        model: addWidgetSearchModel
                        delegate: Rectangle {
                            id: addWDelegateRoot
                            required property string name

                            width: parent ? parent.width : 0
                            height: 40
                            color: "transparent"

                            Text {
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.left: parent.left
                                anchors.margins: 8
                                text: addWDelegateRoot.name
                                color: palette.text
                            }

                            MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    pinnedTiles.addWidgetTile({
                                        "name": addWDelegateRoot.name
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
                            id: tileLoader
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
                            onLoaded: {
                                item.name = Qt.binding(function () {
                                    return tileRoot.name;
                                });
                                item.payload = Qt.binding(function () {
                                    return tileRoot.payload;
                                });
                                item.colSpan = Qt.binding(function () {
                                    return tileRoot.colSpan;
                                });
                                item.rowSpan = Qt.binding(function () {
                                    return tileRoot.rowSpan;
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
                            Menu {
                                id: colourMenu
                                title: "Change colour"

                                Instantiator {
                                    model: Object.keys(themeColors)
                                    MenuItem {
                                        text: modelData
                                        onTriggered: pinnedTiles.setTileColour(tileRoot.index, themeColors[modelData])
                                    }
                                    onObjectAdded: (index, object) => colourMenu.insertItem(index, object)
                                    onObjectRemoved: (index, object) => colourMenu.removeItem(object)
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
    }
}
