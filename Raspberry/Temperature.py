import subprocess
import datetime


def get_cpu_temp():
    result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
    temp_str = result.stdout.strip().split('=')[1]
    return float(temp_str.strip("'C"))


def get_cpu_temp_sys():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp = int(f.read().strip()) / 1000
    return temp


def check_temperature(threshold=80):
    temp = get_cpu_temp_sys()
    print(f"Temperature CPU: {temp} C")
    
    if temp > threshold:
        print(f"Error: Temperature CPU >= {threshold} C!")

    return temp


def write_to_file(value, filename='output.txt'):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    line = f"{value} - {current_time}\n"
   
    with open(filename, 'a') as file:
        file.write(line)


def clear_file(filename):
    with open(filename, 'w') as file:
        file.truncate(0)


if __name__ == '__main__':
    check_temperature(75)