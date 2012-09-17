#!/usr/bin/env python2

import os, re, sys, json, datetime, time, glob, ConfigParser, subprocess
from functools import wraps

import psutil

import dbus

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

from dbus.mainloop.qt import DBusQtMainLoop

from WebkitQObject import WebkitQObject
from desktop import DesktopLauncher, Desktop
from music import MusicBackend

try:
  from cStringIO import StringIO
except:
  from StringIO import StringIO

DBusQtMainLoop(set_as_default=True)


def cached_property(function):
  result = None

  @wraps(function)
  def wrapper(*args, **kwargs):
    if result:
      return result

    result = function(*args, **kwargs)

    return result
  return wrapper


def debug(function):
  @wraps(function)
  def wrapper(*args, **kwargs):
    result = function(*args, **kwargs)

    print '{}() -> {}'.format(function.__name__, result)

    return result

  return wrapper



class WebkitQObject(QObject):
  def __init__(self):
    super(WebkitQObject, self).__init__()
    self.__cache__ = []

  def store(self, item):
    self.__cache__.append(item)

    return self.__cache__[-1]



class System(QObject):
  def __init__(self):
    super(System, self).__init__()

  @pyqtProperty(QVariant)
  @debug
  def ram(self):
    return dict(psutil.phymem_usage().__dict__)

  @pyqtSlot(QVariant)
  @debug
  def cpu(self):
    return {
      'usage': psutil.cpu_percent(),
      'cores': psutil.cpu_percent(percpu=True)
    }



class Background(QWebView):
  def __init__(self):
    super(Background, self).__init__()

    self.resize(QApplication.desktop().size())
    geometry = self.frameGeometry()
    geometry.moveCenter(QDesktopWidget().availableGeometry().center())
    self.move(geometry.topLeft())

    self.frame = self.page().mainFrame()

    self.settings = QWebSettings.globalSettings()
    self.settings.setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
    self.settings.setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
    self.settings.setAttribute(QWebSettings.LocalContentCanAccessFileUrls, True)
    self.settings.setAttribute(QWebSettings.LocalStorageEnabled, True)
    self.settings.setAttribute(QWebSettings.AutoLoadImages, True)

    self.setAttribute(Qt.WA_X11NetWmWindowTypeDesktop)


    system_info = System()
    music_info = MusicBackend()
    desktop_info = Desktop()

    self.frame.addToJavaScriptWindowObject('system', system_info)
    self.frame.addToJavaScriptWindowObject('desktop', desktop_info)
    self.frame.addToJavaScriptWindowObject('music', music_info)

  def load_theme(self, name):
    path = os.path.abspath('themes/{name}/index.html'.format(name=name))

    if not os.path.exists(path):
      return False

    self.load(QUrl.fromLocalFile(path))
    self.load(QUrl('http://gridster.net/'))
    
    return True


        

if __name__ == '__main__':
  app = QApplication(sys.argv)
  
  background = Background()
  background.load_theme('text')
  background.show()

  sys.exit(app.exec_())
