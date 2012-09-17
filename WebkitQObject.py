from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class WebkitQObject(QObject):
  def __init__(self):
    super(WebkitQObject, self).__init__()
    self.__cache__ = []

  def store(self, item):
    self.__cache__.append(item)

    return self.__cache__[-1]