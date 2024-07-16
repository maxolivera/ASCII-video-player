from pathlib import Path
import logging
import cv2 as cv
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QProgressBar,
    QPushButton,
    QSlider,
    QStyle,
    QVBoxLayout,
    QWidget,
)
from src.graphics.processing import frame_2_ascii


class AsciiVideoPlayer(QWidget):
    def __init__(self, button: QPushButton, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.video_path: str = ""
        self.ascii_frame_function = frame_2_ascii

        self.frames_list: list[str] = []
        self.current_frame_idx: int = 0
        self.is_playing: bool = False
        self.fps: float = 0

        # Progress bar utilized when processing the video
        self.progress_bar = QProgressBar(self)
        self.progress_bar.hide()
        # Slider to move over the video
        self.slider = QSlider(Qt.Horizontal)
        self.slider.hide()
        self.slider.setRange(0, 0)
        _ = self.slider.valueChanged.connect(self.set_position)
        # Text label that shows the ASCII frame
        self.label: QLabel = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Choose your video!")
        # Title label that shows the name of the file
        self.title: QLabel = QLabel(self)
        self.title.hide()
        self.title.setAlignment(Qt.AlignCenter)

        self.play_button = button
        _ = self.play_button.clicked.connect(self.toggle_play)

        self.timer: QTimer = QTimer(self)
        _ = self.timer.timeout.connect(self.next_frame)

        layout: QVBoxLayout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        layout.addWidget(self.progress_bar)

    def load_video(self) -> None:
        video = cv.VideoCapture(self.video_path)
        frames_count: int = int(video.get(cv.CAP_PROP_FRAME_COUNT))
        self.fps = video.get(cv.CAP_PROP_FPS)
        logging.info("Starting frame processing")
        self.label.setText("Processing video...")
        self.progress_bar.setRange(0, int(frames_count // self.fps))
        self.progress_bar.show()
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break
            ascii_frame = self.ascii_frame_function(frame)
            self.frames_list.append(ascii_frame)
            if len(self.frames_list) % self.fps == 0:
                self.progress_bar.setValue(self.progress_bar.value() + 1)
            logging.debug(f"Processing frame {len(self.frames_list)}")

        video.release()
        logging.info("Finish frame processing")
        self.label.setFont(QFont("Courier", 5))
        if self.frames_list:
            print(f"The first frame is:\n'{self.frames_list[0]}'")

            self.progress_bar.hide()

            self.title.setText(Path(self.video_path).name)
            self.title.show()

            self.slider.setRange(0, len(self.frames_list) + 1)
            self.slider.show()

            self.label.setText(self.frames_list[0])
            self.play_button.setEnabled(True)

    def toggle_play(self) -> None:
        if self.is_playing:
            self.timer.stop()
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.timer.start(int(1000 // self.fps))
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.is_playing = not self.is_playing

    def next_frame(self) -> None:
        if self.current_frame_idx < len(self.frames_list):
            self.current_frame_idx += 1
        else:
            self.current_frame_idx = 0  # Reset to start

        self.label.setText(self.frames_list[self.current_frame_idx])
        self.slider.setValue(self.current_frame_idx)

    def set_position(self, position: int) -> None:
        self.label.setText(self.frames_list[position])
        self.current_frame_idx = position
