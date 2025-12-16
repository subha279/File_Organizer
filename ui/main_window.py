from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.config import APP_NAME
from app.organizer import organize
from app.undo import undo_all
from app.updater import apply_update, check_update

# ---------------- THEMES (QSS) ---------------- #

DARK_THEME = """
QMainWindow {
    background-color: #121212;
}

#Header {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #1e3c72,
        stop:1 #2a5298
    );
    border-radius: 12px;
}

QLabel {
    color: #ffffff;
    font-size: 14px;
}

#Title {
    font-size: 20px;
    font-weight: bold;
}

QPushButton {
    background-color: #1f2937;
    color: white;
    border-radius: 12px;
    padding: 10px 18px;
}

QPushButton:hover {
    background-color: #374151;
}

QPushButton#Primary {
    background-color: #00c853;
    color: black;
    font-weight: bold;
}

QPushButton#Primary:hover {
    background-color: #00e676;
}
"""

LIGHT_THEME = """
QMainWindow {
    background-color: #f5f5f5;
}

#Header {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #56ccf2,
        stop:1 #2f80ed
    );
    border-radius: 12px;
}

QLabel {
    color: #000000;
    font-size: 14px;
}

#Title {
    font-size: 20px;
    font-weight: bold;
}

QPushButton {
    background-color: #ffffff;
    color: #000000;
    border-radius: 12px;
    padding: 10px 18px;
    border: 1px solid #dddddd;
}

QPushButton:hover {
    background-color: #eeeeee;
}

QPushButton#Primary {
    background-color: #2f80ed;
    color: white;
    font-weight: bold;
}

QPushButton#Primary:hover {
    background-color: #1366d6;
}
"""


# ---------------- MAIN WINDOW ---------------- #


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(680, 460)

        self.dark_mode = True
        self.setStyleSheet(DARK_THEME)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # ---------- HEADER ---------- #
        header = QWidget()
        header.setObjectName("Header")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)

        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setFixedSize(40, 40)
        self.theme_btn.clicked.connect(self.toggle_theme)

        title = QLabel(APP_NAME)
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.update_btn = QPushButton("⟳")
        self.update_btn.setFixedSize(40, 40)
        self.update_btn.clicked.connect(self.update_app)

        header_layout.addWidget(self.theme_btn)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.update_btn)

        main_layout.addWidget(header)

        # ---------- STATUS ---------- #
        self.status = QLabel("Ready")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status)

        # ---------- ACTION BUTTONS ---------- #
        action_row = QHBoxLayout()
        action_row.setSpacing(20)

        start_btn = QPushButton("Start Organizing")
        start_btn.setObjectName("Primary")
        start_btn.clicked.connect(self.start)

        undo_btn = QPushButton("Undo / Restore")
        undo_btn.clicked.connect(self.undo)

        action_row.addStretch()
        action_row.addWidget(start_btn)
        action_row.addWidget(undo_btn)
        action_row.addStretch()

        main_layout.addLayout(action_row)

    # ---------------- LOGIC ---------------- #

    def start(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if not folder:
            return

        if (
            QMessageBox.question(
                self,
                APP_NAME,
                "This will organize ALL files in the selected folder.\n\nContinue?",
            )
            != QMessageBox.StandardButton.Yes
        ):
            return

        moved = organize(folder, self.set_status)
        QMessageBox.information(self, APP_NAME, f"Files moved: {moved}")
        self.set_status("Ready")

    def undo(self):
        undo_all()
        QMessageBox.information(self, APP_NAME, "Undo completed")
        self.set_status("Ready")

    def update_app(self):
        has, version, url = check_update()
        if not has:
            QMessageBox.information(self, APP_NAME, "Already up to date")
            return

        if (
            QMessageBox.question(self, APP_NAME, f"Update to version {version}?")
            == QMessageBox.StandardButton.Yes
        ):
            apply_update(url)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.setStyleSheet(DARK_THEME if self.dark_mode else LIGHT_THEME)
        self.theme_btn.setText("🌙" if self.dark_mode else "☀️")

    def set_status(self, text):
        self.status.setText(text)
