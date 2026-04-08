import smbus2
import struct
import time

I2C_BUS = 7
IMU_ADDR = 0x6A

WHO_AM_I = 0x0F
CTRL1_XL = 0x10
CTRL2_G = 0x11
CTRL3_C = 0x12

OUTX_L_G = 0x22
OUTX_L_XL = 0x28


class ISM330DLC:
    def init(self, bus=I2C_BUS, address=IMU_ADDR):
        self.bus = smbus2.SMBus(bus)
        self.address = address
        self._verify_who_am_i()
        self._configure()

    def _verify_who_am_i(self):
        chip_id = self.bus.read_byte_data(self.address, WHO_AM_I)
        if chip_id != 0x6B:
            raise RuntimeError(
                f"WHO_AM_I mismatch: expected 0x6B, got 0x{chip_id:02X}. Check wiring and I2C address."
            )

    def _configure(self):
        ctrl3 = self.bus.read_byte_data(self.address, CTRL3_C)
        self.bus.write_byte_data(self.address, CTRL3_C, ctrl3 | 0x44)
        self.bus.write_byte_data(self.address, CTRL1_XL, 0x40)
        self.bus.write_byte_data(self.address, CTRL2_G, 0x40)
        time.sleep(0.1)

    def _read_raw_xyz(self, start_reg):
        data = self.bus.read_i2c_block_data(self.address, start_reg, 6)
        x, y, z = struct.unpack("<hhh", bytes(data))
        return x, y, z

    def read_accel_raw(self):
        return self._read_raw_xyz(OUTX_L_XL)

    def read_gyro_raw(self):
        return self._read_raw_xyz(OUTX_L_G)

    def read_accel_mps2(self):
        ax, ay, az = self.read_accel_raw()
        scale_mps2_per_lsb = 0.061e-3 * 9.80665
        return (
            ax * scale_mps2_per_lsb,
            ay * scale_mps2_per_lsb,
            az * scale_mps2_per_lsb,
        )

    def read_gyro_radps(self):
        gx, gy, gz = self.read_gyro_raw()
        scale_radps_per_lsb = 8.75e-3 * 3.141592653589793 / 180.0
        return (
            gx * scale_radps_per_lsb,
            gy * scale_radps_per_lsb,
            gz * scale_radps_per_lsb,
        )

    def close(self):
        self.bus.close()
