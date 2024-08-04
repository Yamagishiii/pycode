import zlib, base64, shutil
with open("./dist/main/main.exe", "rb") as f:
	temp = base64.b85encode(zlib.compress(bytes.hex(f.read()).encode())).decode()
	print(temp)
	with open("./main.txt", "w", encoding="utf-8") as f:
		f.write(temp)
shutil.move("./dist/main/_internal", "./_internal")
shutil.move("./dist/main/main.exe", "./main.exe")