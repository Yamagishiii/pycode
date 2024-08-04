import tkinter as tk
import threading, os, asyncio, contextlib

OS = ""
user = ""
setjs = {}
theme = {}
si = ""
cwd = ""
termdata = ""
termdata2 = ""
runcheck = 0

class panel(tk.Frame):
	def __init__(self, master):
		super(panel, self).__init__(master)
		self.job = None
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

		self.termtxt = tk.Text(self)
		self.termtxt.grid(column=0, row=0, rowspan=2, sticky=tk.NSEW)
		self.termtxt.insert("1.0", f"{cwd}>")
		self.termtxt.configure(bg=theme["text"]["back"], fg=theme["text"]["fore"], selectbackground=theme["text"]["sback"], selectforeground=theme["text"]["sfore"], insertbackground=theme["text"]["insert"])

		self.termtxt.bind("<Return>", self.start_command)
		self.termtxt.bind("<<Modified>>", self.datacheck)

		self.termkill = tk.Button(self, text="Reload", command=self.rebootterm)
		self.termkill.grid(column=0, row=0, sticky=tk.NE)

		self.close = tk.Label(self, text="X")
		self.close.grid(column=1, row=0, sticky=tk.N)

		termscroll = tk.Scrollbar(self, command=self.termtxt.yview)
		termscroll.grid(column=1, row=1, sticky=tk.NS)
		self.termtxt["yscrollcommand"] = termscroll.set

	def start_command(self, event=None):
		global cwd, termdata
		command = self.termtxt.get("1.0", "end-1c").replace(termdata, "")
		if "set['path']['python']" in command:
			command = command.replace("set['path']['python']", setjs["path"]["python"])
		elif 'set["path"]["python"]' in command:
			command = command.replace('set["path"]["python"]', setjs["path"]["python"])
		command = list(command.replace("\n", "").split(" "))
		if "cd" in command:
			try:command = command[1]
			except:
				threading.Thread(target=self.insert).start()
				return
			try:os.chdir(command)
			except:self.termtxt.insert('end', f"\ncd : パス '{os.path.abspath(command)}' が存在しないため検出できません。")
		elif command == [""]:pass
		else:
			threading.Thread(target=lambda: asyncio.run(self.run_command_in_realtime(command))).start()
			return
		threading.Thread(target=self.insert).start()

	def datacheck(self, e):
		global termdata, termdata2
		if termdata in self.termtxt.get("1.0", "end-1c"):
			termdata2 = self.termtxt.get("1.0", "end-1c")
		else:
			self.termtxt.delete("1.0", "end")
			self.termtxt.insert("1.0", termdata2)
			self.termtxt.see(tk.END)
		e.widget.edit_modified(False)
	def rebootterm(self):
		try:
			self.termprocess.kill()
		except:print("terminal process kill error")
		self.termtxt.config(state="normal")
		self.termtxt.delete("1.0", "end")
		self.insert()
#		except:pass

	def insert(self):
		global termdata, cwd
		self.termtxt["state"] = "normal"
		cwd = os.getcwd()
		self.termtxt.insert("end", cwd + ">")
		termdata = self.termtxt.get("1.0", "end-1c")
		self.termtxt.see("end")

	async def update_termtxt(self):
		global termdata, runcheck
		try:
			runcheck = 2
			while True:
				line = await self.termprocess.stdout.readline()
				if line:
					line = line.decode("utf-8")
					line = line.strip()
					self.termtxt.config(state="normal")
					self.termtxt.insert('end', line + '\n')
					self.termtxt.config(state="disabled")
					self.termtxt.see(tk.END)
				else:
					termdata = self.termtxt.get("1.0", "end-1c")
					self.termtxt.config(state="normal")
					self.insert()
					break
		finally:
			await self.termprocess.wait()
			runcheck = 0

	async def run(self, command):
		try:self.termprocess = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT, startupinfo=si)
		except:
			return
		await self.update_termtxt()

	async def poll(self, proc):
		with contextlib.suppress(asyncio.TimeoutError):
			await asyncio.wait_for(proc.wait(), 1e-6)
		return proc.returncode is None

	async def run_command_in_realtime(self, command):
		self.termtxt.config(state="disabled")
		await self.run(command)
