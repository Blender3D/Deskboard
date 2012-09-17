import re

from functools import wraps

from WebkitQObject import WebkitQObject

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import dbus

from dbus.mainloop.qt import DBusQtMainLoop
DBusQtMainLoop(set_as_default=True)

def dbus_clean(function):
  regex = re.compile(r'<type \'_dbus_bindings\._(.*?)Base\'>')

  def clean(value):
    base = type(value).__bases__[0]
    matched = regex.findall(repr(base))

    if matched:
      return eval(matched[0].lower())(value)
    else:
      return base(value)

  @wraps(function)
  def wrapper(*args, **kwargs):
    return {clean(key).replace('-', '_'): clean(value) for key, value in function(*args, **kwargs).iteritems()}

  return wrapper



class MusicBackend(WebkitQObject):
  playback_changed = pyqtSignal(str)
  track_seek = pyqtSignal(int)

  def __init__(self):
    super(MusicBackend, self).__init__()

    self.bus = dbus.SessionBus()
    self.dbus_services = self.bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')

    if 'org.bansheeproject.Banshee' in self.services():
      self.player = self.bus.get_object('org.bansheeproject.Banshee', '/org/bansheeproject/Banshee/PlayerEngine')

      self.player.connect_to_signal('StateChanged', self.state_changed_signal)
      self.player.connect_to_signal('EventChanged', self.state_changed_signal)
    else:
      self.player = None
  
  def state_changed_signal(self, *args):
    print args

    if args[0] in ['playing', 'paused', 'idle']:
      self.playback_changed.emit(str(args[0]))
    elif args[0] in ['startofstream']:
      self.playback_changed.emit('playing')
    elif args[0] in ['seek']:
      self.track_seek.emit(self._remaining())
    #self.state_changed.emit(args)

  def services(self):
    return self.dbus_services.ListNames()
  
  @pyqtProperty(QVariant)
  def remaining(self):
    return self._remaining()

  def _remaining(self):
    current, length = int(self.player.GetPosition()), int(self.player.GetLength())
    remaining = (length - current) / 1000

    return remaining



  @pyqtProperty(QVariant)
  def state(self):
    if not self.player:
      return 'idle'

    return str(self.player.GetCurrentState())

  @pyqtProperty(QVariant)
  @dbus_clean
  def current_track(self):
    return self.player.GetCurrentTrack()