import time
from machine import Pin, reset, UART

class UARTAckError(Exception):
	pass
class ConfigError(Exception):
	pass

#to replace zfill
def int_fw(i, w):
	s = str(i)
	while len(s) < w:
		s = "0" + s
	return s

class UART_DROK_200220(object):
	def __init__(self, uart_number, pin_tx, pin_rx, rw_delay, retry_count):
		self.work_ok = True
		self.rw_delay = rw_delay
		self.retry_count = retry_count
		self.uart_obj = UART(uart_number, baudrate=9600, bits=8, parity=None, stop=1, tx=pin_tx, rx=pin_rx)
	def send_write_command(self, command):
		ack_received = False
		current_attempt = 0
		while ack_received == False and current_attempt < self.retry_count:
			self.uart_obj.write(bytes(":" + command + "\x0d\x0a", "utf-8"))
			time.sleep(self.rw_delay)
			current_attempt += 1
			received_ack = self.uart_obj.read()
			if received_ack == bytes("#" + command[:2] + "ok\r\n", "utf-8"):
				ack_received = True
		if ack_received == False:
			raise UARTAckError
		else:
			return True
	def send_read_command(self, command):
		ack_received = False
		data_received = None
		current_attempt = 0
		while ack_received == False and current_attempt < self.retry_count:
			self.uart_obj.write(bytes(":" + command + "\x0d\x0a", "utf-8"))
			time.sleep(self.rw_delay)
			current_attempt += 1
			received_ack = self.uart_obj.read()
			if len(received_ack) == 16 and type(received_ack) == bytes:
				if received_ack[:3] == bytes("#" + command[:2], "utf-8") and received_ack[-2:] == bytes("\x0d\x0a", "utf-8"):
					data_received = int(str(received_ack[3:-2])[2:-1])
					ack_received = True
					return data_received
		if ack_received == False:
			raise UARTAckError
	def write_and_verify(self, verify_value, command_write, command_read):
		verified = False
		current_attempt = 0
		while verified == False and current_attempt < self.retry_count:
			self.send_write_command(command_write)
			tv = self.send_read_command(command_read)
			verified = (verify_value == tv)
			current_attempt += 1
		if verified == False:
			raise UARTAckError
		return verified
	def write_output_voltage(self, voltage):
		return self.write_and_verify(voltage, "wu"+int_fw(voltage, 4), "rv")
	def write_output_current(self, current):
		return self.write_and_verify(current, "wi"+int_fw(current, 4), "ra")
	def write_output_status(self, status):
		return self.write_and_verify(int(status), "wo"+int_fw(int(status), 1), "ro")
	def read_actual_output_voltage(self):
		return self.send_read_command("ru")
	def read_actual_output_current(self):
		return self.send_read_command("ri")
	def read_setpoint_output_voltage(self):
		return self.send_read_command("rv")
	def read_setpoint_output_current(self):
		return self.send_read_command("ra")
	def read_working_time(self):
		return self.send_read_command("rt")
	def read_output_capacity(self):
		return self.send_read_command("rc")
	def read_output_status(self):
		return self.send_read_command("ro")
