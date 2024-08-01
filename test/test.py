import logging
from test2 import Test_2
import time
# Create a custom logger
logger = logging.getLogger(__name__)
logger_format = (' - %(message)s')
logging.basicConfig(format = logger_format, level=logging.INFO)
# Create handlers

def install_checker():
    '''Ml30s on 3.17 need you to either wait 10 seconds or Ctrl X to confirm and install, 
    if you press esc it will cancel install'''
    logger.info(f"Checking")
    for _ in range(120):
        logger.info(f'LOOP {_}')
        #time.sleep(0.5)
        lines = ('Firmware or Config via  1K Xmodem: CPI: New firmware ver 3.17.5 PI: Image size 772292 downloaded 773120 01/01/00,00:00:00 Hello from MTU4 init...Option bytes: fffaae1 Restore state, sz 173 01/01/00,00:00:00 Set fuel level 0x00 01/01/00,00:00:00 CCE: Setting states to 0x00000000 01/01/00,00:00:00 Flags M e 01/01/00,00:00:00 Restored GPI states to 0x00 01/01/00,00:00:00 BS: Restore ok 98 bytes, 0x60001402 01/01/00,00:00:00 Asset Block: error, read failed 01/01/00,00:00:00 Restore AssetIMEI failed, len 1')

        if not lines: continue
        
        if "Ctrl X" in str(lines):
            # self.write_commands(chr(24))
            # logger.info(f"{self.serial_port_name} SENDING CTRL X")
            # time.sleep(5)
            continue

        if "install failed" in str(lines):
            logger.warning(f'INSTALL FAILED')
            return False
        
        if "Abort" in str(lines):
            logger.warning(f'INSTALL FAILED')
            return False
        
        if "Hello" in str(lines):
            logger.info(f'Unit replied with Hello')
            break
        
        logger.info(f'Install Check - IS ALIVE')

    logger.info('CHECKER TIMEOUT')
    return False

install_checker()