import sys
import math
import random
from PyQt5.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
)
from PyQt5.QtGui import (
    QPainter, QLinearGradient, QColor, QFont
)
from PyQt5.QtWidgets import (
    QApplication, QDialog, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox, QGraphicsOpacityEffect, QWidget
)

class LineWidget(QWidget):
    """
    A simple widget representing a white line (rectangle).
    Animate its geometry to move it on the screen.
    """
    def __init__(self, thickness=4, parent=None):
        super().__init__(parent)
        self.thickness = thickness
        # The entire widget is white:
        self.setStyleSheet("background-color: white;")

class AnimatedBackgroundWidget(QDialog):
    """
    A QDialog that features:
      1. A dynamic rainbow gradient background that shifts over time.
      2. A starfield/particle layer drawn on top (animated).
      3. Title, subtitle, and buttons with sequential fade-in animations.
      4. Animated white lines from corners to near the middle of the screen. (Not appearing for some reason)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to QuantumNetSim")
        self.setFixedSize(1800, 1200)
        self.setModal(True)

        # Rainbow gradient counter
        self.gradient_counter = 0

        # Starfield/particle data
        self.num_particles = 5000  # Increase or decrease as desired
        self.particles = []

        # references to the UI elements to animate them
        self.title_label = None
        self.subtitle_label = None
        self.start_button = None
        self.help_button = None
        self.about_button = None

        # the UI (labels, buttons), lines, and fade animations
        self.setup_ui()
        self.setup_lines()
        self.setup_line_animations()
        self.setup_fade_in_animations()

        # Initialize the starfield
        self.init_particles()

        # Timer for both gradient and starfield animations (~33 FPS)
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(30)

    # -------------------------------------------------------------------------
    # UI Setup
    # -------------------------------------------------------------------------
    def setup_ui(self):
        """
        Create the main layout, add the title, subtitle, and buttons,
        but do NOT animate them yet (that's in setup_fade_in_animations).
        """
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        # Increase bottom margin to accommodate lines near bottom
        main_layout.setContentsMargins(50, 50, 50, 250)

        # Title
        self.title_label = QLabel("QuantumNetSim", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 44, QFont.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: white;")

        # Subtitle
        self.subtitle_label = QLabel("A Simulation Tool", self)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_font = QFont("Arial", 20, QFont.Normal)
        self.subtitle_label.setFont(subtitle_font)
        self.subtitle_label.setStyleSheet("color: #F0F0F0;")

        # Buttons
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start", self)
        self.start_button.setFixedSize(360, 90)
        self.start_button.setStyleSheet(self.button_style())
        self.start_button.clicked.connect(self.on_start_clicked)

        self.help_button = QPushButton("Help", self)
        self.help_button.setFixedSize(240, 90)
        self.help_button.setStyleSheet(self.button_style())
        self.help_button.clicked.connect(self.on_help_clicked)

        self.about_button = QPushButton("About", self)
        self.about_button.setFixedSize(240, 90)
        self.about_button.setStyleSheet(self.button_style())
        self.about_button.clicked.connect(self.on_about_clicked)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.about_button)

        # Add labels to layout
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        # Spacer to push buttons lower
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addSpacerItem(spacer)

        # Add the button row
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def setup_lines(self):
        """
        Create 6 line widgets:
          - 2 from top-left corner
          - 2 from bottom-left corner
          - 2 from bottom-right corner
        Initially placed with minimal size, which we'll animate via geometry.
        """
        self.lines_top_left = []
        self.lines_bottom_left = []
        self.lines_bottom_right = []

        line_thickness = 4
        gap = 10  # ~1 cm in pixels
        w = self.width()
        h = self.height()

        # --- Top-left corner lines ---
        for i in range(2):
            line = LineWidget(thickness=line_thickness, parent=self)
            line.setGeometry(
                i * gap,  # offset horizontally by 'gap' for the second line
                0,
                line_thickness,
                10  # minimal height
            )
            line.show()
            line.raise_()  # Ensure lines are on top
            self.lines_top_left.append(line)

        # --- Bottom-left corner lines ---
        for i in range(2):
            line = LineWidget(thickness=line_thickness, parent=self)
            line.setGeometry(
                0,
                h - line_thickness - i * gap,
                10,
                line_thickness
            )
            line.show()
            line.raise_()  # Ensure lines are on top
            self.lines_bottom_left.append(line)

        # --- Bottom-right corner lines ---
        for i in range(2):
            line = LineWidget(thickness=line_thickness, parent=self)
            line.setGeometry(
                w - line_thickness - i * gap,
                h - line_thickness,
                line_thickness,
                10
            )
            line.show()
            line.raise_()  # Ensure lines are on top
            self.lines_bottom_right.append(line)

            

        

    def setup_line_animations(self):
        """
        Animate each line from corners to near the 'middle' of the screen.
        We'll store the animations in a list and start them in parallel.
        """
        cx = self.width() // 2
        cy = self.height() // 2
        duration = 700
        curve = QEasingCurve.InOutQuad

        self.all_line_animations = []

        # --- Animate top-left lines downward ---
        for i, line in enumerate(self.lines_top_left):
            anim = QPropertyAnimation(line, b"geometry", self)
            anim.setDuration(duration)
            anim.setEasingCurve(curve)
            start_rect = line.geometry()
            anim.setStartValue(start_rect)
            # end_rect example: half the distance down from top to center
            end_rect = QRect(
                cx - (line.width() // 2) + i*10,
                cy // 4,
                line.width(),
                cy - (cy // 4)
            )
            anim.setEndValue(end_rect)
            self.all_line_animations.append(anim)

        # --- Animate bottom-left lines right ---
        for i, line in enumerate(self.lines_bottom_left):
            anim = QPropertyAnimation(line, b"geometry", self)
            anim.setDuration(duration)
            anim.setEasingCurve(curve)
            start_rect = line.geometry()
            anim.setStartValue(start_rect)
            # move horizontally halfway to center
            end_width = cx // 2
            end_rect = QRect(
                0,
                line.y() - i*10,
                end_width,
                line.height()
            )
            anim.setEndValue(end_rect)
            self.all_line_animations.append(anim)

        # --- Animate bottom-right lines upward ---
        for i, line in enumerate(self.lines_bottom_right):
            anim = QPropertyAnimation(line, b"geometry", self)
            anim.setDuration(duration)
            anim.setEasingCurve(curve)
            start_rect = line.geometry()
            anim.setStartValue(start_rect)
            # move upward
            end_height = (self.height() - cy)//2
            end_rect = QRect(
                line.x(),
                cy + i*10,
                line.width(),
                end_height
            )
            anim.setEndValue(end_rect)
            self.all_line_animations.append(anim)

        # Start them all in parallel
        for anim in self.all_line_animations:
            anim.start()

    def button_style(self):
        """Return a stylish stylesheet for the buttons."""
        return """
        QPushButton {
            background-color: rgba(255, 255, 255, 0.8);
            color: #333333;
            border-radius: 12px;
            font-size: 60px;
            font-weight: bold;
            padding: 12px 20px;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 1.0);
        }
        QPushButton:pressed {
            background-color: #dddddd;
        }
        """

    def on_start_clicked(self):
        """Close the dialog with Accepted when 'Start' is clicked."""
        self.accept()

    def on_help_clicked(self):
        """Display a basic help message."""
        QMessageBox.information(self, "Help", "Help contents go here...")

    def on_about_clicked(self):
        """Show an About message."""
        QMessageBox.about(self, "About QuantumNetSim",
                          "<h3>QuantumNetSim</h3>"
                          "<p>A user-friendly GUI for designing quantum networks.</p>"
                          "<p>Version 1.0 - For research and educational purposes.</p>")

    # -------------------------------------------------------------------------
    # Fade-In Animations
    # -------------------------------------------------------------------------
    def setup_fade_in_animations(self):
        """
        Creates QPropertyAnimations that fade in the title, then subtitle,
        then the buttons.
        """
        # Title fade
        title_effect = QGraphicsOpacityEffect(self.title_label)
        self.title_label.setGraphicsEffect(title_effect)
        title_effect.setOpacity(0.0)

        self.title_anim = QPropertyAnimation(title_effect, b"opacity", self)
        self.title_anim.setDuration(400)
        self.title_anim.setStartValue(0.0)
        self.title_anim.setEndValue(1.0)
        self.title_anim.setEasingCurve(QEasingCurve.InOutQuad)

        # Subtitle fade
        subtitle_effect = QGraphicsOpacityEffect(self.subtitle_label)
        self.subtitle_label.setGraphicsEffect(subtitle_effect)
        subtitle_effect.setOpacity(0.0)

        self.subtitle_anim = QPropertyAnimation(subtitle_effect, b"opacity", self)
        self.subtitle_anim.setDuration(400)
        self.subtitle_anim.setStartValue(0.0)
        self.subtitle_anim.setEndValue(1.0)
        self.subtitle_anim.setEasingCurve(QEasingCurve.InOutQuad)

        # Buttons fade (simultaneous)
        self.buttons_anim = []
        for btn in [self.start_button, self.help_button, self.about_button]:
            eff = QGraphicsOpacityEffect(btn)
            btn.setGraphicsEffect(eff)
            eff.setOpacity(0.0)

            anim = QPropertyAnimation(eff, b"opacity", self)
            anim.setDuration(400)
            anim.setStartValue(0.0)
            anim.setEndValue(1.0)
            anim.setEasingCurve(QEasingCurve.InOutQuad)
            self.buttons_anim.append(anim)

        # Chain: title -> subtitle -> buttons
        self.title_anim.finished.connect(self.subtitle_anim.start)
        self.subtitle_anim.finished.connect(self.start_buttons_anim)

        # Start chain
        self.title_anim.start()

    def start_buttons_anim(self):
        """Fade all buttons in together."""
        for anim in self.buttons_anim:
            anim.start()

    # -------------------------------------------------------------------------
    # Particle/Starfield Implementation
    # -------------------------------------------------------------------------
    def init_particles(self):
        """
        Initialize a list of particles for the starfield effect.
        Each particle is a dict with:
          x, y, speed, alpha, size
        """
        self.particles = []
        for _ in range(self.num_particles):
            self.particles.append({
                'x': random.uniform(0, self.width()),
                'y': random.uniform(0, self.height()),
                'speed': random.uniform(0.5, 2.5),
                'alpha': random.uniform(0.3, 1.0),
                'size': random.uniform(1.0, 3.0)
            })

    def update_particles(self):
        """
        Move and fade out each particle. If it goes off screen or too faint, reset it.
        """
        for p in self.particles:
            p['y'] += p['speed']
            # Fade it slightly
            p['alpha'] -= 0.005 * random.uniform(0.5, 1.5)

            # If off-screen or nearly invisible, respawn near top
            if p['y'] > self.height() or p['alpha'] < 0.1:
                p['x'] = random.uniform(0, self.width())
                p['y'] = -10.0  # Just above top
                p['speed'] = random.uniform(0.5, 2.5)
                p['alpha'] = random.uniform(0.5, 1.0)
                p['size'] = random.uniform(1.0, 3.0)

    # -------------------------------------------------------------------------
    # Animation Timer
    # -------------------------------------------------------------------------
    def update_animation(self):
        """
        Called ~30 times/sec:
         - Shift the rainbow gradient
         - Update starfield
         - Repaint
        """
        self.gradient_counter += 1
        self.update_particles()
        self.update()

    # -------------------------------------------------------------------------
    # Painting the Gradient + Starfield
    # -------------------------------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        # 1) Draw the rainbow gradient background
        shift = self.gradient_counter * 0.5
        r = 120 + 50 * math.sin(math.radians(shift))
        g = 120 + 50 * math.sin(math.radians(shift + 120))
        b = 120 + 50 * math.sin(math.radians(shift + 240))

        r2 = 120 + 50 * math.sin(math.radians(shift + 60))
        g2 = 120 + 50 * math.sin(math.radians(shift + 180))
        b2 = 120 + 50 * math.sin(math.radians(shift + 300))

        start_color = QColor(int(r), int(g), int(b))
        end_color = QColor(int(r2), int(g2), int(b2))

        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        gradient.setColorAt(0, start_color)
        gradient.setColorAt(1, end_color)

        painter.fillRect(rect, gradient)

        # 2) Draw the starfield on top
        for p in self.particles:
            alpha_clamped = max(0.0, min(1.0, p['alpha']))
            particle_color = QColor(255, 255, 255, int(alpha_clamped * 255))
            painter.setBrush(particle_color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(p['x']), int(p['y']),
                                int(p['size']), int(p['size']))

        # Let the normal UI draw last (e.g. labels, buttons)
        super().paintEvent(event)


def main():
    app = QApplication(sys.argv)
    window = AnimatedBackgroundWidget()
    if window.exec_() == QDialog.Accepted:
        print("User clicked Start! Proceed to main window...")
    sys.exit(0)

if __name__ == "__main__":
    main()


