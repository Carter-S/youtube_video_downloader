from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QHBoxLayout, QWidget

class LinkInputWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Give the window a title
        self.setWindowTitle("Youtube Video Downloader")

        #Define a layout for the window
        layout = QHBoxLayout()

        #Create a widget which a youtube link can be input into
        self.link_input = QLineEdit()

        #Create a button for submitting a link
        link_submit = QPushButton("Submit")
        link_submit.clicked.connect(self.link_submitted)

        layout.addWidget(self.link_input)
        layout.addWidget(link_submit)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def link_submitted(self):
        print(self.link_input.text())

        
app = QApplication([])

window = LinkInputWindow()
window.show()

app.exec()
