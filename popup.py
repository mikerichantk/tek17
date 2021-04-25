from PyQt5.QtWidgets import QMessageBox

__author__ = "Cole French, Chris Lytle, Alexander Nowlin, Pouya Rad"
__copyright__ = "Copyright 2017-19, Tektronix Inc."
__credits__ = ["Cole French", "Chris Lytle", "Alexander Nowlin", "Pouya Rad"]


# Creates a popup error display message for when there is an error in the application.
# Parameters:
#   error_message <str> : Error Message that will be displayed on the window
#   details <str> : Any additional details to add to the window.  This will be displayed
#                   when the user clicks the details button.
def show_error_message(error_message: str, details: str = None):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)

    msg.setText("Error")
    msg.setInformativeText(error_message)
    msg.setWindowTitle("Error Message")
    msg.setStandardButtons(QMessageBox.Ok)
    if details is not None:
        msg.setDetailedText(details)
    msg.exec_()


# Creates a popup information display message for when there is an error in the application.
# Parameters:
#   error_message <str> : Information Message that will be displayed on the window
#   details <str> : Any additional details to add to the window.  This will be displayed
#                   when the user clicks the details button.
def show_information_message(info_message: str, details: str = None):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setText("Done Training")
    msg.setInformativeText(info_message)
    msg.setWindowTitle("Information Message")
    msg.setStandardButtons(QMessageBox.Ok)
    if details is not None:
        msg.setDetailedText(details)
    msg.exec_()
