
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QHBoxLayout, QWidget, QLabel, QVBoxLayout, QFileDialog, QComboBox
from PyQt5.QtGui import QPixmap, QIcon
import urllib, traceback, time
from pytube import YouTube

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
            self.data_window.setMinimumSize(QSize(1000, 500))
            self.data_window.show()
        except:
            print("ERROR! INVALID LINK!")


class VideoDataWindow(QWidget):
    def __init__(self, video):
        self.video = video
        super().__init__()

        main_layout = QVBoxLayout()

        #Video details section
        video_details = QHBoxLayout()
        thumbnail_url = self.video.thumbnail_url
        thumbnail_data = urllib.request.urlopen(thumbnail_url).read()
        thumbnail_pix = QPixmap()
        thumbnail_pix.loadFromData(thumbnail_data)
        thumbnail = QLabel()
        thumbnail.setPixmap(thumbnail_pix)
        video_details.addWidget(thumbnail)
        title_auth = QVBoxLayout()
        title = QLabel(self.video.title)
        auth = QLabel(self.video.author)
        title_auth.addWidget(title)
        title_auth.addWidget(auth)
        video_details.addLayout(title_auth)
        main_layout.addLayout(video_details)

        #Video stats section
        video_stats = QHBoxLayout()
        converted_length = time.strftime("%H:%M:%S", time.gmtime(self.video.length))
        string = "Video length: "+str(converted_length)
        video_length = QLabel(string)
        string = "Date published: "+str(self.video.publish_date.strftime("%m/%d/%Y"))
        date_published = QLabel(string)
        string = "Views: "+str(self.video.views)
        views = QLabel(string)
        video_stats.addWidget(video_length)
        video_stats.addWidget(date_published)
        video_stats.addWidget(views)

        main_layout.addLayout(video_stats)

        #Download options section
        download_options = QHBoxLayout()
        self.select_stream = QPushButton("Download")
        self.select_stream.clicked.connect(self.download_stream)
        self.dropdown = QComboBox()
        for stream in self.video.streams.filter(file_extension='mp4'):
            s = self.dropdown.addItem(str(stream))
        download_options.addWidget(self.dropdown)
        download_options.addWidget(self.select_stream)
        main_layout.addLayout(download_options)


        self.setLayout(main_layout)

    def download_stream(self):
        index = self.dropdown.currentIndex()
        stream = self.video.streams.filter(file_extension='mp4')[index]
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        stream.download(output_path=file)
        self.close()
            

app = QApplication([])

window = MainWindow()
window.setMinimumSize(QSize(500,500))
window.show()

app.exec()
