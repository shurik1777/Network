import wx  # Импорт библиотеки wxPython для создания графического интерфейса
import threading
from netmiko import ConnectHandler
import datetime
import logging

logging.basicConfig(filename='log_2.txt', level=logging.ERROR,
                    format='%(asctime)s %(clientip) %(levelname)s: %(message)s',
                    encoding='UTF-8',)

username = "rt"
password = "gfhjkmyfcdbnx"
model = "DES3200"  # замените на вашу модель


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Введите диапазон IP-адресов')
        panel = wx.Panel(self)

        self.start_label = wx.StaticText(panel, label='Начальный IP:')
        self.start_text = wx.TextCtrl(panel)

        self.end_label = wx.StaticText(panel, label='Конечный IP:')
        self.end_text = wx.TextCtrl(panel)

        self.start_button = wx.Button(panel, label='Запустить')
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.start_label, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.start_text, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.end_label, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.end_text, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.start_button, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(sizer)
        self.SetSize((300, 200))

    def on_start(self, event):
        start_ip = self.start_text.GetValue()
        end_ip = self.end_text.GetValue()

        if self.validate_ip(start_ip) and self.validate_ip(end_ip):
            threading.Thread(target=main, args=(start_ip, end_ip)).start()
        else:
            wx.MessageBox('Пожалуйста, введите корректные IP-адреса!', 'Ошибка', wx.OK | wx.ICON_ERROR)


    def validate_ip(self, ip):
        parts = ip.split('.')
        return len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)


def generate_switches(start_ip, end_ip):
    start = int(start_ip.split('.')[-1])
    end = int(end_ip.split('.')[-1])
    base = ".".join(start_ip.split('.')[:-1])
    return [f"{base}.{i}" for i in range(start, end + 1)]


def main(start_ip, end_ip):
    switches = generate_switches(start_ip, end_ip)
    for switch_ip in switches:
        success = False
        error_message = ""
        current_date = datetime.datetime.now().strftime("%Y_%m_%d")

        try:
            device_info = {
                'device_type': 'dlink_ds_ssh',
                'host': switch_ip,
                'username': username,
                'password': password,
            }

            connection = ConnectHandler(**device_info)

            # Первая попытка: без dest_file
            command = f'upload cfg_toTFTP 192.168.10.253 bkp_{model}_{switch_ip}_{current_date}.cfg'
            output = connection.send_command(command)
            success = True
            logging.info(f"Свитч: {switch_ip}, успешно выполнен без dest_file.")

        except Exception as e:
            error_message = f"Свитч: {switch_ip}, Ошибка без dest_file: {e}"
            logging.error(error_message)

            # Вторая попытка: с dest_file
            if not success:
                try:
                    command = f'upload cfg_toTFTP 192.168.10.253 dest_file bkp_{model}_{switch_ip}_{current_date}.cfg'
                    output = connection.send_command(command)
                    success = True
                    logging.info(f"Свитч: {switch_ip}, успешно выполнен с dest_file.")

                except Exception as e:
                    error_message += f"\nТакже возникла ошибка с dest_file: {e}"
                    logging.error(error_message)

                finally:
                    if not success:
                        logging.error(f"Свитч: {switch_ip}, обе попытки завершились с ошибкой: {error_message}")
                        dlg = wx.MessageDialog(None, 'Все сделано!', 'Информация', wx.OK | wx.ICON_INFORMATION)
                        dlg.ShowModal()
                        dlg.Destroy()

                    connection.disconnect()


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
