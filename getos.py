import os, sys
from tkinter import messagebox as msg
def getos():
	temp = dict(os.environ)
	if "DESKTOP_SESSION" in temp:OS=temp["DESKTOP_SESSION"]
	elif "OS" in temp:OS="Windows"
	else:
		msg.showwarning(message = f"不明なOS")
		sys.exit()
	return OS