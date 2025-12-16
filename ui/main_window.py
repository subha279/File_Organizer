from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(640, 420)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        top = QHBoxLayout()
        layout.addLayout(top)

        self.update_btn = QPushButton("⟳")
        self.update_btn.clicked.connect(self.update_app)
        top.addStretch()
        top.addWidget(self.update_btn)

        self.status = QLabel("Ready")
        layout.addWidget(self.status)

        btn_row = QHBoxLayout()
        layout.addLayout(btn_row)

        start_btn = QPushButton("Start Organizing")
        start_btn.clicked.connect(self.start)
        btn_row.addWidget(start_btn)

        undo_btn = QPushButton("Undo")
        undo_btn.clicked.connect(self.undo)
        btn_row.addWidget(undo_btn)

    def start(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if not folder:
            return

        if (
            QMessageBox.question(self, APP_NAME, "Organize all files in this folder?")
            != QMessageBox.StandardButton.Yes
        ):
            return

        moved = organize(folder, self.set_status)
        QMessageBox.information(self, APP_NAME, f"Moved {moved} files")

    def undo(self):
        undo_all()
        QMessageBox.information(self, APP_NAME, "Undo completed")

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

    def set_status(self, text):
        self.status.setText(text)
