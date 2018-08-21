import logging
import sys
fmt = logging.Formatter("%(asctime)s - %(name)s - %(ip)s - %(username)s - %(message)s")
h_console = logging.StreamHandler(sys.stdout)
h_console.setFormatter(fmt)
logger = logging.getLogger("myPro")
logger.setLevel(logging.DEBUG)
logger.addHandler(h_console)
extra_dict = {"ip": "113.208.78.29", "username": "Petter"}
logger.debug("User Login!", extra=extra_dict)
extra_dict = {"ip": "223.190.65.139", "username": "Jerry"}
logger.info("User Access!", extra=extra_dict)