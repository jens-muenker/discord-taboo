def log_In_Console(msg, func_name, type):

    if type == "err":

        print("[ERROR] |{}| {}".format(func_name, msg))

    elif type == "war":

        print("[WARNING] |{}| {}".format(func_name, msg))

    elif type == "inf":

        print("[INFO] |{}| {}".format(func_name, msg))

    else:

        print("[NON-TYPE] |{}| {}".format(func_name, msg))