import datetime
import traceback

def activity_log(args):
	try:
		filename = "./logs/" + str(datetime.datetime.now().strftime("%Y_%m_%d")) + "_activity_log.log"
		file = open(filename, "a")
		current_timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f"))
		file.write(
			"[" + current_timestamp + "] " + 
			args["IP"] + " (" + 
			((args["State"] + ", ") if "State" in args and args["State"] != None else "") + 
			args["Country"] + ") | " + 
			args["Name"] + " (" + args["User_ID"] + ") | " + 
			args["Action"] + " | " + 
			args["URL"] + "\n"
		)
		
	except Exception as e:
		print(str(type(e)))
		print(str(e))
		print(traceback.format_exc())

	finally:
		file.close()

def error_log(msg):
	try:
		filename = "./logs/" + str(datetime.datetime.now().strftime("%Y_%m_%d")) + "_error_log.log"
		file = open(filename, "a")

		current_timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f"))
		file.write(current_timestamp + ": " + msg + "\n")

	except Exception as e:
		print(str(type(e)))
		print(str(e))
		print(traceback.format_exc())

	finally:
		file.close()
