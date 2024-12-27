# gui/node_item.py

from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt  
from PyQt5.QtWidgets import QGraphicsEllipseItem
from gui.node_property_dialog import NodePropertyDialog

class NodeItem(QGraphicsEllipseItem):
    """
    Represents a quantum network node with attributes:
      - node_type
      - num_qubits
      - qubit_tech
      - coherence_time
      - insertion_loss
    """
    def __init__(self, x, y, radius=30):
        super().__init__(-radius/2, -radius/2, radius, radius)
        self.setPos(x, y)
        self.setFlags(QGraphicsEllipseItem.ItemIsSelectable | QGraphicsEllipseItem.ItemIsMovable)

        # Default properties
        self.node_type = "memory"
        self.num_qubits = 1
        self.qubit_tech = "Color centers"
        self.coherence_time = 1.0
        self.insertion_loss = 0.0

        self.radius = radius
        self.setPen(QPen(Qt.black, 2))
        self.setBrush(QBrush(QColor("yellow")))

    def contextMenuEvent(self, event):
        """Right-click opens the property dialog to edit node properties."""
        dialog = NodePropertyDialog(self)
        dialog.exec_()

    def mouseDoubleClickEvent(self, event):
        """Double-click opens the property dialog."""
        dialog = NodePropertyDialog(self)
        dialog.exec_()

    def update_appearance(self):
        """Update the node's color based on its type."""
        type_color_map = {
            "memory": QColor("yellow"),
            "detector": QColor("lightblue"),
            "memory-detector": QColor("pink"),
            "repeater": QColor("lightgreen")
        }
        color = type_color_map.get(self.node_type, QColor("gray"))
        self.setBrush(QBrush(color))
