from netmiko import ConnectHandler
import datetime
import logging

# Настройка логгера
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Информация о свитчах
switches = ["192.168.10." + str(i) for i in range(60, 252)]
username = "rt"
password = "gfhjkmyfcdbnx"
model = "DES3200"  # замените на вашу модель


def main():
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

            connection.disconnect()


if __name__ == "__main__":
    main()
