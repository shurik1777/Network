import wx  # Импорт библиотеки wxPython для создания графического интерфейса
from switch_manager import run_switch_manager  # Импорт функции run_switch_manager из другого файла


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(400, 250))  # Создание окна приложения

        panel = wx.Panel(self)  # Создание панели для размещения элементов интерфейса

        # Создание надписей и текстовых полей для ввода IP, имени пользователя и пароля
        self.ip_label = wx.StaticText(panel, label="IP:", pos=(20, 20))
        self.ip_text = wx.TextCtrl(panel, pos=(100, 20), size=(200, -1))

        self.username_label = wx.StaticText(panel, label="Username:", pos=(20, 60))
        self.username_text = wx.TextCtrl(panel, pos=(100, 60), size=(200, -1))

        self.password_label = wx.StaticText(panel, label="Password:", pos=(20, 100))
        self.password_text = wx.TextCtrl(panel, pos=(100, 100), size=(200, -1), style=wx.TE_PASSWORD)

        # Создание кнопки "Run Switch Manager" и связывание её с методом on_button_click
        self.button = wx.Button(panel, label="Run Switch Manager", pos=(150, 150))
        self.Bind(wx.EVT_BUTTON, self.on_button_click, self.button)

    def on_button_click(self, event):
        # Получение введенных значений IP, имени пользователя и пароля
        ip = self.ip_text.GetValue()
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()

        # Проверка, что все поля заполнены, и выполнение функции run_switch_manager
        if ip and username and password:
            run_switch_manager(ip, username, password)
        else:
            # Вывод сообщения об ошибке, если не все поля заполнены
            wx.MessageBox("Please enter IP, username, and password.", "Input Error", wx.OK | wx.ICON_ERROR)


if __name__ == "__main__":
    app = wx.App(False)  # Создание экземпляра приложения
    frame = MyFrame(None, "Switch Manager GUI")  # Создание окна приложения
    frame.Show()  # Отображение окна
    app.MainLoop()  # Запуск цикла обработки событий приложения

