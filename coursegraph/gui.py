import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

# ui 파일이 실행 파일과 같은 위치에 있어야 함.
form_class = uic.loadUiType("Maingui.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.action_open.triggered.connect(self.openFunction) 
        self.action_othernamesave.triggered.connect(self.saveAsFunction) 
        self.pushButton.clicked.connect(self.clearImage)

    

    def openFunction(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.gif)")
        if filename:  # 파일이 선택되었는지 확인
            pixmap = QPixmap(filename)  # 파일을 QPixmap 객체로 로드
            if not pixmap.isNull():  # 유효한 이미지 파일인지 확인
                self.label.setPixmap(pixmap)
                self.label.setScaledContents(True)  # 이미지 크기에 맞게 QLabel 크기 조정
                self.label.adjustSize()  # QLabel 크기 조정
                self.adjustSize()  # 윈도우 크기 조정
                self.statusBar().showMessage(f"Opened image: {filename}", 5000)  # 상태바에 메시지 표시
                self.addRecentFile(filename)  # 최근 파일 목록에 추가
            else:
                QMessageBox.warning(self, "유효하지 않은 이미지 파일입니다.")
        else:
            return

    def clearImage(self):
        self.label.clear()  # QLabel에 표시된 이미지 제거

    def saveAsFunction(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(self, "Save Image As", "", "PNG Files (*.png);;JPEG Files (*.jpg);;BMP Files (*.bmp);;GIF Files (*.gif)")
            if filename:  # 파일이 선택되었는지 확인
                pixmap = self.label.pixmap()  # QLabel에 표시된 이미지 가져오기
                if pixmap:
                    pixmap.save(filename)  # 이미지를 지정된 파일 경로에 저장
                else:
                    QMessageBox.warning(self, "Warning", "이미지가 없습니다.", QMessageBox.Ok)
        except TypeError:
            QMessageBox.warning(self, "Warning", "파일 저장에 실패했습니다.", QMessageBox.Ok)

# 에러 발생 시 정상 종료하도록 정의
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = exception_hook
app = QApplication(sys.argv)
myWindow = WindowClass()
myWindow.show()
app.exec_()
