# gui/main_window.py

from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import (
    QMainWindow, QMenuBar, QToolBar, QStatusBar, QAction,
    QGraphicsView, QFileDialog, QMessageBox,
    QWidget, QVBoxLayout, QLabel, QInputDialog, QMenu
)
from PyQt5.QtCore import Qt


from gui.network_scene import QuantumNetworkScene


class QuantumNetworkWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quantum Network Simulator")
        self.resize(1200, 800)

        # Set up dark theme palette
        self.setup_palette()

        # Create scene and view
        self.scene = QuantumNetworkScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # Menus / Toolbar
        self.create_menu_bar()
        self.create_tool_bar()

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Optional global style sheet
        self.setStyleSheet("""
            QToolBar {
                background-color: #505050;
                spacing: 10px;
            }
            QMenuBar {
                background-color: #383838;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #505050;
            }
            QMenu {
                background-color: #383838;
                color: white;
            }
            QMenu::item:selected {
                background-color: #505050;
            }
            QGraphicsView {
                border: none;
            }
        """)

    def setup_palette(self):
        """
        Establish a dark theme palette.
        """
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#2F2F2F"))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor("#383838"))
        palette.setColor(QPalette.AlternateBase, QColor("#404040"))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor("#505050"))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Highlight, QColor("#BB86FC"))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

    def create_menu_bar(self):
        """
        Menu bar with File, Simulation, and Help menus.
        """
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # File Menu
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        # Add actions to File Menu
        open_action = QAction("Open...", self)
        open_action.triggered.connect(self.open_file)
        save_action = QAction("Save...", self)
        save_action.triggered.connect(self.save_file)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Simulation Menu
        sim_menu = QMenu("Simulation", self)
        menu_bar.addMenu(sim_menu)

        ent_protocols_action = QAction("Entanglement Protocols", self)
        purification_action = QAction("Purification/Error Correction", self)
        traffic_setup_action = QAction("Traffic Setup", self)
        configure_action = QAction("Configure", self)
        run_action = QAction("Run", self)
        analyze_action = QAction("Analyze", self)

        # Connect Simulation Menu actions
        ent_protocols_action.triggered.connect(self.on_entanglement_protocols)
        purification_action.triggered.connect(self.on_purification)
        traffic_setup_action.triggered.connect(self.on_traffic_setup)
        configure_action.triggered.connect(self.on_configure)
        run_action.triggered.connect(self.on_run)
        analyze_action.triggered.connect(self.on_analyze)

        sim_menu.addAction(ent_protocols_action)
        sim_menu.addAction(purification_action)
        sim_menu.addAction(traffic_setup_action)
        sim_menu.addSeparator()
        sim_menu.addAction(configure_action)
        sim_menu.addAction(run_action)
        sim_menu.addAction(analyze_action)

        # Help Menu
        help_menu = QMenu("Help", self)
        menu_bar.addMenu(help_menu)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def create_tool_bar(self):
        """
        Toolbar with text-based actions.
        """
        tool_bar = QToolBar("Main Toolbar")
        tool_bar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, tool_bar)

        # Create Actions with Text Labels
        add_node_action = QAction("Add Node (A)", self)
        connect_action = QAction("Connect Nodes (C)", self)
        move_node_action = QAction("Move Nodes (M)", self)
        coords_action = QAction("Add Node by Coordinates", self)

        # Set Shortcuts
        add_node_action.setShortcut("A")
        connect_action.setShortcut("C")
        move_node_action.setShortcut("M")

        # Connect Actions
        add_node_action.triggered.connect(lambda: self.scene.setMode("add_node"))
        connect_action.triggered.connect(lambda: self.scene.setMode("connect"))
        move_node_action.triggered.connect(lambda: self.scene.setMode("move"))
        coords_action.triggered.connect(self.scene.addNodeAtCoordinates)

        # Add Actions to Toolbar
        tool_bar.addAction(add_node_action)
        tool_bar.addAction(connect_action)
        tool_bar.addAction(move_node_action)
        tool_bar.addAction(coords_action)

    # ---------------------------
    # Simulation Menu Handlers
    # ---------------------------
    def on_entanglement_protocols(self):
        self.status_bar.showMessage("Entanglement Protocols clicked", 3000)
        # TODO: Implement functionality

    def on_purification(self):
        self.status_bar.showMessage("Purification/Error Correction clicked", 3000)
        # TODO: Implement functionality

    def on_traffic_setup(self):
        self.status_bar.showMessage("Traffic Setup clicked", 3000)
        # TODO: Implement functionality

    def on_configure(self):
        self.status_bar.showMessage("Configure clicked", 3000)
        # TODO: Implement functionality

    def on_run(self):
        self.status_bar.showMessage("Run Simulation clicked", 3000)
        # TODO: Implement functionality

    def on_analyze(self):
        self.status_bar.showMessage("Analyze clicked", 3000)
        # TODO: Implement functionality

    # ---------------------------
    # File Menu Handlers
    # ---------------------------
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open Network", "", "JSON Files (*.json);;All Files (*)"
        )
        if filename:
            QMessageBox.information(self, "Open File", f"Opened file: {filename}")
            # TODO: Implement actual JSON load logic

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Network", "", "JSON Files (*.json);;All Files (*)"
        )
        if filename:
            QMessageBox.information(self, "Save File", f"Saved file: {filename}")
            # TODO: Implement actual JSON save logic

    # ---------------------------
    # Help Menu Handler
    # ---------------------------
    def show_about_dialog(self):
        QMessageBox.about(self, "About Quantum Network Simulator",
                          "<h3>Quantum Network Simulator</h3>"
                          "<p>A user-friendly GUI for designing quantum networks.</p>"
                          "<p>Version 1.0 - For research and educational purposes.</p>")
