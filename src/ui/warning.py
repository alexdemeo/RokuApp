from PyQt5.QtWidgets import QMessageBox


def show_warning(settings, top_text, bottom_text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(top_text)
    msg.setInformativeText(bottom_text)
    msg.setWindowTitle(settings.get_title())
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()
