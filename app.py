import sys

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QApplication, QAbstractItemView, QDoubleSpinBox, QFileDialog,
    QHBoxLayout, QLabel, QListWidget, QMainWindow, QMessageBox,
    QProgressBar, QPushButton, QVBoxLayout, QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Cutter")
        self.resize(760, 520)

        root = QWidget()
        layout = QVBoxLayout(root)

        controls = QHBoxLayout()
        self.add_button = QPushButton("Добавить видео")
        self.output_button = QPushButton("Папка сохранения")
        controls.addWidget(self.add_button)
        controls.addWidget(self.output_button)

        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel("Длина куска (сек):"))
        self.length = QDoubleSpinBox()
        self.length.setRange(0.1, 3600)
        self.length.setValue(5.0)
        length_layout.addWidget(self.length)

        self.files = QListWidget()
        self.files.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)

        actions = QHBoxLayout()
        self.remove_button = QPushButton("Удалить выбранные")
        self.cut_button = QPushButton("Нарезать")
        self.shuffle_button = QPushButton("Перемешать")
        actions.addWidget(self.remove_button)
        actions.addWidget(self.cut_button)
        actions.addWidget(self.shuffle_button)

        layout.addLayout(controls)
        layout.addLayout(length_layout)
        layout.addWidget(self.files)
        layout.addWidget(self.progress)
        layout.addLayout(actions)
        self.setCentralWidget(root)

        self.output_dir = ""
        self.add_button.clicked.connect(self.choose_files)
        self.output_button.clicked.connect(self.choose_output)
        self.remove_button.clicked.connect(self.remove_selected)

    def choose_files(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
            self, "Выберите видео", "",
            "Видео (*.mp4 *.mkv *.avi *.mov *.webm *.mpeg *.mpg *.wmv);;Все файлы (*)",
        )
        for file in files:
            if not any(self.files.item(i).text() == file for i in range(self.files.count())):
                self.files.addItem(file)

    def choose_output(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Папка сохранения")
        if directory:
            self.output_dir = directory
            self.output_button.setText(directory)

    def remove_selected(self) -> None:
        for item in self.files.selectedItems():
            self.files.takeItem(self.files.row(item))


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
