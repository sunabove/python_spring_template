import math
import ctypes
import time
import smbus
import csv

from math import sqrt

#from MPUConstants import MPUConstants as C
#from quat import Quaternion as Q
#from quat import XYZVector as V

from scipy.spatial.transform import Rotation as R 

class Quaternion:
    w = 0.0
    x = 0.0
    y = 0.0
    z = 0.0

    def __init__(self, a_w=1.0, a_x=0.0, a_y=0.0, a_z=0.0):
        self.w = a_w
        self.x = a_x
        self.y = a_y
        self.z = a_z

    def get_product(self, a_quat):
        result = Quaternion(
            self.w * a_quat.w - self.x * a_quat.x -
            self.y * a_quat.y - self.z * a_quat.z,

            self.w * a_quat.x + self.x * a_quat.w +
            self.y * a_quat.z - self.z * a_quat.y,

            self.w * a_quat.y - self.x * a_quat.z +
            self.y * a_quat.w + self.z * a_quat.x,

            self.w * a_quat.z + self.x * a_quat.y -
            self.y * a_quat.x + self.z * a_quat.w)
        return result

    def get_conjugate(self):
        result = Quaternion(self.w, -self.x, -self.y, -self.z)
        return result

    def get_magnitude(self):
        return sqrt(self.w * self.w + self.x * self.x + self.y * self.y +
                    self.z * self.z)

    def normalize(self):
        m = self.get_magnitude()
        self.w = self.w / m
        self.x = self.x / m
        self.y = self.y / m
        self.z = self.z / m

    def get_normalized(self):
        result = Quaternion(self.w, self.x, self.y, self.z)
        result.normalize()
        return result
    pass
pass # Quaternion

Q = Quaternion 

class XYZVector:
    x = 0.0
    y = 0.0
    z = 0.0

    def __init__(self, a_x=0.0, a_y=0.0, a_z=0.0):
        self.x = a_x
        self.y = a_y
        self.z = a_z

    def get_magnitude(self):
        return sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def normalize(self):
        m = self.get_magnitude()
        self.x = self.x / m
        self.y = self.y / m
        self.z = self.z / m

    def get_normalized(self):
        result = XYZVector(self.x, self.y, self.z)
        result.normalize()
        return result

    def rotate(self, a_quat):
        p = Quaternion(0.0, self.x, self.y, self.z)
        p = a_quat.get_product(p)
        p = p.get_product(a_quat.get_conjugate())
        # By magic quaternion p is now [0, x', y', z']
        self.x = p.x
        self.y = p.y
        self.z = p.z

    def get_rotated(self, a_quat):
        r = XYZVector(self.x, self.y, self.z)
        r.rotate(a_quat)
        return r
    pass
pass # XYZVector

V = XYZVector 

class MPUConstants : 
    MPU6050_ADDRESS_AD0_LOW = 0x68  # address pin low (GND), default
    MPU6050_ADDRESS_AD0_HIGH = 0x69  # address pin high (VCC)
    MPU6050_DEFAULT_ADDRESS = MPU6050_ADDRESS_AD0_LOW

    # [7] PWR_MODE, [6:1] XG_OFFS_TC, [0] OTP_BNK_VLD
    MPU6050_RA_XG_OFFS_TC = 0x00
    # [7] PWR_MODE, [6:1] YG_OFFS_TC, [0] OTP_BNK_VLD
    MPU6050_RA_YG_OFFS_TC = 0x01
    # [7] PWR_MODE, [6:1] ZG_OFFS_TC, [0] OTP_BNK_VLD
    MPU6050_RA_ZG_OFFS_TC = 0x02
    # [7:0] X_FINE_GAIN
    MPU6050_RA_X_FINE_GAIN = 0x03
    # [7:0] Y_FINE_GAIN
    MPU6050_RA_Y_FINE_GAIN = 0x04
    # [7:0] Z_FINE_GAIN
    MPU6050_RA_Z_FINE_GAIN = 0x05
    # [15:0] XA_OFFS
    MPU6050_RA_XA_OFFS_H = 0x06
    MPU6050_RA_XA_OFFS_L_TC = 0x07
    # [15:0] YA_OFFS
    MPU6050_RA_YA_OFFS_H = 0x08
    MPU6050_RA_YA_OFFS_L_TC = 0x09
    # [15:0] ZA_OFFS
    MPU6050_RA_ZA_OFFS_H = 0x0A
    MPU6050_RA_ZA_OFFS_L_TC = 0x0B
    # [15:0] XG_OFFS_USR
    MPU6050_RA_XG_OFFS_USRH = 0x13
    MPU6050_RA_XG_OFFS_USRL = 0x14
    # [15:0] YG_OFFS_USR
    MPU6050_RA_YG_OFFS_USRH = 0x15
    MPU6050_RA_YG_OFFS_USRL = 0x16
    # [15:0] ZG_OFFS_USR
    MPU6050_RA_ZG_OFFS_USRH = 0x17
    MPU6050_RA_ZG_OFFS_USRL = 0x18
    MPU6050_RA_SMPLRT_DIV = 0x19
    MPU6050_RA_CONFIG = 0x1A
    MPU6050_RA_GYRO_CONFIG = 0x1B
    MPU6050_RA_ACCEL_CONFIG = 0x1C
    MPU6050_RA_FF_THR = 0x1D
    MPU6050_RA_FF_DUR = 0x1E
    MPU6050_RA_MOT_THR = 0x1F
    MPU6050_RA_MOT_DUR = 0x20
    MPU6050_RA_ZRMOT_THR = 0x21
    MPU6050_RA_ZRMOT_DUR = 0x22
    MPU6050_RA_FIFO_EN = 0x23
    MPU6050_RA_I2C_MST_CTRL = 0x24
    MPU6050_RA_I2C_SLV0_ADDR = 0x25
    MPU6050_RA_I2C_SLV0_REG = 0x26
    MPU6050_RA_I2C_SLV0_CTRL = 0x27
    MPU6050_RA_I2C_SLV1_ADDR = 0x28
    MPU6050_RA_I2C_SLV1_REG = 0x29
    MPU6050_RA_I2C_SLV1_CTRL = 0x2A
    MPU6050_RA_I2C_SLV2_ADDR = 0x2B
    MPU6050_RA_I2C_SLV2_REG = 0x2C
    MPU6050_RA_I2C_SLV2_CTRL = 0x2D
    MPU6050_RA_I2C_SLV3_ADDR = 0x2E
    MPU6050_RA_I2C_SLV3_REG = 0x2F
    MPU6050_RA_I2C_SLV3_CTRL = 0x30
    MPU6050_RA_I2C_SLV4_ADDR = 0x31
    MPU6050_RA_I2C_SLV4_REG = 0x32
    MPU6050_RA_I2C_SLV4_DO = 0x33
    MPU6050_RA_I2C_SLV4_CTRL = 0x34
    MPU6050_RA_I2C_SLV4_DI = 0x35
    MPU6050_RA_I2C_MST_STATUS = 0x36
    MPU6050_RA_INT_PIN_CFG = 0x37
    MPU6050_RA_INT_ENABLE = 0x38
    MPU6050_RA_DMP_INT_STATUS = 0x39
    MPU6050_RA_INT_STATUS = 0x3A
    MPU6050_RA_ACCEL_XOUT_H = 0x3B
    MPU6050_RA_ACCEL_XOUT_L = 0x3C
    MPU6050_RA_ACCEL_YOUT_H = 0x3D
    MPU6050_RA_ACCEL_YOUT_L = 0x3E
    MPU6050_RA_ACCEL_ZOUT_H = 0x3F
    MPU6050_RA_ACCEL_ZOUT_L = 0x40
    MPU6050_RA_TEMP_OUT_H = 0x41
    MPU6050_RA_TEMP_OUT_L = 0x42
    MPU6050_RA_GYRO_XOUT_H = 0x43
    MPU6050_RA_GYRO_XOUT_L = 0x44
    MPU6050_RA_GYRO_YOUT_H = 0x45
    MPU6050_RA_GYRO_YOUT_L = 0x46
    MPU6050_RA_GYRO_ZOUT_H = 0x47
    MPU6050_RA_GYRO_ZOUT_L = 0x48
    MPU6050_RA_EXT_SENS_DATA_00 = 0x49
    MPU6050_RA_EXT_SENS_DATA_01 = 0x4A
    MPU6050_RA_EXT_SENS_DATA_02 = 0x4B
    MPU6050_RA_EXT_SENS_DATA_03 = 0x4C
    MPU6050_RA_EXT_SENS_DATA_04 = 0x4D
    MPU6050_RA_EXT_SENS_DATA_05 = 0x4E
    MPU6050_RA_EXT_SENS_DATA_06 = 0x4F
    MPU6050_RA_EXT_SENS_DATA_07 = 0x50
    MPU6050_RA_EXT_SENS_DATA_08 = 0x51
    MPU6050_RA_EXT_SENS_DATA_09 = 0x52
    MPU6050_RA_EXT_SENS_DATA_10 = 0x53
    MPU6050_RA_EXT_SENS_DATA_11 = 0x54
    MPU6050_RA_EXT_SENS_DATA_12 = 0x55
    MPU6050_RA_EXT_SENS_DATA_13 = 0x56
    MPU6050_RA_EXT_SENS_DATA_14 = 0x57
    MPU6050_RA_EXT_SENS_DATA_15 = 0x58
    MPU6050_RA_EXT_SENS_DATA_16 = 0x59
    MPU6050_RA_EXT_SENS_DATA_17 = 0x5A
    MPU6050_RA_EXT_SENS_DATA_18 = 0x5B
    MPU6050_RA_EXT_SENS_DATA_19 = 0x5C
    MPU6050_RA_EXT_SENS_DATA_20 = 0x5D
    MPU6050_RA_EXT_SENS_DATA_21 = 0x5E
    MPU6050_RA_EXT_SENS_DATA_22 = 0x5F
    MPU6050_RA_EXT_SENS_DATA_23 = 0x60
    MPU6050_RA_MOT_DETECT_STATUS = 0x61
    MPU6050_RA_I2C_SLV0_DO = 0x63
    MPU6050_RA_I2C_SLV1_DO = 0x64
    MPU6050_RA_I2C_SLV2_DO = 0x65
    MPU6050_RA_I2C_SLV3_DO = 0x66
    MPU6050_RA_I2C_MST_DELAY_CTRL = 0x67
    MPU6050_RA_SIGNAL_PATH_RESET = 0x68
    MPU6050_RA_MOT_DETECT_CTRL = 0x69
    MPU6050_RA_USER_CTRL = 0x6A
    MPU6050_RA_PWR_MGMT_1 = 0x6B
    MPU6050_RA_PWR_MGMT_2 = 0x6C
    MPU6050_RA_BANK_SEL = 0x6D
    MPU6050_RA_MEM_START_ADDR = 0x6E
    MPU6050_RA_MEM_R_W = 0x6F
    MPU6050_RA_DMP_CFG_1 = 0x70
    MPU6050_RA_DMP_CFG_2 = 0x71
    MPU6050_RA_FIFO_COUNTH = 0x72
    MPU6050_RA_FIFO_COUNTL = 0x73
    MPU6050_RA_FIFO_R_W = 0x74
    MPU6050_RA_WHO_AM_I = 0x75

    MPU6050_TC_PWR_MODE_BIT = 7
    MPU6050_TC_OFFSET_BIT = 6
    MPU6050_TC_OFFSET_LENGTH = 6
    MPU6050_TC_OTP_BNK_VLD_BIT = 0

    MPU6050_VDDIO_LEVEL_VLOGIC = 0
    MPU6050_VDDIO_LEVEL_VDD = 1

    MPU6050_CFG_EXT_SYNC_SET_BIT = 5
    MPU6050_CFG_EXT_SYNC_SET_LENGTH = 3
    MPU6050_CFG_DLPF_CFG_BIT = 2
    MPU6050_CFG_DLPF_CFG_LENGTH = 3

    MPU6050_EXT_SYNC_DISABLED = 0x0
    MPU6050_EXT_SYNC_TEMP_OUT_L = 0x1
    MPU6050_EXT_SYNC_GYRO_XOUT_L = 0x2
    MPU6050_EXT_SYNC_GYRO_YOUT_L = 0x3
    MPU6050_EXT_SYNC_GYRO_ZOUT_L = 0x4
    MPU6050_EXT_SYNC_ACCEL_XOUT_L = 0x5
    MPU6050_EXT_SYNC_ACCEL_YOUT_L = 0x6
    MPU6050_EXT_SYNC_ACCEL_ZOUT_L = 0x7

    MPU6050_DLPF_BW_256 = 0x00
    MPU6050_DLPF_BW_188 = 0x01
    MPU6050_DLPF_BW_98 = 0x02
    MPU6050_DLPF_BW_42 = 0x03
    MPU6050_DLPF_BW_20 = 0x04
    MPU6050_DLPF_BW_10 = 0x05
    MPU6050_DLPF_BW_5 = 0x06

    MPU6050_GCONFIG_FS_SEL_BIT = 4
    MPU6050_GCONFIG_FS_SEL_LENGTH = 2

    MPU6050_GYRO_FS_250 = 0x00
    MPU6050_GYRO_FS_500 = 0x01
    MPU6050_GYRO_FS_1000 = 0x02
    MPU6050_GYRO_FS_2000 = 0x03

    MPU6050_ACONFIG_XA_ST_BIT = 7
    MPU6050_ACONFIG_YA_ST_BIT = 6
    MPU6050_ACONFIG_ZA_ST_BIT = 5
    MPU6050_ACONFIG_AFS_SEL_BIT = 4
    MPU6050_ACONFIG_AFS_SEL_LENGTH = 2
    MPU6050_ACONFIG_ACCEL_HPF_BIT = 2
    MPU6050_ACONFIG_ACCEL_HPF_LENGTH = 3

    MPU6050_ACCEL_FS_2 = 0x00
    MPU6050_ACCEL_FS_4 = 0x01
    MPU6050_ACCEL_FS_8 = 0x02
    MPU6050_ACCEL_FS_16 = 0x03

    MPU6050_DHPF_RESET = 0x00
    MPU6050_DHPF_5 = 0x01
    MPU6050_DHPF_2P5 = 0x02
    MPU6050_DHPF_1P25 = 0x03
    MPU6050_DHPF_0P63 = 0x04
    MPU6050_DHPF_HOLD = 0x07

    MPU6050_TEMP_FIFO_EN_BIT = 7
    MPU6050_XG_FIFO_EN_BIT = 6
    MPU6050_YG_FIFO_EN_BIT = 5
    MPU6050_ZG_FIFO_EN_BIT = 4
    MPU6050_ACCEL_FIFO_EN_BIT = 3
    MPU6050_SLV2_FIFO_EN_BIT = 2
    MPU6050_SLV1_FIFO_EN_BIT = 1
    MPU6050_SLV0_FIFO_EN_BIT = 0

    MPU6050_MULT_MST_EN_BIT = 7
    MPU6050_WAIT_FOR_ES_BIT = 6
    MPU6050_SLV_3_FIFO_EN_BIT = 5
    MPU6050_I2C_MST_P_NSR_BIT = 4
    MPU6050_I2C_MST_CLK_BIT = 3
    MPU6050_I2C_MST_CLK_LENGTH = 4

    MPU6050_CLOCK_DIV_348 = 0x0
    MPU6050_CLOCK_DIV_333 = 0x1
    MPU6050_CLOCK_DIV_320 = 0x2
    MPU6050_CLOCK_DIV_308 = 0x3
    MPU6050_CLOCK_DIV_296 = 0x4
    MPU6050_CLOCK_DIV_286 = 0x5
    MPU6050_CLOCK_DIV_276 = 0x6
    MPU6050_CLOCK_DIV_267 = 0x7
    MPU6050_CLOCK_DIV_258 = 0x8
    MPU6050_CLOCK_DIV_500 = 0x9
    MPU6050_CLOCK_DIV_471 = 0xA
    MPU6050_CLOCK_DIV_444 = 0xB
    MPU6050_CLOCK_DIV_421 = 0xC
    MPU6050_CLOCK_DIV_400 = 0xD
    MPU6050_CLOCK_DIV_381 = 0xE
    MPU6050_CLOCK_DIV_364 = 0xF

    MPU6050_I2C_SLV_RW_BIT = 7
    MPU6050_I2C_SLV_ADDR_BIT = 6
    MPU6050_I2C_SLV_ADDR_LENGTH = 7
    MPU6050_I2C_SLV_EN_BIT = 7
    MPU6050_I2C_SLV_BYTE_SW_BIT = 6
    MPU6050_I2C_SLV_REG_DIS_BIT = 5
    MPU6050_I2C_SLV_GRP_BIT = 4
    MPU6050_I2C_SLV_LEN_BIT = 3
    MPU6050_I2C_SLV_LEN_LENGTH = 4

    MPU6050_I2C_SLV4_RW_BIT = 7
    MPU6050_I2C_SLV4_ADDR_BIT = 6
    MPU6050_I2C_SLV4_ADDR_LENGTH = 7
    MPU6050_I2C_SLV4_EN_BIT = 7
    MPU6050_I2C_SLV4_INT_EN_BIT = 6
    MPU6050_I2C_SLV4_REG_DIS_BIT = 5
    MPU6050_I2C_SLV4_MST_DLY_BIT = 4
    MPU6050_I2C_SLV4_MST_DLY_LENGTH = 5

    MPU6050_MST_PASS_THROUGH_BIT = 7
    MPU6050_MST_I2C_SLV4_DONE_BIT = 6
    MPU6050_MST_I2C_LOST_ARB_BIT = 5
    MPU6050_MST_I2C_SLV4_NACK_BIT = 4
    MPU6050_MST_I2C_SLV3_NACK_BIT = 3
    MPU6050_MST_I2C_SLV2_NACK_BIT = 2
    MPU6050_MST_I2C_SLV1_NACK_BIT = 1
    MPU6050_MST_I2C_SLV0_NACK_BIT = 0

    MPU6050_INTCFG_INT_LEVEL_BIT = 7
    MPU6050_INTCFG_INT_OPEN_BIT = 6
    MPU6050_INTCFG_LATCH_INT_EN_BIT = 5
    MPU6050_INTCFG_INT_RD_CLEAR_BIT = 4
    MPU6050_INTCFG_FSYNC_INT_LEVEL_BIT = 3
    MPU6050_INTCFG_FSYNC_INT_EN_BIT = 2
    MPU6050_INTCFG_I2C_BYPASS_EN_BIT = 1
    MPU6050_INTCFG_CLKOUT_EN_BIT = 0

    MPU6050_INTMODE_ACTIVEHIGH = 0x00
    MPU6050_INTMODE_ACTIVELOW = 0x01

    MPU6050_INTDRV_PUSHPULL = 0x00
    MPU6050_INTDRV_OPENDRAIN = 0x01

    MPU6050_INTLATCH_50USPULSE = 0x00
    MPU6050_INTLATCH_WAITCLEAR = 0x01

    MPU6050_INTCLEAR_STATUSREAD = 0x00
    MPU6050_INTCLEAR_ANYREAD = 0x01

    MPU6050_INTERRUPT_FF_BIT = 7
    MPU6050_INTERRUPT_MOT_BIT = 6
    MPU6050_INTERRUPT_ZMOT_BIT = 5
    MPU6050_INTERRUPT_FIFO_OFLOW_BIT = 4
    MPU6050_INTERRUPT_I2C_MST_INT_BIT = 3
    MPU6050_INTERRUPT_PLL_RDY_INT_BIT = 2
    MPU6050_INTERRUPT_DMP_INT_BIT = 1
    MPU6050_INTERRUPT_DATA_RDY_BIT = 0

    # TODO: figure out what these actually do
    # UMPL source code is not very obivous
    MPU6050_DMPINT_5_BIT = 5
    MPU6050_DMPINT_4_BIT = 4
    MPU6050_DMPINT_3_BIT = 3
    MPU6050_DMPINT_2_BIT = 2
    MPU6050_DMPINT_1_BIT = 1
    MPU6050_DMPINT_0_BIT = 0

    MPU6050_MOTION_MOT_XNEG_BIT = 7
    MPU6050_MOTION_MOT_XPOS_BIT = 6
    MPU6050_MOTION_MOT_YNEG_BIT = 5
    MPU6050_MOTION_MOT_YPOS_BIT = 4
    MPU6050_MOTION_MOT_ZNEG_BIT = 3
    MPU6050_MOTION_MOT_ZPOS_BIT = 2
    MPU6050_MOTION_MOT_ZRMOT_BIT = 0

    MPU6050_DELAYCTRL_DELAY_ES_SHADOW_BIT = 7
    MPU6050_DELAYCTRL_I2C_SLV4_DLY_EN_BIT = 4
    MPU6050_DELAYCTRL_I2C_SLV3_DLY_EN_BIT = 3
    MPU6050_DELAYCTRL_I2C_SLV2_DLY_EN_BIT = 2
    MPU6050_DELAYCTRL_I2C_SLV1_DLY_EN_BIT = 1
    MPU6050_DELAYCTRL_I2C_SLV0_DLY_EN_BIT = 0

    MPU6050_PATHRESET_GYRO_RESET_BIT = 2
    MPU6050_PATHRESET_ACCEL_RESET_BIT = 1
    MPU6050_PATHRESET_TEMP_RESET_BIT = 0

    MPU6050_DETECT_ACCEL_ON_DELAY_BIT = 5
    MPU6050_DETECT_ACCEL_ON_DELAY_LENGTH = 2
    MPU6050_DETECT_FF_COUNT_BIT = 3
    MPU6050_DETECT_FF_COUNT_LENGTH = 2
    MPU6050_DETECT_MOT_COUNT_BIT = 1
    MPU6050_DETECT_MOT_COUNT_LENGTH = 2

    MPU6050_DETECT_DECREMENT_RESET = 0x0
    MPU6050_DETECT_DECREMENT_1 = 0x1
    MPU6050_DETECT_DECREMENT_2 = 0x2
    MPU6050_DETECT_DECREMENT_4 = 0x3

    MPU6050_USERCTRL_DMP_EN_BIT = 7
    MPU6050_USERCTRL_FIFO_EN_BIT = 6
    MPU6050_USERCTRL_I2C_MST_EN_BIT = 5
    MPU6050_USERCTRL_I2C_IF_DIS_BIT = 4
    MPU6050_USERCTRL_DMP_RESET_BIT = 3
    MPU6050_USERCTRL_FIFO_RESET_BIT = 2
    MPU6050_USERCTRL_I2C_MST_RESET_BIT = 1
    MPU6050_USERCTRL_SIG_COND_RESET_BIT = 0

    MPU6050_PWR1_DEVICE_RESET_BIT = 7
    MPU6050_PWR1_SLEEP_BIT = 6
    MPU6050_PWR1_CYCLE_BIT = 5
    MPU6050_PWR1_TEMP_DIS_BIT = 3
    MPU6050_PWR1_CLKSEL_BIT = 2
    MPU6050_PWR1_CLKSEL_LENGTH = 3

    MPU6050_CLOCK_INTERNAL = 0x00
    MPU6050_CLOCK_PLL_XGYRO = 0x01
    MPU6050_CLOCK_PLL_YGYRO = 0x02
    MPU6050_CLOCK_PLL_ZGYRO = 0x03
    MPU6050_CLOCK_PLL_EXT32K = 0x04
    MPU6050_CLOCK_PLL_EXT19M = 0x05
    MPU6050_CLOCK_KEEP_RESET = 0x07

    MPU6050_PWR2_LP_WAKE_CTRL_BIT = 7
    MPU6050_PWR2_LP_WAKE_CTRL_LENGTH = 2
    MPU6050_PWR2_STBY_XA_BIT = 5
    MPU6050_PWR2_STBY_YA_BIT = 4
    MPU6050_PWR2_STBY_ZA_BIT = 3
    MPU6050_PWR2_STBY_XG_BIT = 2
    MPU6050_PWR2_STBY_YG_BIT = 1
    MPU6050_PWR2_STBY_ZG_BIT = 0

    MPU6050_WAKE_FREQ_1P25 = 0x0
    MPU6050_WAKE_FREQ_2P5 = 0x1
    MPU6050_WAKE_FREQ_5 = 0x2
    MPU6050_WAKE_FREQ_10 = 0x3

    MPU6050_BANKSEL_PRFTCH_EN_BIT = 6
    MPU6050_BANKSEL_CFG_USER_BANK_BIT = 5
    MPU6050_BANKSEL_MEM_SEL_BIT = 4
    MPU6050_BANKSEL_MEM_SEL_LENGTH = 5

    MPU6050_WHO_AM_I_BIT = 6
    MPU6050_WHO_AM_I_LENGTH = 6

    MPU6050_DMP_MEMORY_BANKS = 8
    MPU6050_DMP_MEMORY_BANK_SIZE = 256
    MPU6050_DMP_MEMORY_CHUNK_SIZE = 16

    # From MPU6050_6Axis_MotionApps20.h
    MPU6050_DMP_CODE_SIZE = 1929  # dmpMemory[]
    MPU6050_DMP_CONFIG_SIZE = 192  # dmpConfig[]
    MPU6050_DMP_UPDATES_SIZE = 47  # dmpUpdates[]
    '''
     * ================================================================================================ *
     | Default MotionApps v2.0 42-byte FIFO packet structure:                                           |
     |                                                                                                  |
     | [QUAT W][      ][QUAT X][      ][QUAT Y][      ][QUAT Z][      ][GYRO X][      ][GYRO Y][      ] |
     |   0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  |
     |                                                                                                  |
     | [GYRO Z][      ][ACC X ][      ][ACC Y ][      ][ACC Z ][      ][      ]                         |
     |  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40  41                          |
     * ================================================================================================ *
     '''
    # dmpMemory has size MPU6050_DMP_CODE_SIZE = 1929
    dmpMemory = [
        # bank 0, 256 bytes
        0xFB, 0x00, 0x00, 0x3E, 0x00, 0x0B, 0x00, 0x36, 0x00, 0x01, 0x00, 0x02,
        0x00, 0x03, 0x00, 0x00,
        0x00, 0x65, 0x00, 0x54, 0xFF, 0xEF, 0x00, 0x00, 0xFA, 0x80, 0x00, 0x0B,
        0x12, 0x82, 0x00, 0x01,
        0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x28, 0x00, 0x00, 0xFF, 0xFF, 0x45, 0x81, 0xFF, 0xFF, 0xFA, 0x72,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x03, 0xE8, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x7F, 0xFF,
        0xFF, 0xFE, 0x80, 0x01,
        0x00, 0x1B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x3E, 0x03, 0x30, 0x40, 0x00, 0x00, 0x00, 0x02, 0xCA, 0xE3, 0x09,
        0x3E, 0x80, 0x00, 0x00,
        0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00,
        0x60, 0x00, 0x00, 0x00,
        0x41, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x0B, 0x2A, 0x00, 0x00, 0x16, 0x55,
        0x00, 0x00, 0x21, 0x82,
        0xFD, 0x87, 0x26, 0x50, 0xFD, 0x80, 0x00, 0x00, 0x00, 0x1F, 0x00, 0x00,
        0x00, 0x05, 0x80, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00,
        0x00, 0x03, 0x00, 0x00,
        0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x6F, 0x00, 0x02, 0x65, 0x32,
        0x00, 0x00, 0x5E, 0xC0,
        0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0xFB, 0x8C, 0x6F, 0x5D, 0xFD, 0x5D, 0x08, 0xD9, 0x00, 0x7C, 0x73, 0x3B,
        0x00, 0x6C, 0x12, 0xCC,
        0x32, 0x00, 0x13, 0x9D, 0x32, 0x00, 0xD0, 0xD6, 0x32, 0x00, 0x08, 0x00,
        0x40, 0x00, 0x01, 0xF4,
        0xFF, 0xE6, 0x80, 0x79, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0xD0, 0xD6,
        0x00, 0x00, 0x27, 0x10,

        # bank 1, 256 bytes
        0xFB, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00,
        0x01, 0x00, 0x00, 0x00,
        0x00, 0x00, 0xFA, 0x36, 0xFF, 0xBC, 0x30, 0x8E, 0x00, 0x05, 0xFB, 0xF0,
        0xFF, 0xD9, 0x5B, 0xC8,
        0xFF, 0xD0, 0x9A, 0xBE, 0x00, 0x00, 0x10, 0xA9, 0xFF, 0xF4, 0x1E, 0xB2,
        0x00, 0xCE, 0xBB, 0xF7,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x04, 0x00, 0x02, 0x00, 0x02,
        0x02, 0x00, 0x00, 0x0C,
        0xFF, 0xC2, 0x80, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0xCF, 0x80, 0x00,
        0x40, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x00,
        0x00, 0x00, 0x00, 0x14,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x03, 0x3F, 0x68, 0xB6, 0x79, 0x35, 0x28, 0xBC,
        0xC6, 0x7E, 0xD1, 0x6C,
        0x80, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0xB2, 0x6A,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xF0,
        0x00, 0x00, 0x00, 0x30,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x25, 0x4D, 0x00, 0x2F, 0x70, 0x6D, 0x00, 0x00, 0x05, 0xAE,
        0x00, 0x0C, 0x02, 0xD0,

        # bank 2, 256 bytes
        0x00, 0x00, 0x00, 0x00, 0x00, 0x65, 0x00, 0x54, 0xFF, 0xEF, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x01, 0x00, 0x00, 0x44, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x00,
        0x00, 0x00, 0x01, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x65, 0x00, 0x00, 0x00, 0x54, 0x00, 0x00,
        0xFF, 0xEF, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x1B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x40, 0x00, 0x00, 0x00,
        0x00, 0x1B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,

        # bank 3, 256 bytes
        0xD8, 0xDC, 0xBA, 0xA2, 0xF1, 0xDE, 0xB2, 0xB8, 0xB4, 0xA8, 0x81, 0x91,
        0xF7, 0x4A, 0x90, 0x7F,
        0x91, 0x6A, 0xF3, 0xF9, 0xDB, 0xA8, 0xF9, 0xB0, 0xBA, 0xA0, 0x80, 0xF2,
        0xCE, 0x81, 0xF3, 0xC2,
        0xF1, 0xC1, 0xF2, 0xC3, 0xF3, 0xCC, 0xA2, 0xB2, 0x80, 0xF1, 0xC6, 0xD8,
        0x80, 0xBA, 0xA7, 0xDF,
        0xDF, 0xDF, 0xF2, 0xA7, 0xC3, 0xCB, 0xC5, 0xB6, 0xF0, 0x87, 0xA2, 0x94,
        0x24, 0x48, 0x70, 0x3C,
        0x95, 0x40, 0x68, 0x34, 0x58, 0x9B, 0x78, 0xA2, 0xF1, 0x83, 0x92, 0x2D,
        0x55, 0x7D, 0xD8, 0xB1,
        0xB4, 0xB8, 0xA1, 0xD0, 0x91, 0x80, 0xF2, 0x70, 0xF3, 0x70, 0xF2, 0x7C,
        0x80, 0xA8, 0xF1, 0x01,
        0xB0, 0x98, 0x87, 0xD9, 0x43, 0xD8, 0x86, 0xC9, 0x88, 0xBA, 0xA1, 0xF2,
        0x0E, 0xB8, 0x97, 0x80,
        0xF1, 0xA9, 0xDF, 0xDF, 0xDF, 0xAA, 0xDF, 0xDF, 0xDF, 0xF2, 0xAA, 0xC5,
        0xCD, 0xC7, 0xA9, 0x0C,
        0xC9, 0x2C, 0x97, 0x97, 0x97, 0x97, 0xF1, 0xA9, 0x89, 0x26, 0x46, 0x66,
        0xB0, 0xB4, 0xBA, 0x80,
        0xAC, 0xDE, 0xF2, 0xCA, 0xF1, 0xB2, 0x8C, 0x02, 0xA9, 0xB6, 0x98, 0x00,
        0x89, 0x0E, 0x16, 0x1E,
        0xB8, 0xA9, 0xB4, 0x99, 0x2C, 0x54, 0x7C, 0xB0, 0x8A, 0xA8, 0x96, 0x36,
        0x56, 0x76, 0xF1, 0xB9,
        0xAF, 0xB4, 0xB0, 0x83, 0xC0, 0xB8, 0xA8, 0x97, 0x11, 0xB1, 0x8F, 0x98,
        0xB9, 0xAF, 0xF0, 0x24,
        0x08, 0x44, 0x10, 0x64, 0x18, 0xF1, 0xA3, 0x29, 0x55, 0x7D, 0xAF, 0x83,
        0xB5, 0x93, 0xAF, 0xF0,
        0x00, 0x28, 0x50, 0xF1, 0xA3, 0x86, 0x9F, 0x61, 0xA6, 0xDA, 0xDE, 0xDF,
        0xD9, 0xFA, 0xA3, 0x86,
        0x96, 0xDB, 0x31, 0xA6, 0xD9, 0xF8, 0xDF, 0xBA, 0xA6, 0x8F, 0xC2, 0xC5,
        0xC7, 0xB2, 0x8C, 0xC1,
        0xB8, 0xA2, 0xDF, 0xDF, 0xDF, 0xA3, 0xDF, 0xDF, 0xDF, 0xD8, 0xD8, 0xF1,
        0xB8, 0xA8, 0xB2, 0x86,

        # bank 4, 256 bytes
        0xB4, 0x98, 0x0D, 0x35, 0x5D, 0xB8, 0xAA, 0x98, 0xB0, 0x87, 0x2D, 0x35,
        0x3D, 0xB2, 0xB6, 0xBA,
        0xAF, 0x8C, 0x96, 0x19, 0x8F, 0x9F, 0xA7, 0x0E, 0x16, 0x1E, 0xB4, 0x9A,
        0xB8, 0xAA, 0x87, 0x2C,
        0x54, 0x7C, 0xB9, 0xA3, 0xDE, 0xDF, 0xDF, 0xA3, 0xB1, 0x80, 0xF2, 0xC4,
        0xCD, 0xC9, 0xF1, 0xB8,
        0xA9, 0xB4, 0x99, 0x83, 0x0D, 0x35, 0x5D, 0x89, 0xB9, 0xA3, 0x2D, 0x55,
        0x7D, 0xB5, 0x93, 0xA3,
        0x0E, 0x16, 0x1E, 0xA9, 0x2C, 0x54, 0x7C, 0xB8, 0xB4, 0xB0, 0xF1, 0x97,
        0x83, 0xA8, 0x11, 0x84,
        0xA5, 0x09, 0x98, 0xA3, 0x83, 0xF0, 0xDA, 0x24, 0x08, 0x44, 0x10, 0x64,
        0x18, 0xD8, 0xF1, 0xA5,
        0x29, 0x55, 0x7D, 0xA5, 0x85, 0x95, 0x02, 0x1A, 0x2E, 0x3A, 0x56, 0x5A,
        0x40, 0x48, 0xF9, 0xF3,
        0xA3, 0xD9, 0xF8, 0xF0, 0x98, 0x83, 0x24, 0x08, 0x44, 0x10, 0x64, 0x18,
        0x97, 0x82, 0xA8, 0xF1,
        0x11, 0xF0, 0x98, 0xA2, 0x24, 0x08, 0x44, 0x10, 0x64, 0x18, 0xDA, 0xF3,
        0xDE, 0xD8, 0x83, 0xA5,
        0x94, 0x01, 0xD9, 0xA3, 0x02, 0xF1, 0xA2, 0xC3, 0xC5, 0xC7, 0xD8, 0xF1,
        0x84, 0x92, 0xA2, 0x4D,
        0xDA, 0x2A, 0xD8, 0x48, 0x69, 0xD9, 0x2A, 0xD8, 0x68, 0x55, 0xDA, 0x32,
        0xD8, 0x50, 0x71, 0xD9,
        0x32, 0xD8, 0x70, 0x5D, 0xDA, 0x3A, 0xD8, 0x58, 0x79, 0xD9, 0x3A, 0xD8,
        0x78, 0x93, 0xA3, 0x4D,
        0xDA, 0x2A, 0xD8, 0x48, 0x69, 0xD9, 0x2A, 0xD8, 0x68, 0x55, 0xDA, 0x32,
        0xD8, 0x50, 0x71, 0xD9,
        0x32, 0xD8, 0x70, 0x5D, 0xDA, 0x3A, 0xD8, 0x58, 0x79, 0xD9, 0x3A, 0xD8,
        0x78, 0xA8, 0x8A, 0x9A,
        0xF0, 0x28, 0x50, 0x78, 0x9E, 0xF3, 0x88, 0x18, 0xF1, 0x9F, 0x1D, 0x98,
        0xA8, 0xD9, 0x08, 0xD8,
        0xC8, 0x9F, 0x12, 0x9E, 0xF3, 0x15, 0xA8, 0xDA, 0x12, 0x10, 0xD8, 0xF1,
        0xAF, 0xC8, 0x97, 0x87,

        # bank 5, 256 bytes
        0x34, 0xB5, 0xB9, 0x94, 0xA4, 0x21, 0xF3, 0xD9, 0x22, 0xD8, 0xF2, 0x2D,
        0xF3, 0xD9, 0x2A, 0xD8,
        0xF2, 0x35, 0xF3, 0xD9, 0x32, 0xD8, 0x81, 0xA4, 0x60, 0x60, 0x61, 0xD9,
        0x61, 0xD8, 0x6C, 0x68,
        0x69, 0xD9, 0x69, 0xD8, 0x74, 0x70, 0x71, 0xD9, 0x71, 0xD8, 0xB1, 0xA3,
        0x84, 0x19, 0x3D, 0x5D,
        0xA3, 0x83, 0x1A, 0x3E, 0x5E, 0x93, 0x10, 0x30, 0x81, 0x10, 0x11, 0xB8,
        0xB0, 0xAF, 0x8F, 0x94,
        0xF2, 0xDA, 0x3E, 0xD8, 0xB4, 0x9A, 0xA8, 0x87, 0x29, 0xDA, 0xF8, 0xD8,
        0x87, 0x9A, 0x35, 0xDA,
        0xF8, 0xD8, 0x87, 0x9A, 0x3D, 0xDA, 0xF8, 0xD8, 0xB1, 0xB9, 0xA4, 0x98,
        0x85, 0x02, 0x2E, 0x56,
        0xA5, 0x81, 0x00, 0x0C, 0x14, 0xA3, 0x97, 0xB0, 0x8A, 0xF1, 0x2D, 0xD9,
        0x28, 0xD8, 0x4D, 0xD9,
        0x48, 0xD8, 0x6D, 0xD9, 0x68, 0xD8, 0xB1, 0x84, 0x0D, 0xDA, 0x0E, 0xD8,
        0xA3, 0x29, 0x83, 0xDA,
        0x2C, 0x0E, 0xD8, 0xA3, 0x84, 0x49, 0x83, 0xDA, 0x2C, 0x4C, 0x0E, 0xD8,
        0xB8, 0xB0, 0xA8, 0x8A,
        0x9A, 0xF5, 0x20, 0xAA, 0xDA, 0xDF, 0xD8, 0xA8, 0x40, 0xAA, 0xD0, 0xDA,
        0xDE, 0xD8, 0xA8, 0x60,
        0xAA, 0xDA, 0xD0, 0xDF, 0xD8, 0xF1, 0x97, 0x86, 0xA8, 0x31, 0x9B, 0x06,
        0x99, 0x07, 0xAB, 0x97,
        0x28, 0x88, 0x9B, 0xF0, 0x0C, 0x20, 0x14, 0x40, 0xB8, 0xB0, 0xB4, 0xA8,
        0x8C, 0x9C, 0xF0, 0x04,
        0x28, 0x51, 0x79, 0x1D, 0x30, 0x14, 0x38, 0xB2, 0x82, 0xAB, 0xD0, 0x98,
        0x2C, 0x50, 0x50, 0x78,
        0x78, 0x9B, 0xF1, 0x1A, 0xB0, 0xF0, 0x8A, 0x9C, 0xA8, 0x29, 0x51, 0x79,
        0x8B, 0x29, 0x51, 0x79,
        0x8A, 0x24, 0x70, 0x59, 0x8B, 0x20, 0x58, 0x71, 0x8A, 0x44, 0x69, 0x38,
        0x8B, 0x39, 0x40, 0x68,
        0x8A, 0x64, 0x48, 0x31, 0x8B, 0x30, 0x49, 0x60, 0xA5, 0x88, 0x20, 0x09,
        0x71, 0x58, 0x44, 0x68,

        # bank 6, 256 bytes
        0x11, 0x39, 0x64, 0x49, 0x30, 0x19, 0xF1, 0xAC, 0x00, 0x2C, 0x54, 0x7C,
        0xF0, 0x8C, 0xA8, 0x04,
        0x28, 0x50, 0x78, 0xF1, 0x88, 0x97, 0x26, 0xA8, 0x59, 0x98, 0xAC, 0x8C,
        0x02, 0x26, 0x46, 0x66,
        0xF0, 0x89, 0x9C, 0xA8, 0x29, 0x51, 0x79, 0x24, 0x70, 0x59, 0x44, 0x69,
        0x38, 0x64, 0x48, 0x31,
        0xA9, 0x88, 0x09, 0x20, 0x59, 0x70, 0xAB, 0x11, 0x38, 0x40, 0x69, 0xA8,
        0x19, 0x31, 0x48, 0x60,
        0x8C, 0xA8, 0x3C, 0x41, 0x5C, 0x20, 0x7C, 0x00, 0xF1, 0x87, 0x98, 0x19,
        0x86, 0xA8, 0x6E, 0x76,
        0x7E, 0xA9, 0x99, 0x88, 0x2D, 0x55, 0x7D, 0x9E, 0xB9, 0xA3, 0x8A, 0x22,
        0x8A, 0x6E, 0x8A, 0x56,
        0x8A, 0x5E, 0x9F, 0xB1, 0x83, 0x06, 0x26, 0x46, 0x66, 0x0E, 0x2E, 0x4E,
        0x6E, 0x9D, 0xB8, 0xAD,
        0x00, 0x2C, 0x54, 0x7C, 0xF2, 0xB1, 0x8C, 0xB4, 0x99, 0xB9, 0xA3, 0x2D,
        0x55, 0x7D, 0x81, 0x91,
        0xAC, 0x38, 0xAD, 0x3A, 0xB5, 0x83, 0x91, 0xAC, 0x2D, 0xD9, 0x28, 0xD8,
        0x4D, 0xD9, 0x48, 0xD8,
        0x6D, 0xD9, 0x68, 0xD8, 0x8C, 0x9D, 0xAE, 0x29, 0xD9, 0x04, 0xAE, 0xD8,
        0x51, 0xD9, 0x04, 0xAE,
        0xD8, 0x79, 0xD9, 0x04, 0xD8, 0x81, 0xF3, 0x9D, 0xAD, 0x00, 0x8D, 0xAE,
        0x19, 0x81, 0xAD, 0xD9,
        0x01, 0xD8, 0xF2, 0xAE, 0xDA, 0x26, 0xD8, 0x8E, 0x91, 0x29, 0x83, 0xA7,
        0xD9, 0xAD, 0xAD, 0xAD,
        0xAD, 0xF3, 0x2A, 0xD8, 0xD8, 0xF1, 0xB0, 0xAC, 0x89, 0x91, 0x3E, 0x5E,
        0x76, 0xF3, 0xAC, 0x2E,
        0x2E, 0xF1, 0xB1, 0x8C, 0x5A, 0x9C, 0xAC, 0x2C, 0x28, 0x28, 0x28, 0x9C,
        0xAC, 0x30, 0x18, 0xA8,
        0x98, 0x81, 0x28, 0x34, 0x3C, 0x97, 0x24, 0xA7, 0x28, 0x34, 0x3C, 0x9C,
        0x24, 0xF2, 0xB0, 0x89,
        0xAC, 0x91, 0x2C, 0x4C, 0x6C, 0x8A, 0x9B, 0x2D, 0xD9, 0xD8, 0xD8, 0x51,
        0xD9, 0xD8, 0xD8, 0x79,

        # bank 7, 138 bytes (remainder)
        0xD9, 0xD8, 0xD8, 0xF1, 0x9E, 0x88, 0xA3, 0x31, 0xDA, 0xD8, 0xD8, 0x91,
        0x2D, 0xD9, 0x28, 0xD8,
        0x4D, 0xD9, 0x48, 0xD8, 0x6D, 0xD9, 0x68, 0xD8, 0xB1, 0x83, 0x93, 0x35,
        0x3D, 0x80, 0x25, 0xDA,
        0xD8, 0xD8, 0x85, 0x69, 0xDA, 0xD8, 0xD8, 0xB4, 0x93, 0x81, 0xA3, 0x28,
        0x34, 0x3C, 0xF3, 0xAB,
        0x8B, 0xF8, 0xA3, 0x91, 0xB6, 0x09, 0xB4, 0xD9, 0xAB, 0xDE, 0xFA, 0xB0,
        0x87, 0x9C, 0xB9, 0xA3,
        0xDD, 0xF1, 0xA3, 0xA3, 0xA3, 0xA3, 0x95, 0xF1, 0xA3, 0xA3, 0xA3, 0x9D,
        0xF1, 0xA3, 0xA3, 0xA3,
        0xA3, 0xF2, 0xA3, 0xB4, 0x90, 0x80, 0xF2, 0xA3, 0xA3, 0xA3, 0xA3, 0xA3,
        0xA3, 0xA3, 0xA3, 0xA3,
        0xA3, 0xB2, 0xA3, 0xA3, 0xA3, 0xA3, 0xA3, 0xA3, 0xB0, 0x87, 0xB5, 0x99,
        0xF1, 0xA3, 0xA3, 0xA3,
        0x98, 0xF1, 0xA3, 0xA3, 0xA3, 0xA3, 0x97, 0xA3, 0xA3, 0xA3, 0xA3, 0xF3,
        0x9B, 0xA3, 0xA3, 0xDC,
        0xB9, 0xA7, 0xF1, 0x26, 0x26, 0x26, 0xD8, 0xD8, 0xFF]

    # dmpConfig has size MPU6050_DMP_CONFIG_SIZE = 192
    dmpConfig = [
        #  BANK    OFFSET  LENGTH  [DATA]
        0x03, 0x7B, 0x03, 0x4C, 0xCD, 0x6C,  # FCFG_1 inv_set_gyro_calibration
        0x03, 0xAB, 0x03, 0x36, 0x56, 0x76,  # FCFG_3 inv_set_gyro_calibration
        0x00, 0x68, 0x04, 0x02, 0xCB, 0x47, 0xA2,
        # D_0_104 inv_set_gyro_calibration
        0x02, 0x18, 0x04, 0x00, 0x05, 0x8B, 0xC1,
        # D_0_24 inv_set_gyro_calibration
        0x01, 0x0C, 0x04, 0x00, 0x00, 0x00, 0x00,
        # D_1_152 inv_set_accel_calibration
        0x03, 0x7F, 0x06, 0x0C, 0xC9, 0x2C, 0x97, 0x97, 0x97,
        # FCFG_2 inv_set_accel_calibration
        0x03, 0x89, 0x03, 0x26, 0x46, 0x66,  # FCFG_7 inv_set_accel_calibration
        0x00, 0x6C, 0x02, 0x20, 0x00,  # D_0_108 inv_set_accel_calibration
        0x02, 0x40, 0x04, 0x00, 0x00, 0x00, 0x00,
        # CPASS_MTX_00 inv_set_compass_calibration
        0x02, 0x44, 0x04, 0x00, 0x00, 0x00, 0x00,  # CPASS_MTX_01
        0x02, 0x48, 0x04, 0x00, 0x00, 0x00, 0x00,  # CPASS_MTX_02
        0x02, 0x4C, 0x04, 0x00, 0x00, 0x00, 0x00,  # CPASS_MTX_10
        0x02, 0x50, 0x04, 0x00, 0x00, 0x00, 0x00,  # CPASS_MTX_11
        0x02, 0x54, 0x04, 0x00, 0x00, 0x00, 0x00,  # CPASS_MTX_12
        0x02, 0x58, 0x04, 0x00, 0x00, 0x00, 0x00,  # CPASS_MTX_20
        0x02, 0x5C, 0x04, 0x00, 0x00, 0x00, 0x00,  # CPASS_MTX_21
        0x02, 0xBC, 0x04, 0x00, 0x00, 0x00, 0x00,  # CPASS_MTX_22
        0x01, 0xEC, 0x04, 0x00, 0x00, 0x40, 0x00,
        # D_1_236 inv_apply_endian_accel
        0x03, 0x7F, 0x06, 0x0C, 0xC9, 0x2C, 0x97, 0x97, 0x97,
        # FCFG_2 inv_set_mpu_sensors
        0x04, 0x02, 0x03, 0x0D, 0x35, 0x5D,
        # CFG_MOTION_BIAS inv_turn_on_bias_from_no_motion
        0x04, 0x09, 0x04, 0x87, 0x2D, 0x35, 0x3D,  # FCFG_5 inv_set_bias_update
        0x00, 0xA3, 0x01, 0x00,  # D_0_163 inv_set_dead_zone
        # SPECIAL 0x01 = enable interrupts
        0x00, 0x00, 0x00, 0x01,  # SET INT_ENABLE at i=22, SPECIAL INSTRUCTION
        0x07, 0x86, 0x01, 0xFE,  # CFG_6 inv_set_fifo_interupt
        0x07, 0x41, 0x05, 0xF1, 0x20, 0x28, 0x30, 0x38,
        # CFG_8 inv_send_quaternion
        0x07, 0x7E, 0x01, 0x30,  # CFG_16 inv_set_footer
        0x07, 0x46, 0x01, 0x9A,  # CFG_GYRO_SOURCE inv_send_gyro
        0x07, 0x47, 0x04, 0xF1, 0x28, 0x30, 0x38,
        # CFG_9 inv_send_gyro -> inv_construct3_fifo
        0x07, 0x6C, 0x04, 0xF1, 0x28, 0x30, 0x38,
        # CFG_12 inv_send_accel -> inv_construct3_fifo
        0x02, 0x16, 0x02, 0x00, 0x09]  # D_0_22 inv_set_fifo_rate

    # This very last 0x04 WAS a 0x09, which drops the FIFO rate down to 20 Hz.
    # 0x07 is 25 Hz, 0x01 is 100Hz. Going faster than 100Hz (0x00=200Hz) tends
    # to result in very noisy data. DMP output frequency is calculated easily
    # using this equation: (200Hz / (1 + value))

    # It is important to make sure the host processor can keep up with reading
    # and processing the FIFO output at the desired rate. Handling FIFO overflow
    # cleanly is also a good idea.

    # dmpUpdates has size MPU6050_DMP_UPDATES_SIZE = 47
    dmpUpdates = [
        0x01, 0xB2, 0x02, 0xFF, 0xFF,
        0x01, 0x90, 0x04, 0x09, 0x23, 0xA1, 0x35,
        0x01, 0x6A, 0x02, 0x06, 0x00,
        0x01, 0x60, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x60, 0x04, 0x40, 0x00, 0x00, 0x00,
        0x01, 0x62, 0x02, 0x00, 0x00,
        0x00, 0x60, 0x04, 0x00, 0x40, 0x00, 0x00]
    pass

pass

C = MPUConstants 

class MPU6050:
    __buffer = [0] * 14
    __debug = False
    __DMP_packet_size = 0
    __dev_id = 0
    __bus = None

    ### the offsets are set to default numbers for the ease of use ###
    # The offsets are different for each device and should be changed
    # accordingly using a calibration procedure
    def __init__(self, a_bus=1, a_address=C.MPU6050_DEFAULT_ADDRESS, freq_divider=4,
                 a_xAOff=-5489, a_yAOff=-1441, a_zAOff=1305, a_xGOff=-2,
                 a_yGOff=-72, a_zGOff=-5, a_debug=False):

        ### Define the divider of the DMP frequency
        self.freq_divider = freq_divider
        ###

        self.__dev_id = a_address
        # Connect to num 1 SMBus
        self.__bus = smbus.SMBus(a_bus)
        # Set clock source to gyro
        self.set_clock_source(C.MPU6050_CLOCK_PLL_XGYRO)
        # Set accelerometer range
        self.set_full_scale_accel_range(C.MPU6050_ACCEL_FS_2)
        # Set gyro range
        self.set_full_scale_gyro_range(C.MPU6050_GYRO_FS_250)
        # Take the MPU out of time.sleep mode
        self.wake_up()
        # Set offsets
        if a_xAOff:
            self.set_x_accel_offset(a_xAOff)
        if a_yAOff:
            self.set_y_accel_offset(a_yAOff)
        if a_zAOff:
            self.set_z_accel_offset(a_zAOff)
        if a_xGOff:
            self.set_x_gyro_offset(a_xGOff)
        if a_yGOff:
            self.set_y_gyro_offset(a_yGOff)
        if a_zGOff:
            self.set_z_gyro_offset(a_zGOff)
        self.__debug = a_debug

    ###  ###
    def isreadyFIFO(self, packet_size):
        FIFO_count = self.get_FIFO_count()
        mpu_int_status = self.get_int_status()

        # If overflow is detected by status or fifo count we want to reset
        if (FIFO_count == 1024) or (mpu_int_status & 0x10):
            self.reset_FIFO()
            # print('overflow!')

            return 0
        # Check if fifo data is ready
        elif (mpu_int_status & 0x02):
            # Wait until packet_size number of bytes are ready for reading, default
            # is 42 bytes
            while FIFO_count < packet_size:
                FIFO_count = self.get_FIFO_count()

            return 1
        
        return 0

    # Core bit and byte operations
    def read_bit(self, a_reg_add, a_bit_position):
        return self.read_bits(a_reg_add, a_bit_position, 1)

    def write_bit(self, a_reg_add, a_bit_num, a_bit):
        byte = self.__bus.read_byte_data(self.__dev_id, a_reg_add)
        if a_bit:
            byte |= 1 << a_bit_num
        else:
            byte &= ~(1 << a_bit_num)
        self.__bus.write_byte_data(
            self.__dev_id, a_reg_add, ctypes.c_int8(byte).value)

    def read_bits(self, a_reg_add, a_bit_start, a_length):
        byte = self.__bus.read_byte_data(self.__dev_id, a_reg_add)
        mask = ((1 << a_length) - 1) << (a_bit_start - a_length + 1)
        byte &= mask
        byte >>= a_bit_start - a_length + 1
        return byte

    def write_bits(self, a_reg_add, a_bit_start, a_length, a_data):
        byte = self.__bus.read_byte_data(self.__dev_id, a_reg_add)
        mask = ((1 << a_length) - 1) << (a_bit_start - a_length + 1)
        # Get data in position and zero all non-important bits in data
        a_data <<= a_bit_start - a_length + 1
        a_data &= mask
        # Clear all important bits in read byte and combine with data
        byte &= ~mask
        byte = byte | a_data
        # Write the data to the I2C device
        self.__bus.write_byte_data(
            self.__dev_id, a_reg_add, ctypes.c_int8(byte).value)

    def read_memory_byte(self):
        return self.__bus.read_byte_data(self.__dev_id, C.MPU6050_RA_MEM_R_W)

    def read_bytes(self, a_data_list, a_address, a_length):
        if a_length > len(a_data_list):
            print('read_bytes, length of passed list too short')
            return a_data_list
        # Attempt to use the built in read bytes function in the adafruit lib
        # a_data_list = self.__bus.read_i2c_block_data(self.__dev_id, a_address,
        #                                             a_length)
        # Attempt to bypass adafruit lib
        #a_data_list = self.__mpu.bus.read_i2c_block_data(0x68, a_address, a_length)
        #print('data' + str(a_data_list))
        for x in range(0, a_length):
            a_data_list[x] = self.__bus.read_byte_data(self.__dev_id,
                                                       a_address + x)
        return a_data_list

    def write_memory_block(self, a_data_list, a_data_size, a_bank, a_address,
                           a_verify):
        success = True
        self.set_memory_bank(a_bank)
        self.set_memory_start_address(a_address)

        # For each a_data_item we want to write it to the board to a certain
        # memory bank and address
        for i in range(0, a_data_size):
            # Write each data to memory
            self.__bus.write_byte_data(self.__dev_id, C.MPU6050_RA_MEM_R_W,
                                       a_data_list[i])

            if a_verify:
                self.set_memory_bank(a_bank)
                self.set_memory_start_address(a_address)
                verify_data = self.__bus.read_byte_data(self.__dev_id,
                                                        C.MPU6050_RA_MEM_R_W)
                if verify_data != a_data_list[i]:
                    success = False

            # If we've filled the bank, change the memory bank
            if a_address == 255:
                a_address = 0
                a_bank += 1
                self.set_memory_bank(a_bank)
            else:
                a_address += 1

            # Either way update the memory address
            self.set_memory_start_address(a_address)

        return success

    def wake_up(self):
        self.write_bit(
            C.MPU6050_RA_PWR_MGMT_1, C.MPU6050_PWR1_SLEEP_BIT, 0)

    def set_clock_source(self, a_source):
        self.write_bits(C.MPU6050_RA_PWR_MGMT_1, C.MPU6050_PWR1_CLKSEL_BIT,
                        C.MPU6050_PWR1_CLKSEL_LENGTH, a_source)

    def set_full_scale_gyro_range(self, a_data):
        self.write_bits(C.MPU6050_RA_GYRO_CONFIG,
                        C.MPU6050_GCONFIG_FS_SEL_BIT,
                        C.MPU6050_GCONFIG_FS_SEL_LENGTH, a_data)

    def set_full_scale_accel_range(self, a_data):
        self.write_bits(C.MPU6050_RA_ACCEL_CONFIG,
                        C.MPU6050_ACONFIG_AFS_SEL_BIT,
                        C.MPU6050_ACONFIG_AFS_SEL_LENGTH, a_data)

    def reset(self):
        self.write_bit(C.MPU6050_RA_PWR_MGMT_1,
                       C.MPU6050_PWR1_DEVICE_RESET_BIT, 1)

    def set_sleep_enabled(self, a_enabled):
        set_bit = 0
        if a_enabled:
            set_bit = 1
        self.write_bit(C.MPU6050_RA_PWR_MGMT_1,
                       C.MPU6050_PWR1_SLEEP_BIT, set_bit)

    def set_memory_bank(self, a_bank, a_prefetch_enabled=False,
                        a_user_bank=False):
        a_bank &= 0x1F
        if a_user_bank:
            a_bank |= 0x20
        if a_prefetch_enabled:
            a_bank |= 0x20
        self.__bus.write_byte_data(
            self.__dev_id, C.MPU6050_RA_BANK_SEL, a_bank)

    def set_memory_start_address(self, a_address):
        self.__bus.write_byte_data(
            self.__dev_id, C.MPU6050_RA_MEM_START_ADDR, a_address)

    def get_x_gyro_offset_TC(self):
        return self.read_bits(C.MPU6050_RA_XG_OFFS_TC,
                              C.MPU6050_TC_OFFSET_BIT,
                              C.MPU6050_TC_OFFSET_LENGTH)

    def set_x_gyro_offset_TC(self, a_offset):
        self.write_bits(C.MPU6050_RA_XG_OFFS_TC,
                        C.MPU6050_TC_OFFSET_BIT,
                        C.MPU6050_TC_OFFSET_LENGTH, a_offset)

    def get_y_gyro_offset_TC(self):
        return self.read_bits(C.MPU6050_RA_YG_OFFS_TC,
                              C.MPU6050_TC_OFFSET_BIT,
                              C.MPU6050_TC_OFFSET_LENGTH)

    def set_y_gyro_offset_TC(self, a_offset):
        self.write_bits(C.MPU6050_RA_YG_OFFS_TC,
                        C.MPU6050_TC_OFFSET_BIT,
                        C.MPU6050_TC_OFFSET_LENGTH, a_offset)

    def get_z_gyro_offset_TC(self):
        return self.read_bits(C.MPU6050_RA_ZG_OFFS_TC,
                              C.MPU6050_TC_OFFSET_BIT,
                              C.MPU6050_TC_OFFSET_LENGTH)

    def set_z_gyro_offset_TC(self, a_offset):
        self.write_bits(C.MPU6050_RA_ZG_OFFS_TC,
                        C.MPU6050_TC_OFFSET_BIT,
                        C.MPU6050_TC_OFFSET_LENGTH, a_offset)

    def set_slave_address(self, a_num, a_address):
        self.__bus.write_byte_data(
            self.__dev_id, C.MPU6050_RA_I2C_SLV0_ADDR + a_num * 3, a_address)

    def set_I2C_master_mode_enabled(self, a_enabled):
        bit = 0
        if a_enabled:
            bit = 1
        self.write_bit(C.MPU6050_RA_USER_CTRL,
                       C.MPU6050_USERCTRL_I2C_MST_EN_BIT, bit)

    def reset_I2C_master(self):
        self.write_bit(C.MPU6050_RA_USER_CTRL,
                       C.MPU6050_USERCTRL_I2C_MST_RESET_BIT, 1)

    def write_prog_memory_block(self, a_data_list, a_data_size, a_bank=0,
                                a_address=0, a_verify=True):
        return self.write_memory_block(a_data_list, a_data_size, a_bank,
                                       a_address, a_verify)

    def write_DMP_configuration_set(self, a_data_list, a_data_size):
        index = 0
        while index < a_data_size:
            bank = a_data_list[index]
            offset = a_data_list[index + 1]
            length = a_data_list[index + 2]
            index += 3
            success = False

            # Normal case
            if length > 0:
                data_selection = list()
                for subindex in range(0, length):
                    data_selection.append(a_data_list[index + subindex])
                success = self.write_memory_block(data_selection, length, bank,
                                                  offset, True)
                index += length
            # Special undocumented case
            else:
                special = a_data_list[index]
                index += 1
                if special == 0x01:
                    # TODO Figure out if write8 can return True/False
                    success = self.__bus.write_byte_data(
                        self.__dev_id, C.MPU6050_RA_INT_ENABLE, 0x32)

            if success == False:
                # TODO implement error messagemajigger
                return False
                pass
        return True

    def write_prog_dmp_configuration(self, a_data_list, a_data_size):
        return self.write_DMP_configuration_set(a_data_list, a_data_size)

    def set_int_enable(self, a_enabled):
        self.__bus.write_byte_data(
            self.__dev_id, C.MPU6050_RA_INT_ENABLE, a_enabled)

    def set_rate(self, a_rate):
        self.__bus.write_byte_data(
            self.__dev_id, C.MPU6050_RA_SMPLRT_DIV, a_rate)

    def set_external_frame_sync(self, a_sync):
        self.write_bits(C.MPU6050_RA_CONFIG,
                        C.MPU6050_CFG_EXT_SYNC_SET_BIT,
                        C.MPU6050_CFG_EXT_SYNC_SET_LENGTH, a_sync)

    def set_DLF_mode(self, a_mode):
        self.write_bits(C.MPU6050_RA_CONFIG, C.MPU6050_CFG_DLPF_CFG_BIT,
                        C.MPU6050_CFG_DLPF_CFG_LENGTH, a_mode)

    def get_DMP_config_1(self):
        return self.__bus.read_byte_data(self.__dev_id, C.MPU6050_RA_DMP_CFG_1)

    def set_DMP_config_1(self, a_config):
        self.__bus.write_byte_data(
            self.__dev_id, C.MPU6050_RA_DMP_CFG_1, a_config)

    def get_DMP_config_2(self):
        return self.__bus.read_byte_data(self.__dev_id, C.MPU6050_RA_DMP_CFG_2)

    def set_DMP_config_2(self, a_config):
        self.__bus.write_byte_data(
            self.__dev_id, C.MPU6050_RA_DMP_CFG_2, a_config)

    def set_OTP_bank_valid(self, a_enabled):
        bit = 0
        if a_enabled:
            bit = 1
        self.write_bit(C.MPU6050_RA_XG_OFFS_TC,
                       C.MPU6050_TC_OTP_BNK_VLD_BIT, bit)

    def get_OTP_bank_valid(self):
        return self.read_bit(C.MPU6050_RA_XG_OFFS_TC,
                             C.MPU6050_TC_OTP_BNK_VLD_BIT)

    def set_motion_detection_threshold(self, a_threshold):
        self.__bus.write_byte_data(
            self.__dev_id, C.MPU6050_RA_MOT_THR, a_threshold)

    def set_zero_motion_detection_threshold(self, a_threshold):
        self.__bus.write_byte_data(
            self.__dev_id, C.MPU6050_RA_ZRMOT_THR, a_threshold)

    def set_motion_detection_duration(self, a_duration):
        self.__bus.write_byte_data(
            self.__dev_id, C.MPU6050_RA_MOT_DUR, a_duration)

    def set_zero_motion_detection_duration(self, a_duration):
        self.__bus.write_byte_data(
            self.__dev_id, C.MPU6050_RA_ZRMOT_DUR, a_duration)

    def set_FIFO_enabled(self, a_enabled):
        bit = 0
        if a_enabled:
            bit = 1
        self.write_bit(C.MPU6050_RA_USER_CTRL,
                       C.MPU6050_USERCTRL_FIFO_EN_BIT, bit)

    def set_DMP_enabled(self, a_enabled):
        bit = 0
        if a_enabled:
            bit = 1
        self.write_bit(C.MPU6050_RA_USER_CTRL,
                       C.MPU6050_USERCTRL_DMP_EN_BIT, bit)

    def reset_DMP(self):
        self.write_bit(C.MPU6050_RA_USER_CTRL,
                       C.MPU6050_USERCTRL_DMP_RESET_BIT, True)

    def dmp_initialize(self):
        # Reset the MPU
        self.reset()
        # time.Sleep a bit while resetting
        time.sleep(50 / 1000)
        # Disable time.sleep mode
        self.set_sleep_enabled(0)

        # get MPU hardware revision
        if self.__debug:
            print('Selecting user bank 16')
        self.set_memory_bank(0x10, True, True)

        if self.__debug:
            print('Selecting memory byte 6')
        self.set_memory_start_address(0x6)

        if self.__debug:
            print('Checking hardware revision')
        HW_revision = self.read_memory_byte()
        if self.__debug:
            print('Revision @ user[16][6] = ' + hex(HW_revision))

        if self.__debug:
            print('Resetting memory bank selection to 0')
        self.set_memory_bank(0)

        # check OTP bank valid
        # TODO Find out what OTP is
        OTP_valid = self.get_OTP_bank_valid()
        if self.__debug:
            if OTP_valid:
                print('OTP bank is valid')
            else:
                print('OTP bank is invalid')

        # get X/Y/Z gyro offsets
        if self.__debug:
            print('Reading gyro offet TC values')
        x_g_offset_TC = self.get_x_gyro_offset_TC()
        y_g_offset_TC = self.get_y_gyro_offset_TC()
        z_g_offset_TC = self.get_z_gyro_offset_TC()
        if self.__debug:
            print("X gyro offset = ", repr(x_g_offset_TC))
            print("Y gyro offset = ", repr(y_g_offset_TC))
            print("Z gyro offset = ", repr(z_g_offset_TC))

        # setup weird slave stuff (?)
        if self.__debug:
            print('Setting slave 0 address to 0x7F')
        self.set_slave_address(0, 0x7F)
        if self.__debug:
            print('Disabling I2C Master mode')
        self.set_I2C_master_mode_enabled(False)
        if self.__debug:
            print('Setting slave 0 address to 0x68 (self)')
        self.set_slave_address(0, 0x68)
        if self.__debug:
            print('Resetting I2C Master control')
        self.reset_I2C_master()
        # Wait a bit for the device to register the changes
        time.sleep(20 / 1000)

        # load DMP code into memory banks
        if self.__debug:
            print('Writing DMP code to MPU memory banks ' +
                  repr(C.MPU6050_DMP_CODE_SIZE) + ' bytes')
        if self.write_prog_memory_block(C.dmpMemory, C.MPU6050_DMP_CODE_SIZE):
            # TODO Check if we've actually verified this
            if self.__debug:
                print('Success! DMP code written and verified')

            # Write DMP configuration
            if self.__debug:
                print('Writing DMP configuration to MPU memory banks ' +
                      repr(C.MPU6050_DMP_CONFIG_SIZE) + ' bytes in config')
                
            ### Here we change the DMP configuration to set an arbitrary divider for DMP frequency
            dmp_config = C.dmpConfig # set an arbitrary divider
            dmp_config[-1] = self.freq_divider # Define the divider of the DMP frequency
            ###
            if self.write_prog_dmp_configuration(dmp_config,
                                                 C.MPU6050_DMP_CONFIG_SIZE):
                if self.__debug:
                    print('Success! DMP configuration written and verified.')
                    print('Setting clock source to Z gyro')
                self.set_clock_source(C.MPU6050_CLOCK_PLL_ZGYRO)

                if self.__debug:
                    print('Setting DMP and FIFO_OFLOW interrupts enabled')
                self.set_int_enable(0x12)

                if self.__debug:
                    print('Setting sample rate to 200Hz')
                self.set_rate(4)

                if self.__debug:
                    print('Setting external frame sync to TEMP_OUT_L[0]')
                self.set_external_frame_sync(C.MPU6050_EXT_SYNC_TEMP_OUT_L)

                if self.__debug:
                    print('Setting DLPF bandwidth to 42Hz')
                self.set_DLF_mode(C.MPU6050_DLPF_BW_42)

                if self.__debug:
                    print('Setting gyro sensitivity to +/- 2000 deg/sec')
                self.set_full_scale_gyro_range(C.MPU6050_GYRO_FS_2000)

                if self.__debug:
                    print('Setting DMP configuration bytes (function unknown)')
                self.set_DMP_config_1(0x03)
                self.set_DMP_config_2(0x00)

                if self.__debug:
                    print('Clearing OTP Bank flag')
                self.set_OTP_bank_valid(False)

                if self.__debug:
                    print('Setting X/Y/Z gyro offset TCs to previous values')
                self.set_x_gyro_offset_TC(x_g_offset_TC)
                self.set_y_gyro_offset_TC(y_g_offset_TC)
                self.set_z_gyro_offset_TC(z_g_offset_TC)

                # Uncomment this to zero offsets when dmp_initialize is called
                # if self.__debug:
                #    print('Setting X/Y/Z gyro user offsets to zero')
                # self.set_x_gyro_offset(0)
                # self.set_y_gyro_offset(0)
                # self.set_z_gyro_offset(0)

                if self.__debug:
                    print('Writing final memory update 1/7 (function unknown)')
                pos = 0
                j = 0
                dmp_update = [0] * 16
                while (j < 4) or (j < dmp_update[2] + 3):
                    dmp_update[j] = C.dmpUpdates[pos]
                    pos += 1
                    j += 1
                # Write as block from pos 3
                self.write_memory_block(dmp_update[3:], dmp_update[2],
                                        dmp_update[0], dmp_update[1], True)

                if self.__debug:
                    print('Writing final memory update 2/7 (function unknown)')
                j = 0
                while (j < 4) or (j < dmp_update[2] + 3):
                    dmp_update[j] = C.dmpUpdates[pos]
                    pos += 1
                    j += 1
                # Write as block from pos 3
                self.write_memory_block(dmp_update[3:], dmp_update[2],
                                        dmp_update[0], dmp_update[1], True)

                if self.__debug:
                    print('Resetting FIFO')
                self.reset_FIFO()

                if self.__debug:
                    print('Reading FIFO count')
                FIFO_count = self.get_FIFO_count()

                if self.__debug:
                    print('FIFO count: ' + repr(FIFO_count))

                if self.__debug:
                    print('Getting FIFO buffer')
                FIFO_buffer = [0] * 128
                FIFO_buffer = self.get_FIFO_bytes(FIFO_count)

                if self.__debug:
                    print('Setting motion detection threshold to 2')
                self.set_motion_detection_threshold(2)

                if self.__debug:
                    print('Setting zero-motion detection threshold to 156')
                self.set_zero_motion_detection_threshold(156)

                if self.__debug:
                    print('Setting motion detection duration to 80')
                self.set_motion_detection_duration(80)

                if self.__debug:
                    print('Setting zero-motion detection duration to 0')
                self.set_zero_motion_detection_duration(0)

                if self.__debug:
                    print('Resetting FIFO')
                self.reset_FIFO()

                if self.__debug:
                    print('Enabling FIFO')
                self.set_FIFO_enabled(True)

                if self.__debug:
                    print('Enabling DMP')
                self.set_DMP_enabled(True)

                if self.__debug:
                    print('Resetting DMP')
                self.reset_DMP()

                if self.__debug:
                    print('Writing final memory update 3/7 (function unknown)')
                j = 0
                while (j < 4) or (j < dmp_update[2] + 3):
                    dmp_update[j] = C.dmpUpdates[pos]
                    pos += 1
                    j += 1
                # Write as block from pos 3
                self.write_memory_block(dmp_update[3:], dmp_update[2],
                                        dmp_update[0], dmp_update[1], True)

                if self.__debug:
                    print('Writing final memory update 4/7 (function unknown)')
                j = 0
                while (j < 4) or (j < dmp_update[2] + 3):
                    dmp_update[j] = C.dmpUpdates[pos]
                    pos += 1
                    j += 1
                # Write as block from pos 3
                self.write_memory_block(dmp_update[3:], dmp_update[2],
                                        dmp_update[0], dmp_update[1], True)

                if self.__debug:
                    print('Writing final memory update 5/7 (function unknown)')
                j = 0
                while (j < 4) or (j < dmp_update[2] + 3):
                    dmp_update[j] = C.dmpUpdates[pos]
                    pos += 1
                    j += 1
                # Write as block from pos 3
                self.write_memory_block(dmp_update[3:], dmp_update[2],
                                        dmp_update[0], dmp_update[1], True)

                if self.__debug:
                    print('Waiting for FIFO count > 2')
                FIFO_count = self.get_FIFO_count()
                while FIFO_count < 3:
                    FIFO_count = self.get_FIFO_count()

                if self.__debug:
                    print('Current FIFO count = ' + repr(FIFO_count))
                    print('Reading FIFO data')
                FIFO_buffer = self.get_FIFO_bytes(FIFO_count)

                if self.__debug:
                    print('Reading interrupt status')
                MPU_int_status = self.get_int_status()

                if self.__debug:
                    print('Current interrupt status = ' + hex(MPU_int_status))
                    print('Writing final memory update 6/7 (function unknown)')
                j = 0
                while (j < 4) or (j < dmp_update[2] + 3):
                    dmp_update[j] = C.dmpUpdates[pos]
                    pos += 1
                    j += 1
                # Write as block from pos 3
                self.write_memory_block(dmp_update[3:], dmp_update[2],
                                        dmp_update[0], dmp_update[1], True)

                if self.__debug:
                    print('Waiting for FIFO count > 2')
                FIFO_count = self.get_FIFO_count()
                while FIFO_count < 3:
                    FIFO_count = self.get_FIFO_count()

                if self.__debug:
                    print('Current FIFO count = ' + repr(FIFO_count))
                    print('Reading FIFO count')
                FIFO_buffer = self.get_FIFO_bytes(FIFO_count)

                if self.__debug:
                    print('Reading interrupt status')
                MPU_int_status = self.get_int_status()

                if self.__debug:
                    print('Current interrupt status = ' + hex(MPU_int_status))
                    print('Writing final memory update 7/7 (function unknown)')
                j = 0
                while (j < 4) or (j < dmp_update[2] + 3):
                    dmp_update[j] = C.dmpUpdates[pos]
                    pos += 1
                    j += 1
                # Write as block from pos 3
                self.write_memory_block(dmp_update[3:], dmp_update[2],
                                        dmp_update[0], dmp_update[1], True)

                if self.__debug:
                    print('DMP is good to go! Finally.')
                    print('Disabling DMP (you turn it on later)')
                self.set_DMP_enabled(False)

                if self.__debug:
                    print('Setting up internal 42 byte DMP packet buffer')
                self.__DMP_packet_size = 42

                if self.__debug:
                    print(
                        'Resetting FIFO and clearing INT status one last time')
                self.reset_FIFO()
                self.get_int_status()

            else:
                if self.__debug:
                    print('Configuration block loading failed')
                return 2

        else:
            if self.__debug:
                print('Main binary block loading failed')
            return 1

        if self.__debug:
            print('DMP initialization was successful')
        return 0

    # Acceleration and gyro offset setters and getters
    def set_x_accel_offset(self, a_offset):
        self.__bus.write_byte_data(self.__dev_id, C.MPU6050_RA_XA_OFFS_H,
                                   ctypes.c_int8(a_offset >> 8).value)
        self.__bus.write_byte_data(self.__dev_id, C.MPU6050_RA_XA_OFFS_L_TC,
                                   ctypes.c_int8(a_offset).value)

    def set_y_accel_offset(self, a_offset):
        self.__bus.write_byte_data(self.__dev_id, C.MPU6050_RA_YA_OFFS_H,
                                   ctypes.c_int8(a_offset >> 8).value)
        self.__bus.write_byte_data(self.__dev_id, C.MPU6050_RA_YA_OFFS_L_TC,
                                   ctypes.c_int8(a_offset).value)

    def set_z_accel_offset(self, a_offset):
        self.__bus.write_byte_data(self.__dev_id, C.MPU6050_RA_ZA_OFFS_H,
                                   ctypes.c_int8(a_offset >> 8).value)
        self.__bus.write_byte_data(self.__dev_id, C.MPU6050_RA_ZA_OFFS_L_TC,
                                   ctypes.c_int8(a_offset).value)

    def set_x_gyro_offset(self, a_offset):
        self.__bus.write_byte_data(self.__dev_id, C.MPU6050_RA_XG_OFFS_USRH,
                                   ctypes.c_int8(a_offset >> 8).value)
        self.__bus.write_byte_data(self.__dev_id, C.MPU6050_RA_XG_OFFS_USRL,
                                   ctypes.c_int8(a_offset).value)

    def set_y_gyro_offset(self, a_offset):
        self.__bus.write_byte_data(self.__dev_id, C.MPU6050_RA_YG_OFFS_USRH,
                                   ctypes.c_int8(a_offset >> 8).value)
        self.__bus.write_byte_data(self.__dev_id, C.MPU6050_RA_YG_OFFS_USRL,
                                   ctypes.c_int8(a_offset).value)

    def set_z_gyro_offset(self, a_offset):
        self.__bus.write_byte_data(self.__dev_id, C.MPU6050_RA_ZG_OFFS_USRH,
                                   ctypes.c_int8(a_offset >> 8).value)
        self.__bus.write_byte_data(self.__dev_id, C.MPU6050_RA_ZG_OFFS_USRL,
                                   ctypes.c_int8(a_offset).value)

    # Main interfacing functions to get raw data from MPU
    def get_acceleration(self):
        raw_data = self.__bus.read_i2c_block_data(self.__dev_id,
                                                  C.MPU6050_RA_ACCEL_XOUT_H, 6)
        # accel = [0] * 3
        x = ctypes.c_int16(raw_data[0] << 8 | raw_data[1]).value
        y = ctypes.c_int16(raw_data[2] << 8 | raw_data[3]).value
        z = ctypes.c_int16(raw_data[4] << 8 | raw_data[5]).value
        return V(x,y,z)

    def get_rotation(self):
        raw_data = self.__bus.read_i2c_block_data(self.__dev_id,
                                                  C.MPU6050_RA_GYRO_XOUT_H, 6)
        # gyro = [0] * 3
        x = ctypes.c_int16(raw_data[0] << 8 | raw_data[1]).value
        y = ctypes.c_int16(raw_data[2] << 8 | raw_data[3]).value
        z = ctypes.c_int16(raw_data[4] << 8 | raw_data[5]).value
        return V(x,y,z)

    # Interfacing functions to get data from FIFO buffer
    def DMP_get_FIFO_packet_size(self):
        return self.__DMP_packet_size

    def reset_FIFO(self):
        self.write_bit(C.MPU6050_RA_USER_CTRL,
                       C.MPU6050_USERCTRL_FIFO_RESET_BIT, True)

    def get_FIFO_count(self):
        data = [0] * 2
        data = self.read_bytes(data, C.MPU6050_RA_FIFO_COUNTH, 2)
        return (data[0] << 8) | data[1]

    def get_FIFO_bytes(self, a_FIFO_count):
        return_list = list()
        for index in range(0, a_FIFO_count):
            return_list.append(
                self.__bus.read_byte_data(self.__dev_id,
                                          C.MPU6050_RA_FIFO_R_W))
        return return_list

    def get_int_status(self):
        return self.__bus.read_byte_data(self.__dev_id,
                                         C.MPU6050_RA_INT_STATUS)

    # Data retrieval from received FIFO buffer
    def DMP_get_quaternion_int16(self, a_FIFO_buffer):
        w = ctypes.c_int16((a_FIFO_buffer[0] << 8) | a_FIFO_buffer[1]).value
        x = ctypes.c_int16((a_FIFO_buffer[4] << 8) | a_FIFO_buffer[5]).value
        y = ctypes.c_int16((a_FIFO_buffer[8] << 8) | a_FIFO_buffer[9]).value
        z = ctypes.c_int16((a_FIFO_buffer[12] << 8) | a_FIFO_buffer[13]).value
        return Q(w, x, y, z)

    def DMP_get_quaternion(self, a_FIFO_buffer):
        quat = self.DMP_get_quaternion_int16(a_FIFO_buffer)
        w = quat.w / 16384.0
        x = quat.x / 16384.0
        y = quat.y / 16384.0
        z = quat.z / 16384.0
        return Q(w, x, y, z)

    def DMP_get_acceleration_int16(self, a_FIFO_buffer):
        x = ctypes.c_int16(a_FIFO_buffer[28] << 8 | a_FIFO_buffer[29]).value
        y = ctypes.c_int16(a_FIFO_buffer[32] << 8 | a_FIFO_buffer[33]).value
        z = ctypes.c_int16(a_FIFO_buffer[36] << 8 | a_FIFO_buffer[37]).value
        return V(x, y, z)

    def DMP_get_gravity(self, a_quat):
        x = 2.0 * (a_quat.x * a_quat.z - a_quat.w * a_quat.y)
        y = 2.0 * (a_quat.w * a_quat.x + a_quat.y * a_quat.z)
        z = 1.0 * (a_quat.w * a_quat.w - a_quat.x * a_quat.x -
                   a_quat.y * a_quat.y + a_quat.z * a_quat.z)
        return V(x, y, z)

    # def DMP_get_linear_accel_int16(self, a_v_raw, a_grav):
    #     x = ctypes.c_int16(a_v_raw.x - (a_grav.x*8192)).value
    #     y = ctypes.c_int16(a_v_raw.y - (a_grav.y*8192)).value
    #     z = ctypes.c_int16(a_v_raw.y - (a_grav.y*8192)).value
    #     return V(x, y, z)

    ### NEW LINEAR ACCELERATION function ###
    # The output of raw acceleration axes are according to the body of IMU.
    # This function gives the linear acceleration, which is according to the EARTH!
    # In a stationary situation, the output of this function will always be (0,0,g).
    def get_linear_accel(self, accel_raw, quat):
        quat.normalize()
        return accel_raw.get_rotated(quat)
    ### END ###

    def DMP_get_euler(self, a_quat):
        psi = math.atan2(2*a_quat.x*a_quat.y - 2*a_quat.w*a_quat.z,
                         2*a_quat.w*a_quat.w + 2*a_quat.x*a_quat.x - 1)
        theta = -math.asin(2*a_quat.x*a_quat.z + 2*a_quat.w*a_quat.y)
        phi = math.atan2(2*a_quat.y*a_quat.z - 2*a_quat.w*a_quat.x,
                         2*a_quat.w*a_quat.w + 2*a_quat.z*a_quat.z - 1)
        return V(psi, theta, phi)

    def DMP_get_roll_pitch_yaw(self, a_quat):
        # # roll: (tilt left/right, about X axis)
        # roll = math.atan(a_grav_vect.y /
        #                  math.sqrt(a_grav_vect.x*a_grav_vect.x +
        #                       a_grav_vect.z*a_grav_vect.z))
        # # pitch: (nose up/down, about Y axis)
        # pitch = math.atan(a_grav_vect.x /
        #                   math.sqrt(a_grav_vect.y*a_grav_vect.y +
        #                        a_grav_vect.z*a_grav_vect.z))
        # # yaw: (about Z axis)
        # yaw = math.atan2(2*a_quat.x*a_quat.y - 2*a_quat.w*a_quat.z,
        #                  2*a_quat.w*a_quat.w + 2*a_quat.x*a_quat.x - 1)
        # return V(roll, pitch, yaw)

        quat = R.from_quat((a_quat.x,a_quat.y,a_quat.z,a_quat.w))
        rpy = quat.as_euler('xyz', degrees=0)

        return V(rpy[0],rpy[1],rpy[2])

    def DMP_get_euler_roll_pitch_yaw(self, a_quat):
        rad_ypr = self.DMP_get_roll_pitch_yaw(a_quat)
        roll = rad_ypr.x * (180.0/math.pi)
        pitch = rad_ypr.y * (180.0/math.pi)
        yaw = rad_ypr.z * (180.0/math.pi)
        return V(roll, pitch, yaw)

    def DMP_get_linear_accel(self, a_vector_raw, a_vect_grav):
        x = a_vector_raw.x - a_vect_grav.x*8192
        y = a_vector_raw.y - a_vect_grav.y*8192
        z = a_vector_raw.z - a_vect_grav.z*8192
        return V(x, y, z)


class MPU6050IRQHandler:
    __mpu = MPU6050
    __FIFO_buffer = list()
    __count = 0
    __packet_size = None
    __detected_error = False
    __logging = False
    __log_file = None
    __csv_writer = None
    __start_time = None
    __debug = None

    # def __init__(self, a_i2c_bus, a_device_address, a_x_accel_offset,
    #             a_y_accel_offset, a_z_accel_offset, a_x_gyro_offset,
    #             a_y_gyro_offset, a_z_gyro_offset, a_enable_debug_output):
    #    self.__mpu = MPU6050(a_i2c_bus, a_device_address, a_x_accel_offset,
    #                         a_y_accel_offset, a_z_accel_offset,
    #                         a_x_gyro_offset, a_y_gyro_offset, a_z_gyro_offset,
    #                         a_enable_debug_output)
    def __init__(self, a_mpu, a_logging=False, a_log_file='log.csv',
                 a_debug=False):
        self.__mpu = a_mpu
        self.__FIFO_buffer = [0]*64
        self.__mpu.dmp_initialize()
        self.__mpu.set_DMP_enabled(True)
        self.__packet_size = self.__mpu.DMP_get_FIFO_packet_size()
        mpu_int_status = self.__mpu.get_int_status()
        if a_logging:
            self.__start_time = time.clock()
            self.__logging = True
            self.__log_file = open(a_log_file, 'ab')
            self.__csv_writer = csv.writer(self.__log_file, delimiter=',',
                                           quotechar='|',
                                           quoting=csv.QUOTE_MINIMAL)
        self.__debug = a_debug

    def action(self, channel):
        if self.__detected_error:
            # Clear FIFO and reset MPU
            mpu_int_status = self.__mpu.get_int_status()
            self.__mpu.reset_FIFO()
            self.__detected_error = False
            return

        try:
            FIFO_count = self.__mpu.get_FIFO_count()
            mpu_int_status = self.__mpu.get_int_status()
        except:
            self.__detected_error = True
            return

        # If overflow is detected by status or fifo count we want to reset
        if (FIFO_count == 1024) or (mpu_int_status & 0x10):
            try:
                self.__mpu.reset_FIFO()
            except:
                self.__detected_error = True
                return

        elif (mpu_int_status & 0x02):
            # Wait until packet_size number of bytes are ready for reading,
            # default is 42 bytes
            while FIFO_count < self.__packet_size:
                try:
                    FIFO_count = self.__mpu.get_FIFO_count()
                except:
                    self.__detected_error = True
                    return

            while FIFO_count > self.__packet_size:

                try:
                    self.__FIFO_buffer = \
                        self.__mpu.get_FIFO_bytes(self.__packet_size)
                except:
                    self.__detected_error = True
                    return
                accel = \
                    self.__mpu.DMP_get_acceleration_int16(self.__FIFO_buffer)
                quat = self.__mpu.DMP_get_quaternion_int16(self.__FIFO_buffer)
                grav = self.__mpu.DMP_get_gravity(quat)
                roll_pitch_yaw = self.__mpu.DMP_get_euler_roll_pitch_yaw(quat,
                                                                         grav)
                if self.__logging:
                    delta_time = time.clock() - self.__start_time
                    data_concat = ['%.4f' % delta_time] + \
                        [accel.x, accel.y, accel.z] + \
                        ['%.3f' % roll_pitch_yaw.x,
                         '%.3f' % roll_pitch_yaw.y,
                         '%.3f' % roll_pitch_yaw.z]
                    self.__csv_writer.writerow(data_concat)

                if (self.__debug) and (self.__count % 100 == 0):
                    print('roll: ' + str(roll_pitch_yaw.x))
                    print('pitch: ' + str(roll_pitch_yaw.y))
                    print('yaw: ' + str(roll_pitch_yaw.z))
                self.__count += 1
                FIFO_count -= self.__packet_size
