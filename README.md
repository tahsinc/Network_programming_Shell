# Network_programming_Shell
This is providing a user defined function to verify credential of network devices like switches or routers.

1. The code provides a file under utils folder. This file has a userdefined function to verify network device credential using netmiko library. 

2. The idea is just to provide an easier to get access to a network device or more than one network devices regardless the connectivity is through telnet or ssh. Currenly works with cisco ios-xe and cisco ios-xr. 
Users are welocome to add some modification for other platforms.

The code will check first the connectivity with telnet. If it fails then it will try connecting through ssh. 

3. The main.py is a template for how to use that userdefined function in your actual program.

Feel free to use it, suggest for changes or make changes for your own code.
