"""Serial AT-command client for a LoRa-E5 compatible module."""
import time
import serial

class LoRaError(RuntimeError):
    pass

class LoRaClient:
    def __init__(self, port, baudrate=9600, timeout=2.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def _command(self, command, wait_seconds=1.5):
        with serial.Serial(self.port, self.baudrate, timeout=self.timeout,
                           write_timeout=self.timeout) as ser:
            ser.reset_input_buffer()
            ser.write((command + "\r\n").encode("ascii"))
            ser.flush()
            time.sleep(wait_seconds)
            return ser.read_all().decode(errors="replace").strip()

    def get_id(self):
        return self._command("AT+ID")

    def network_status(self):
        return self._command("AT+NJS")

    def join(self):
        status = self.network_status()
        low = status.lower()
        if "+njs: 1" in low or "joined already" in low:
            return status
        response = self._command("AT+JOIN", wait_seconds=10.0)
        low = response.lower()
        if not any(x in low for x in ("joined already", "network joined", "+join: done", "+join: joined")):
            raise LoRaError(f"LoRaWAN join failed: {response or '<no response>'}")
        return response

    def send_hex(self, payload):
        response = self._command(f'AT+MSGHEX="{payload.hex().upper()}"', wait_seconds=6.0)
        if "done" not in response.lower():
            raise LoRaError(f"LoRaWAN transmission did not confirm success: {response or '<no response>'}")
        return response
