error_flag = False 

def report(line, where, message):
    print("[line " + str(line+1) + "] Error" + where + ": " + message)
    global error_flag 
    error_flag = True 

def error(line, message):
    report(line, "", message)