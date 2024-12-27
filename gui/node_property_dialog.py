# gui/node_property_dialog.py

from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QVBoxLayout, QMessageBox
)

class NodePropertyDialog(QDialog):
    """
    A dialog to set or edit node properties:
      - Node type
      - Number of qubits
      - Qubit technology
      - Coherence time
      - Photon insertion loss
    """
    def __init__(self, node_item, parent=None):
        super().__init__(parent)
        self.node_item = node_item
        self.setWindowTitle("Node Properties")
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()

        # Node Type
        self.nodeTypeCombo = QComboBox()
        self.nodeTypeCombo.addItems(["memory", "detector", "memory-detector", "repeater"])
        self.nodeTypeCombo.setCurrentText(self.node_item.node_type)
        layout.addRow(QLabel("Node Type:"), self.nodeTypeCombo)

        # Number of Qubits
        self.qubitsEdit = QLineEdit(str(self.node_item.num_qubits))
        layout.addRow(QLabel("Number of Qubits:"), self.qubitsEdit)

        # Qubit Technology
        self.qubitTechCombo = QComboBox()
        self.qubitTechCombo.addItems(["Color centers", "Atoms", "Ions", "Superconducting"])
        self.qubitTechCombo.setCurrentText(self.node_item.qubit_tech)
        layout.addRow(QLabel("Qubit Tech:"), self.qubitTechCombo)

        # Coherence Time
        self.coherenceTimeEdit = QLineEdit(str(self.node_item.coherence_time))
        layout.addRow(QLabel("Coherence Time (s):"), self.coherenceTimeEdit)

        # Photon Insertion Loss
        self.insertionLossEdit = QLineEdit(str(self.node_item.insertion_loss))
        layout.addRow(QLabel("Photon Insertion Loss (dB):"), self.insertionLossEdit)

        # Buttons
        button_layout = QVBoxLayout()
        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")
        button_layout.addWidget(self.okButton)
        button_layout.addWidget(self.cancelButton)

        layout.addRow(button_layout)
        self.setLayout(layout)

        # Connect signals
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def accept(self):
        """Save changes and update the node."""
        # Update node_type
        self.node_item.node_type = self.nodeTypeCombo.currentText()

        # Update num_qubits with validation
        try:
            num_qubits = int(self.qubitsEdit.text())
            if num_qubits < 1:
                raise ValueError
            self.node_item.num_qubits = num_qubits
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Number of Qubits must be a positive integer.")
            return

        # Update qubit_tech
        self.node_item.qubit_tech = self.qubitTechCombo.currentText()

        # Update coherence_time with validation
        try:
            coherence_time = float(self.coherenceTimeEdit.text())
            if coherence_time < 0:
                raise ValueError
            self.node_item.coherence_time = coherence_time
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Coherence Time must be a non-negative number.")
            return

        # Update insertion_loss with validation
        try:
            insertion_loss = float(self.insertionLossEdit.text())
            if insertion_loss < 0:
                raise ValueError
            self.node_item.insertion_loss = insertion_loss
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Photon Insertion Loss must be a non-negative number.")
            return

        # Update appearance based on node_type
        self.node_item.update_appearance()
        super().accept()
