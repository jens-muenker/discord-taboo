from datetime import datetime
from termcolor import colored, cprint
import colorama

def log_In_Console(msg, func_name, type=None):

    colorama.init()

    dateTimeObj = datetime.now()
    current_time = dateTimeObj.strftime("%d.%m.%Y %H:%M:%S")

    if type == "err":

        out = colored(str("[ERROR] [{}] |{}| {}".format(str(current_time), func_name, msg)), "red")

    elif type == "war":

        out = colored(str("[WARNING] [{}] |{}| {}".format(str(current_time), func_name, msg)), "yellow")

    elif type == "inf":

        out = colored(str("[INFO] [{}] |{}| {}".format(str(current_time), func_name, msg)), "green")
        
    else:

        out = colored(str("[NON-TYPE] [{}] |{}| {}".format(str(current_time), func_name, msg)), "white")
        
    cprint(out)