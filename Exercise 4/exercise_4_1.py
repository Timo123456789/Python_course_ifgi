from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

view = QWebView()
url=QUrl("https://de.wikipedia.org/wiki/[%Name%]")

view.load(url)
view.show()