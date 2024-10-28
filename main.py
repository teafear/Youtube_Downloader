
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import yt_dlp

class YouTubeDownloaderApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 400, 200)
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        # CSS стили для оформления интерфейса
        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
                color: #D8DEE9;
                font-size: 14px;
            }
            QLineEdit, QPushButton, QLabel {
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #88C0D0;
                color: #2E3440;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
        """)

        # Поле для ввода ссылки
        self.link_label = QtWidgets.QLabel("Введите ссылку на YouTube:")
        self.link_input = QtWidgets.QLineEdit()
        self.link_input.setPlaceholderText("https://www.youtube.com/...")
        
        # Кнопка выбора папки для сохранения
        self.path_button = QtWidgets.QPushButton("Выбрать папку")
        self.path_button.clicked.connect(self.select_folder)
        
        # Кнопка для загрузки видео
        self.download_button = QtWidgets.QPushButton("Скачать")
        self.download_button.clicked.connect(self.download_video)
        
        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.link_label)
        layout.addWidget(self.link_input)
        layout.addWidget(self.path_button)
        layout.addWidget(self.download_button)
        
        self.setLayout(layout)

    def select_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if not self.folder_path:
            QMessageBox.warning(self, "Предупреждение", "Папка для загрузки не выбрана!")
    
    def download_video(self):
        url = self.link_input.text()
        if not url:
            QMessageBox.warning(self, "Предупреждение", "Введите ссылку на YouTube!")
            return
        if not hasattr(self, 'folder_path') or not self.folder_path:
            QMessageBox.warning(self, "Предупреждение", "Папка для загрузки не выбрана!")
            return
        
        try:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': f'{self.folder_path}/%(title)s.%(ext)s',
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                formats = info_dict.get('formats', [])

                # Получаем список доступных разрешений
                resolutions = [f"{fmt['format_id']} - {fmt['resolution']}" for fmt in formats if 'resolution' in fmt and fmt['ext'] == 'mp4']
                chosen_format, ok = QtWidgets.QInputDialog.getItem(
                    self, "Выберите разрешение", "Разрешения:", resolutions, 0, False)
                
                if ok and chosen_format:
                    # Скачиваем выбранное разрешение
                    ydl_opts['format'] = chosen_format.split(" ")[0]
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    QMessageBox.information(self, "Успех", "Видео успешно загружено!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = YouTubeDownloaderApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
