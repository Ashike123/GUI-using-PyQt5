import pyvisa
import sys
import time

class XC9283_84:
   def __init__(self):
      rm = pyvisa.ResourceManager()
      reslist = rm.list_resources("USB?::?*::INSTR")
      if len(reslist) == 0:
         sys.exit()
      self.board = rm.open_resource(reslist[0])

   def set_led(self, led_status):
      self.board.write('a'+led_status)

   def TME(self):
      self.board.write_raw(b'\x0A')
      time.sleep(0.1)

   def reg_write(self, addr, data):
      payload = bytes([1, addr, data])
      # payload.append(b'\x01')
      # payload.append(addr.tobytes(1, "little"))
      # payload.append(data.tobytes(1, "little"))
      # self.board.write_raw(b'\x01\x07\xB8')
      # self.board.write_raw(payload)
      self.board.write_raw(b'\x01')
      # self.board.write_raw(b'\x07')
      # self.board.write_raw(b'\xB8')
      time.sleep(0.1)

   def reg_read(self,addr):
      payload = bytes([2, addr])
      self.board.write_raw(payload)
      time.sleep(0.1)
      return(self.board.read_bytes(1))

   def test_mode_exit(self):
      self.board.write_raw(b'\x01\x10\x01')
      time.sleep(0.1)