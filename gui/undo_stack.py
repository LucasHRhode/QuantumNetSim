from PyQt5.QtWidgets import QUndoCommand

class AddNodeCommand(QUndoCommand):
    def __init__(self, scene, node_item, description="Add Node"):
        super().__init__(description)
        self.scene = scene
        self.node_item = node_item
        self.added = False

    def redo(self):
        if not self.added:
            self.scene.addItem(self.node_item)
            self.added = True
        else:
            self.scene.addItem(self.node_item)

    def undo(self):
        self.scene.removeItem(self.node_item)

class AddEdgeCommand(QUndoCommand):
    def __init__(self, scene, edge_item, description="Add Edge"):
        super().__init__(description)
        self.scene = scene
        self.edge_item = edge_item
        self.added = False

    def redo(self):
        if not self.added:
            self.scene.addItem(self.edge_item)
            self.added = True
        else:
            self.scene.addItem(self.edge_item)

    def undo(self):
        self.scene.removeItem(self.edge_item)
