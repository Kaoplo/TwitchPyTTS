import sys

from PySide6.QtWidgets import QApplication
from src.TTSengine.TTSmain import MainWindow

# TODO: Redo the file structure, move all the TTS engine stuff to a separate folder

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
