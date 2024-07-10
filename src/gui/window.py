from tkinter import Tk, Canvas

class Window():
    def __init__(self, width: int, height:int) -> None:
        self.__active = False
        self.__root = Tk()
        self.__root.title("ASCII Video Player")
        self.canvas = Canvas(
                self.__root,
                height=height,
                width=width,
                background=BACKGROUND
        )
