import npyscreen
import shlex
import socket
import threading
import time

class ActionController(npyscreen.ActionControllerSimple):

  def process_command_complete(self, command_line, widget):
    if command_line.startswith('/'):
      args = shlex.split(command_line)
    else:
      self.parent.sendLine(command_line)

class GameForm(npyscreen.FormMuttActive):
  ACTION_CONTROLLER = ActionController

  def sendLine(self, line):
    self.parentApp.sendLine(line)

class GameApp(npyscreen.NPSAppManaged):

  def onStart(self):
    self.form = self.addForm("MAIN", GameForm)
    self.form.add_handlers({
        '^Q': self.quit,
        })
    s = socket.socket()
    s.connect(('localhost', 9191))
    self.socket = s.makefile()
    thread = threading.Thread(target=self.readSocket)
    thread.daemon = True
    thread.start()

  def quit(self, *args, **kwargs):
    self.switchForm(None)

  def sendLine(self, line):
    self.socket.write(line + '\n')
    self.addLine(line)

  def addLine(self, line):
    self.form.wMain.values.append(line)
    self.form.wMain.display()

  def readSocket(self, writeLn):
    for line in self.socket:
      self.addLine(line)

if __name__ == "__main__":
  GameApp().run()
