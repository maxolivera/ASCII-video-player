import logging
import cv2 as cv
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from src.graphics.processing import frame_2_ascii

class AsciiVideoPlayer(QWidget):
    def __init__(
            self,
            button: QPushButton,
            parent: QWidget|None = None
        ) -> None:
        super().__init__(parent)
        self.video_path:str = ""
        self.ascii_frame_function = frame_2_ascii

        self.frames_list: list[str] = []
        self.current_frame_idx: int = 0
        self.is_playing: bool = False
        self.fps: float = 0

        self.label: QLabel = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Choose your video!")

        self.play_button = button
        _ = self.play_button.clicked.connect(self.toggle_play)

        self.timer: QTimer = QTimer(self)
        _ = self.timer.timeout.connect(self.next_frame)

        layout: QVBoxLayout = QVBoxLayout(self)
        layout.addWidget(self.label)

    def load_video(self) -> None:
        self.label.setText("Processing video...")
        video = cv.VideoCapture(self.video_path)
        frames_count: int = int(video.get(cv.CAP_PROP_FRAME_COUNT))
        self.fps = video.get(cv.CAP_PROP_FPS) 
        logging.info("Starting frame processing")
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break
            ascii_frame = self.ascii_frame_function(frame)
            ascii_frame = ascii_frame.replace(" ", "\u00A0")
            self.frames_list.append(ascii_frame)
            logging.debug(f"Processing frame {len(self.frames_list)}")
            self.label.setText(progress_bar(len(self.frames_list), frames_count))
            QApplication.processEvents()

        video.release()
        logging.info("Finish frame processing")
        self.label.setFont(QFont("Courier", 5))
        if self.frames_list:
            print(f"The first frame is:\n'{self.frames_list[0]}'")
            self.label.setText(self.frames_list[0])
            self.play_button.setEnabled(True)

    def toggle_play(self) -> None:
        if self.is_playing:
            self.timer.stop()
        else:
            self.timer.start(int(1000 // self.fps))
        self.is_playing = not self.is_playing

    def next_frame(self) -> None:
        if self.current_frame_idx < len(self.frames_list):
            self.label.setText(self.frames_list[self.current_frame_idx])
            self.current_frame_idx += 1
        else:
            self.timer.stop()
            self.is_playing = False
            self.current_frame_idx = 0 # Reset to start


def progress_bar(current: int, total: int, bar_length: int=20) -> str:
    fraction: float = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    ending = '\n' if current == total else '\r'

    return f"Progress: [{arrow}{padding}] {int(fraction*100)}%" + ending

