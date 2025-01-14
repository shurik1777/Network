from netmiko import ConnectHandler
import datetime

# Информация о свитче
switch_ip = "192.168.10.15"
username = "rt"
password = "gfhjkmyfcdbnx"
model = "some_model"  # замените на вашу модель

# Данные для подключения
device_info = {
    'device_type': 'dlink_ds_ssh',
    'host': switch_ip,
    'username': username,
    'password': password,
}

# Установка соединения
connection = ConnectHandler(**device_info)

# Получаем текущую дату
current_date = datetime.datetime.now().strftime("%Y_%m_%d")

# Формируем команду
command = f'upload cfg_toTFTP 192.168.10.253 bkp_{model}_{switch_ip}_{current_date}.cfg'

# Отправляем команду
output = connection.send_command(command)

print(f"Выполнена команда: {command}")
print(f"Вывод команды:\n{output}")

# Закрываем соединение
connection.disconnect()