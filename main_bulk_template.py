'''*** Main Code Template****'''

from utils.ios_xe_xr_login import *

boxes = """*** Replace with devices after verifying """

dcnter = 0
for box in boxes:
    dcnter = dcnter + 1
    print("\n ############# Working with devic {} ###############\n".format(dcnter))

    network_device = ConnectHandler(**box)
    network_device.set_terminal_width(0)
    if network_device.check_enable_mode() == False:
        network_device.enable()

    ###=============================================================================

    """Add your code here ....."""


    ###=============================================================================
    print(network_device.send_command_expect('wr\n')) # For IOS-XE commit
    print(network_device.commit()) # For IOS-XR commit
    network_device.disconnect()