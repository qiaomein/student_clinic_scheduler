from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow

import sys
try:
    import SCS
except ImportError:
    print("ERROR: SCS COULD NOT BE IMPORTED")


if __name__ == "__main__":
    
    app = QApplication(sys.argv) # only one instance per app; passing in sys.argv allows command line args for the app


    window = QMainWindow()
    window.show() # always call this on a widget!

    app.exec() # run the app!