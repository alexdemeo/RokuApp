from PyQt5.QtWidgets import QMessageBox


def show_warning(top_text, bottom_text, settings=None):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(top_text)
    msg.setInformativeText(bottom_text)
    if settings:
        msg.setWindowTitle(settings.get_title())
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()
