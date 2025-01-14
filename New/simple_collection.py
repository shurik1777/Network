from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import datetime
import logging

# Настройка логирования
logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                    format='%(asctime)s - %(message)s')

# Информация о свитче
switch_ip = "192.168.11.111"
username = "rt"
password = "gfhjkmyfcdbnx"
model = "DES3200"  # замените на вашу модель
TFTP = "192.168.10.253"  # замените на ваш сервер

# Данные для подключения
device_info = {
    'device_type': 'dlink_ds_ssh',
    'host': switch_ip,
    'username': username,
    'password': password,
}

# Устанавливаем соединение
try:
    connection = ConnectHandler(**device_info)
    print(f"Успешно подключено к {switch_ip}")

    # Получаем текущую дату
    current_date = datetime.datetime.now().strftime("%Y_%m_%d")

    # Формируем команды
    command1 = f'upload cfg_toTFTP {TFTP} dest_file bkp_{model}_{switch_ip}_{current_date}.cfg'
    command2 = f'upload cfg_toTFTP {TFTP} bkp_{model}_{switch_ip}_{current_date}.cfg'

    # Попробуем выполнить первую команду
    try:
        output = connection.send_command(command1)
        print(f"Выполнена команда: {command1}")
        print(f"Вывод команды:\n{output}")
    except Exception as e:
        print(f"Ошибка при выполнении первой команды: {e}")

        # Если первая команда не удалась, пробуем выполнить вторую
        try:
            output = connection.send_command(command2)
            print(f"Выполнена команда: {command2}")
            print(f"Вывод команды:\n{output}")
        except Exception as e:
            print(f"Ошибка при выполнении второй команды: {e}")
            logging.error(f"Ошибка при выполнении команд для {switch_ip}: {e}")

except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
    logging.error(f"Не удалось подключиться к {switch_ip}: {e}")
    print(f"Ошибка подключения к {switch_ip}: {e}")

# Закрываем соединение если оно было успешно установлено
if 'connection' in locals() and connection:
    connection.disconnect()
    print(f"Соединение с {switch_ip} закрыто.")
