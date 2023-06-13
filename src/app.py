
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QHBoxLayout, QWidget, QLabel, QVBoxLayout, QFileDialog, QComboBox
from pytube import YouTube
import traceback

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_window = None
        #Give the window a title
        self.setWindowTitle("Youtube Video Downloader")

        #Define a layout for the window
        layout = QHBoxLayout()

        #Create a widget which a youtube link can be input into
        self.link_input = QLineEdit()

        #Create a button for submitting a link
        link_submit = QPushButton("Submit")
        link_submit.clicked.connect(self.link_submitted)

        #Add the widgets to the layout
        layout.addWidget(self.link_input)
        layout.addWidget(link_submit)

        page = QWidget()
        page.setLayout(layout)
        self.setCentralWidget(page)


    def link_submitted(self):
        print(self.link_input.text())
        try:
            video = YouTube(self.link_input.text())
            print("SUCCESS! VALID LINK!")
            self.data_window = VideoDataWindow(video)
            self.data_window.show()
        except:
            print("ERROR! INVALID LINK!")


class VideoDataWindow(QWidget):
    def __init__(self, video):
        self.video = video
        super().__init__()
        layout = QVBoxLayout()
        self.select_stream = QPushButton("Download")
        self.select_stream.clicked.connect(self.download_stream)
        self.dropdown = QComboBox()
        for stream in self.video.streams.filter(file_extension='mp4'):
            s = self.dropdown.addItem(str(stream))
        layout.addWidget(self.dropdown)
        layout.addWidget(self.select_stream)
        self.setLayout(layout)

    def download_stream(self):
        index = self.dropdown.currentIndex()
        stream = self.video.streams.filter(file_extension='mp4')[index]
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        stream.download(output_path=file)
        self.close()
            


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
