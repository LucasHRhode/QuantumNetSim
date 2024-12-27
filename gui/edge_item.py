# gui/edge_item.py

from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsLineItem
from gui.node_item import NodeItem

class EdgeItem(QGraphicsLineItem):
    """
    Represents a connection (fiber link) between two NodeItems.
    """
    def __init__(self, source: NodeItem, target: NodeItem):
        super().__init__()
        self.source_node = source
        self.target_node = target
        self.setPen(QPen(QColor("black"), 2))

        self.update_positions()

    def update_positions(self):
        p1 = self.source_node.scenePos()
        p2 = self.target_node.scenePos()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())
