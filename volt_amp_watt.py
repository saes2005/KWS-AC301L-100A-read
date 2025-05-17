# 请先安装 pymodbus 和 pyserial
# pip install pymodbus
# pip install pyserial
 
log_path = 'D:\\MODBUS_VOLTAGE\\'
log_file = log_path + 'result.log'
test_times = 30  # test point count
step = 0.5   # test step 

# from pymodbus.client.sync import ModbusSerialClient as ModbusClient   # 报错，说找不到 sync
from pymodbus.client import ModbusSerialClient as ModbusClient
#from pymodbus.transaction import ModbusRtuFramer
from pymodbus.exceptions import ModbusException, ConnectionException
import logging
import time
from datetime import datetime

# 配置日志记录
logging.basicConfig()
log = logging.getLogger( )
log.setLevel(logging.INFO)
#log = logging.StreamHandler(open(log_path, 'w'))


## create a log file handler
file_handler = logging.FileHandler(log_file)
## bind to a logger
log.addHandler(file_handler)

# 初始化Modbus串行客户端
# client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, timeout=3)    # [Errno 2] could not open port /dev/ttyUSB0: [Errno 2] No such file or directory: '/dev/ttyUSB0'
# client = ModbusClient(method='rtu', port='/dev/ttyTHS1', baudrate=9600, timeout=3)
# ttyTHS4 ttyS0 ttyS1 ttyS2 ttyS4
# client = ModbusClient(method='rtu', port='/dev/ttyTHS1', baudrate=9600, timeout=3)
# client = ModbusClient(method='rtu', port='/dev/ttyTHS0', baudrate=9600, timeout=3, stopbits=1, bytesize=8, parity='N')
client = ModbusClient(port='COM6', baudrate=9600, timeout=3,
                      stopbits=1, bytesize=8, parity='N' )    # 看文档，method='rtu'貌似没用
 
 

def read_voltage(client):
    try:
        # 读取寄存器地址0和1上的4个字节（两个寄存器）
        # result = client.read_input_registers(address=0, count=3, unit=1)  # 这个错了，这是读取输入寄存器的）0x04
        # result = client.read_holding_registers(address=0, count=3, unit=1)  # 这个才是读取输入寄存器的0x03  # unit参数错了，当前pymodbus版本没有这个参数，搞乌龙了，要不是用filelocator搜索函数用法，还真不知道- -
        #time.sleep(3)
        result = client.read_holding_registers(
            address=14, count=1, slave=2 )  #READ 0X0E ADDRESS
        
        if result.isError():
            # 处理错误
            print("读取错误:", result)
            return None
 
        # ADDRESS 0X0E 
        registers = result.registers
        #print(registers)
        #voltage_reg_0 = registers[]
        #voltage_reg_1 = registers[4]
        voltage = registers[0] #0X0E RESULT
 

        #time.sleep(3)
        # 计算实际的電壓
        voltage = voltage * 0.1
        #print (voltage)
 
        # 格式化電壓
        voltage = round(voltage, 1)
        
 
        #return voltage
        return voltage 
    except ModbusException as e:
        print("Modbus异常:", e)
        return None
    except Exception as e:
        # 捕获除ModbusException之外的所有异常
        print(f"An error occurred: {e}")
        return None

def read_current(client):
    try:
        # 读取寄存器地址0和1上的4个字节（两个寄存器）
        # result = client.read_input_registers(address=0, count=3, unit=1)  # 这个错了，这是读取输入寄存器的）0x04
        # result = client.read_holding_registers(address=0, count=3, unit=1)  # 这个才是读取输入寄存器的0x03  # unit参数错了，当前pymodbus版本没有这个参数，搞乌龙了，要不是用filelocator搜索函数用法，还真不知道- -
        #time.sleep(3)
        result = client.read_holding_registers(
            address=15, count=1, slave=2 )  #READ 0X0F ADDRESS
        
        if result.isError():
            # 处理错误
            print("读取错误:", result)
            return None
 
        # ADDRESS 0X0F 
        registers = result.registers
        #print(registers)
        #voltage_reg_0 = registers[]
        #voltage_reg_1 = registers[4]
        current = registers[0] #0X0F RESULT
 

        #time.sleep(3)
        # 计算实际的電流
        current = current * 0.001
        #print (voltage)
 
        # 格式化電壓
        current = round(current, 3)
        
 
        #return voltage
        return current 
    except ModbusException as e:
        print("Modbus异常:", e)
        return None
    except Exception as e:
        # 捕获除ModbusException之外的所有异常
        print(f"An error occurred: {e}")
        return None

def read_watts(client):
    try:
        # 读取寄存器地址0和1上的4个字节（两个寄存器）
        # result = client.read_input_registers(address=0, count=3, unit=1)  # 这个错了，这是读取输入寄存器的）0x04
        # result = client.read_holding_registers(address=0, count=3, unit=1)  # 这个才是读取输入寄存器的0x03  # unit参数错了，当前pymodbus版本没有这个参数，搞乌龙了，要不是用filelocator搜索函数用法，还真不知道- -
        #time.sleep(3)
        result = client.read_holding_registers(
            address=17, count=1, slave=2 )  #READ 0X11 ADDRESS
        
        if result.isError():
            # 处理错误
            print("读取错误:", result)
            return None
 
        # ADDRESS 0X11 
        registers = result.registers
        #print(registers)
        #voltage_reg_0 = registers[]
        #voltage_reg_1 = registers[4]
        watts = registers[0] #0X11 RESULT
 

        #time.sleep(3)
        # 计算实际的電流
        watts = watts * 0.1
        #print (voltage)
 
        # 格式化電流
        watts = round(watts,1 )
        
 
        #return voltage
        return watts 
    except ModbusException as e:
        print("Modbus异常:", e)
        return None
    except Exception as e:
        # 捕获除ModbusException之外的所有异常
        print(f"An error occurred: {e}")
        return None
    
def main():
    try:
        
        now = datetime.now() # current date and time
        current_time = now.strftime("%Y_%m_%d_%H_%M_%S")
        output_file =  log_path + 'result_' + current_time + '.csv'

        #print("Hello World")
        result_file = open (output_file,'w')
        print("year,month,day,time,AC Voltage (V),AC Current (A),Watts (W)" , file=result_file)
        print("year,month,day,time,AC Voltage (V),AC Current (A),Watts (W)" )

        if client.connect():  # 尝试连接到Modbus服务器/设备
            cnt = 0  #loop count
            while cnt < test_times:   
                now = datetime.now() # current date and time
                current_time = now.strftime("%Y,%m,%d,%H:%M:%S")
                #print("Current Time:" , current_time)
                volt = read_voltage(client)
                #print(volt)
                if volt is not None:
                        #print(volt)
                        #print(f"電壓 : {volt} V")
                        client.close()  # 关闭连接
                else:
                        print("无法连接到Modbus设备")
                current = read_current(client)

                if current is not None:
                        #print(volt)
                        #print(f"電流 : {current} A")
                        client.close()  # 关闭连接
                else:
                        print("无法连接到Modbus设备")

                watts = read_watts(client)

                if watts is not None:
                        #print(volt)
                        #print(f"功率 : {watts} W")
                        client.close()  # 关闭连接
                else:
                        print("无法连接到Modbus设备")
                print(f'{current_time},{volt},{current},{watts}' , file=result_file )
                print(f'{current_time},{volt},{current},{watts}' )
                time.sleep(step)
                cnt=cnt+1 ;

        result_file.close()

    except ConnectionException as e:
        print("连接异常:", e)
 
 
if __name__ == "__main__":
    main()