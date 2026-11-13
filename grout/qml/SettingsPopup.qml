import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Popup {
    id: settingsPopup

    // centred on the whole window, not just the area below the header
    parent: Overlay.overlay
    anchors.centerIn: parent
    width: 460
    modal: true
    focus: true
    padding: 20
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    background: Rectangle {
        color: palette.surface
        radius: 8
        border.color: palette.surfaceBorder
    }

    // reset the form to the saved values each time it opens
    onAboutToShow: {
        var idx = paletteBox.find(appSettings.currentPalette);
        paletteBox.currentIndex = idx >= 0 ? idx : 0;
        terminalField.text = appSettings.terminal;
    }

    function save() {
        appSettings.apply(paletteBox.currentText, terminalField.text);
        settingsPopup.close();
    }

    contentItem: ColumnLayout {
        spacing: 16

        Text {
            text: "Settings"
            color: palette.text
            font.pixelSize: 24
            font.bold: true
        }

        // ---- palette ----
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 4
            Text {
                text: "Palette"
                color: palette.text
            }
            ComboBox {
                id: paletteBox
                Layout.fillWidth: true
                model: appSettings.palettes
            }
            Text {
                text: "Applied on next start"
                color: palette.accent
                font.pixelSize: 11
            }
        }

        // ---- terminal ----
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 4
            Text {
                text: "Terminal"
                color: palette.text
            }
            TextField {
                id: terminalField
                Layout.fillWidth: true
                placeholderText: "xterm"
                Keys.onReturnPressed: settingsPopup.save()
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.topMargin: 8
            spacing: 8

            Item {
                Layout.fillWidth: true
            }
            Button {
                text: "Cancel"
                onClicked: settingsPopup.close()
            }
            Button {
                text: "Save"
                highlighted: true
                onClicked: settingsPopup.save()
            }
        }
    }
}
