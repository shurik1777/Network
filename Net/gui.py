import wx
from switch_manager import run_switch_manager


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(400, 250))

        panel = wx.Panel(self)

        self.ip_label = wx.StaticText(panel, label="IP:", pos=(20, 20))
        self.ip_text = wx.TextCtrl(panel, pos=(100, 20), size=(200, -1))

        self.username_label = wx.StaticText(panel, label="Username:", pos=(20, 60))
        self.username_text = wx.TextCtrl(panel, pos=(100, 60), size=(200, -1))

        self.password_label = wx.StaticText(panel, label="Password:", pos=(20, 100))
        self.password_text = wx.TextCtrl(panel, pos=(100, 100), size=(200, -1), style=wx.TE_PASSWORD)

        self.button = wx.Button(panel, label="Run Switch Manager", pos=(150, 150))
        self.Bind(wx.EVT_BUTTON, self.on_button_click, self.button)

    def on_button_click(self, event):
        ip = self.ip_text.GetValue()
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()

        if ip and username and password:
            run_switch_manager(ip, username, password)
        else:
            wx.MessageBox("Please enter IP, username, and password.", "Input Error", wx.OK | wx.ICON_ERROR)


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, "Switch Manager GUI")
    frame.Show()
    app.MainLoop()
