# gui/network_scene.py

from PyQt5.QtWidgets import QGraphicsScene, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from gui.node_item import NodeItem
from gui.edge_item import EdgeItem

class QuantumNetworkScene(QGraphicsScene):
    """
    Scene handling interactive modes: add node, connect nodes, move nodes.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, 1000, 700)

        self.current_mode = "add_node"
        self.temp_source_node = None

    def setMode(self, mode):
        self.current_mode = mode
        if mode == "connect":
            self.temp_source_node = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.views():
                super().mousePressEvent(event)
                return

            view = self.views()[0]
            item_clicked = self.itemAt(event.scenePos(), view.transform())

            if self.current_mode == "add_node":
                x = event.scenePos().x()
                y = event.scenePos().y()
                node = NodeItem(x, y)
                self.addItem(node)

            elif self.current_mode == "connect":
                if isinstance(item_clicked, NodeItem):
                    if self.temp_source_node is None:
                        # Select the first node
                        self.temp_source_node = item_clicked
                        self.statusBarMessage("Select the second node to connect.")
                    else:
                        # Connect to the second node
                        if item_clicked != self.temp_source_node:
                            edge = EdgeItem(self.temp_source_node, item_clicked)
                            self.addItem(edge)
                            self.statusBarMessage("Nodes connected.")
                        self.temp_source_node = None
                else:
                    self.temp_source_node = None

            else:
                # Move mode or default
                pass

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # Optionally, show a "rubber band" line while connecting
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

    def addNodeAtCoordinates(self):
        """
        Prompt the user for X, Y coordinates (in km, for example),
        then place a node at that position.
        """
        x_str, ok_x = QInputDialog.getText(None, "X Coordinate (km)", "Enter X in km:")
        if not ok_x:
            return
        y_str, ok_y = QInputDialog.getText(None, "Y Coordinate (km)", "Enter Y in km:")
        if not ok_y:
            return

        try:
            # Apply a scale factor if necessary (e.g., 1 km = 10 pixels)
            x_val = float(x_str) * 10  # Example scale factor
            y_val = float(y_str) * 10
            node = NodeItem(x_val, y_val)
            self.addItem(node)
            self.statusBarMessage(f"Node added at ({x_val}, {y_val}) pixels.")
        except ValueError:
            QMessageBox.warning(None, "Invalid Input", "Coordinates must be numeric.")

    def statusBarMessage(self, message: str, timeout: int = 3000):
        """
        Display a message in the status bar of the main window.
        """
        if not self.views():
            return
        window = self.views()[0].parent()
        if hasattr(window, 'status_bar'):
            window.status_bar.showMessage(message, timeout)

    def keyPressEvent(self, event):
        """Handle key press events for deleting selected items."""
        if event.key() == Qt.Key_Delete:
            for item in self.selectedItems():
                # Remove edges connected to a node
                if isinstance(item, NodeItem):
                    item.remove_all_edges(self)

                # Remove the edge itself
                elif isinstance(item, EdgeItem):
                    item.source_node.remove_edge(item)
                    item.target_node.remove_edge(item)
                    self.removeItem(item)

                # Remove the item itself (node or edge)
                self.removeItem(item)
        else:
            super().keyPressEvent(event)

