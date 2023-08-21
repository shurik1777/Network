import wx  # Импорт библиотеки wxPython для создания графического интерфейса
import threading  # Импорт библиотеки для работы с потоками
from switch_manager import run_switch_manager  # Импорт функции run_switch_manager из другого файла


# Определение класса MyFrame, наследующего от wx.Frame
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(400, 250))  # Создание окна приложения

        panel = wx.Panel(self)  # Создание панели для размещения элементов интерфейса

        self.ip_label = wx.StaticText(panel, label="IP:", pos=(20, 20))

        # Создаем выпадающий список для выбора начала IP-адреса
        self.ip_templates = ["192.168.10", "192.168.9", "172.18.12"]
        self.ip_choice = wx.Choice(panel, pos=(100, 20), choices=self.ip_templates)
        self.ip_choice.SetSelection(0)

        self.ip_suffix_text = wx.TextCtrl(panel, pos=(200, 20), size=(100, -1))

        self.username_label = wx.StaticText(panel, label="Username:", pos=(20, 60))
        self.username_text = wx.TextCtrl(panel, pos=(100, 60), size=(200, -1))

        self.password_label = wx.StaticText(panel, label="Password:", pos=(20, 100))
        self.password_text = wx.TextCtrl(panel, pos=(100, 100), size=(200, -1), style=wx.TE_PASSWORD)

        self.button = wx.Button(panel, label="Run Switch Manager", pos=(150, 150))
        self.Bind(wx.EVT_BUTTON, self.on_button_click, self.button)

        # Создаем флаг для определения, выполняется ли в данный момент процесс
        self.running = False

    # Обработчик события при нажатии на кнопку
    def on_button_click(self, event):
        if not self.running:
            self.running = True
            self.button.Disable()  # Отключаем кнопку
            selected_template = self.ip_templates[self.ip_choice.GetSelection()]
            ip_suffix = self.ip_suffix_text.GetValue()
            username = self.username_text.GetValue()
            password = self.password_text.GetValue()

            if selected_template and ip_suffix and username and password:
                full_ip = f"{selected_template}.{ip_suffix.rstrip('.')}"
                # Создаем отдельный поток для выполнения run_switch_manager
                thread = threading.Thread(target=self.run_manager, args=(full_ip, username, password))
                thread.start()
            else:
                wx.MessageBox("Please enter all required information.", "Input Error", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Processing is already in progress.", "Processing", wx.OK | wx.ICON_INFORMATION)

    # Метод для выполнения run_switch_manager в отдельном потоке
    def run_manager(self, ip, username, password):
        # Используйте wx.BusyInfo для отображения уведомления
        with wx.BusyInfo("Collecting data, please wait..."):
            run_switch_manager(ip, username, password)
        self.running = False
        self.button.Enable()  # Включаем кнопку после завершения


# Блок кода, выполняющийся при запуске программы
if __name__ == "__main__":
    app = wx.App(False)  # Создание экземпляра приложения
    frame = MyFrame(None, "Switch Manager GUI")  # Создание окна приложения
    frame.Show()  # Отображение окна
    app.MainLoop()  # Запуск цикла обработки событий приложения
