import wx  # Импорт библиотеки wxPython для создания графического интерфейса
import threading
from netmiko import ConnectHandler
import datetime
import logging
import configparser

# Конфигурационный файл
CONFIG_FILE = 'config.ini'

logging.basicConfig(filename='log_2.txt', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    encoding='UTF-8', )


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Введите параметры')
        panel = wx.Panel(self)

        # Загрузка настроек из файла
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILE)

        # Начальный IP
        self.start_label = wx.StaticText(panel, label='Начальный IP:')
        self.start_text = wx.TextCtrl(panel)
        if self.config.has_option('DEFAULT', 'start_ip'):
            self.start_text.SetValue(self.config['DEFAULT']['start_ip'])

        # Конечный IP
        self.end_label = wx.StaticText(panel, label='Конечный IP:')
        self.end_text = wx.TextCtrl(panel)
        if self.config.has_option('DEFAULT', 'end_ip'):
            self.end_text.SetValue(self.config['DEFAULT']['end_ip'])

        # Сервер TFTP
        self.tftp_server_label = wx.StaticText(panel, label='Сервер TFTP:')
        self.tftp_server_text = wx.TextCtrl(panel)
        if self.config.has_option('DEFAULT', 'tftp_server'):
            self.tftp_server_text.SetValue(self.config['DEFAULT']['tftp_server'])

        # Имя пользователя
        self.username_label = wx.StaticText(panel, label='Имя пользователя:')
        self.username_text = wx.TextCtrl(panel)
        if self.config.has_option('DEFAULT', 'username'):
            self.username_text.SetValue(self.config['DEFAULT']['username'])

        # Пароль
        self.password_label = wx.StaticText(panel, label='Пароль:')
        self.password_text = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        if self.config.has_option('DEFAULT', 'password'):
            self.password_text.SetValue(self.config['DEFAULT']['password'])

        # Тип устройства
        self.device_type_label = wx.StaticText(panel, label='Тип устройства:')
        self.device_type_text = wx.TextCtrl(panel)
        if self.config.has_option('DEFAULT', 'device_type'):
            self.device_type_text.SetValue(self.config['DEFAULT']['device_type'])

        # Кнопки
        self.save_button = wx.Button(panel, label='Сохранить настройки')
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)

        self.start_button = wx.Button(panel, label='Запустить')
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start)

        # Компоновщик элементов
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.start_label, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.start_text, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.end_label, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.end_text, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.tftp_server_label, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.tftp_server_text, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.username_label, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.username_text, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.password_label, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.password_text, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.device_type_label, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.device_type_text, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.save_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.start_button, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(sizer)
        self.SetSize((350, 480))  # Увеличенный размер окна для размещения кнопок

    def on_save(self, event):
        """Сохраняем текущие значения в файл."""
        self.config['DEFAULT'] = {}
        self.config['DEFAULT']['start_ip'] = self.start_text.GetValue()
        self.config['DEFAULT']['end_ip'] = self.end_text.GetValue()
        self.config['DEFAULT']['tftp_server'] = self.tftp_server_text.GetValue()
        self.config['DEFAULT']['username'] = self.username_text.GetValue()
        self.config['DEFAULT']['password'] = self.password_text.GetValue()
        self.config['DEFAULT']['device_type'] = self.device_type_text.GetValue()

        with open(CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)

        wx.MessageBox("Настройки успешно сохранены!", "Успех", wx.OK | wx.ICON_INFORMATION)

    def on_start(self, event):
        start_ip = self.start_text.GetValue()
        end_ip = self.end_text.GetValue()
        tftp_server = self.tftp_server_text.GetValue()
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()
        device_type = self.device_type_text.GetValue()

        if self.validate_ip(start_ip) and self.validate_ip(end_ip) and tftp_server and username and password and device_type:
            threading.Thread(target=main, args=(start_ip, end_ip, tftp_server, username, password, device_type)).start()
        else:
            wx.MessageBox('Пожалуйста, заполните все поля корректными данными!', 'Ошибка', wx.OK | wx.ICON_ERROR)

    def validate_ip(self, ip):
        parts = ip.split('.')
        return len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)


def generate_switches(start_ip, end_ip):
    start = int(start_ip.split('.')[-1])
    end = int(end_ip.split('.')[-1])
    base = ".".join(start_ip.split('.')[:-1])
    return [f"{base}.{i}" for i in range(start, end + 1)]


def main(start_ip, end_ip, tftp_server, username, password, device_type):
    switches = generate_switches(start_ip, end_ip)
    successful_count = 0
    for switch_ip in switches:
        success = False
        error_message = ""
        current_date = datetime.datetime.now().strftime("%Y_%m_%d")

        try:
            device_info = {
                'device_type': device_type,
                'host': switch_ip,
                'username': username,
                'password': password,
            }

            connection = ConnectHandler(**device_info)

            # Первая попытка: без dest_file
            command = f'upload cfg_toTFTP {tftp_server} bkp_{device_type}_{switch_ip}_{current_date}.cfg'
            output = connection.send_command(command)
            success = True
            logging.info(f"Свитч: {switch_ip}, успешно выполнен без dest_file.")

        except Exception as e:
            error_message = f"Свитч: {switch_ip}, Ошибка без dest_file: {e}"
            logging.error(error_message)

            # Вторая попытка: с dest_file
            if not success:
                try:
                    command = f'upload cfg_toTFTP {tftp_server} dest_file bkp_{device_type}_{switch_ip}_{current_date}.cfg'
                    output = connection.send_command(command)
                    success = True
                    logging.info(f"Свитч: {switch_ip}, успешно выполнен с dest_file.")
                    successful_count += 1

                except Exception as e:
                    error_message += f"\nТакже возникла ошибка с dest_file: {e}"
                    logging.error(error_message)

    wx.MessageBox(f"Обработка завершена! Всего успешно обработано "
                  f"{successful_count} свитчей.", "Завершение работы",
                  wx.OK | wx.ICON_INFORMATION)


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
