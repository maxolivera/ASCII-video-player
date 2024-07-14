import logging
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QPushButton, QSlider, QStyle, QWidget, QApplication, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from src.gui.ascii_label import AsciiVideoPlayer

class App(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("ASCII video player")
        self.setGeometry(640, 100, 700, 500)

        # Pallets
        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.ascii_label = QLabel(self)

        # Initialize user interface
        self.__init_ui__()

        # Display the window
        self.show()

    def __init_ui__(self):
        # Button to open video files
        open_button = QPushButton()
        open_button.clicked.connect(self.open_file)

        # Button to play or pause video
        self.play_button = QPushButton()
        self.play_button.setEnabled(False)
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        # ASCII Label
        self.asciiPlayer = AsciiVideoPlayer(self.play_button)

        # Slider for seeking within the video
        # self.slider = QSlider(Qt.Hoirzontal)
        # self.slider.setRange(0,0)
        # self.slider.sliderMoved.connect(self.set_position)

        # Create a Horitonal Box Layout for arraging widgets horizontally

        hbox_layout = QHBoxLayout()
        hbox_layout.setContentsMargins(0,0,0,0)
        hbox_layout.addWidget(open_button)
        hbox_layout.addWidget(self.play_button)

        # Create a Vertical Box Layout for arragning widgets vertically
        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(self.asciiPlayer)
        # vbox_layout.addWidget(self.slider)
        vbox_layout.addLayout(hbox_layout)

        # Set the layout of the window
        self.setLayout(vbox_layout)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, caption="Open video",
                                                  filter="Videos (*.mp4)")
        if filename != "":
            logging.info(f"File selected: '{filename}'")
            self.asciiPlayer.video_path = filename
            _ = self.asciiPlayer.load_video()
