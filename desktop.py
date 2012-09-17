import re, os, glob, subprocess, ConfigParser

from WebkitQObject import WebkitQObject

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class DesktopLauncher(QObject):
  def __init__(self, path):
    super(DesktopLauncher, self).__init__()

    self.path = path
    self.config = ConfigParser.SafeConfigParser()
    self.config.read(self.path)

    self.icon = QIcon.fromTheme(self.config.get('Desktop Entry', 'Icon'))

  @pyqtSlot(int, result=str)
  def icon(self, size=64):
    size = QSize(size, size)

    pixmap = self.icon.pixmap(size * 1.1).scaled(size, transformMode=Qt.SmoothTransformation)
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    buffer.open(QIODevice.WriteOnly)
    pixmap.save(buffer, 'PNG')

    return 'data:image/png;base64,' + str(byte_array.toBase64())

  @pyqtSlot()
  def launch(self):
    with open(self.path, 'r') as handle:
      try:
        command = re.search(r'\bExec=(.*?)\n', handle.read()).group(1)
      except AttributeError:
        return False

    return subprocess.call(command, shell=True)



  @pyqtProperty(str)
  def name(self):
    return self.config.get('Desktop Entry', 'Name')





class Desktop(WebkitQObject):
  def __init__(self, path='~/Desktop'):
    super(Desktop, self).__init__()

    self.path = os.path.expanduser(path)

  @pyqtProperty(QVariant)
  def launchers(self):
    launchers = []

    for path in sorted(glob.glob(os.path.join(self.path, '*.desktop'))):
      launcher = DesktopLauncher(path)

      launchers.append(launcher)

    return self.store(launchers)