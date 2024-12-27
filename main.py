# main.py
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from gui.welcome_page import AnimatedBackgroundWidget
from gui.main_window import QuantumNetworkWindow  # main simulator window

def main():
    app = QApplication(sys.argv)

    # Instantiate the new animated welcome page
    welcome = AnimatedBackgroundWidget()
    
    # If user clicks 'Start', proceed to main simulator
    if welcome.exec_() == QDialog.Accepted:
        window = QuantumNetworkWindow()
        window.show()
        sys.exit(app.exec_())
    else:
        # If user closes the welcome page without clicking 'Start', just exit
        sys.exit(0)

if __name__ == "__main__":
    main()
