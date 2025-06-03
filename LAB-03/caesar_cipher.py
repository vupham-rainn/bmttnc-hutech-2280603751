import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPlainTextEdit # Thêm QPlainTextEdit để làm rõ nếu cần
from ui.caesar import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": self.ui.txt_plain.toPlainText(),  # Đã sửa thành toPlainText()
            "key": self.ui.txt_key.toPlainText()             # Đã sửa thành toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher.setPlainText(data["encrypted_message"]) # Đã sửa thành setPlainText()

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API: Status code", response.status_code)
                print("Response:", response.text) # In thêm nội dung phản hồi để debug
        except requests.exceptions.RequestException as e:
            print("Network Error:", str(e))
        except Exception as e: # Bắt các lỗi khác có thể xảy ra
            print("An unexpected error occurred:", str(e))


    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": self.ui.txt_cipher.toPlainText(),  # Đã sửa thành toPlainText()
            "key": self.ui.txt_key.toPlainText()              # Đã sửa thành toPlainText()
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain.setPlainText(data["decrypted_message"]) # Đã sửa thành setPlainText()

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API: Status code", response.status_code)
                print("Response:", response.text) # In thêm nội dung phản hồi để debug
        except requests.exceptions.RequestException as e:
            print("Network Error:", str(e))
        except Exception as e: # Bắt các lỗi khác có thể xảy ra
            print("An unexpected error occurred:", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())