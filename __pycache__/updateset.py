with open("C:/users/yamat/appdata/local/.pycode/application/3.0.0/main.py", "r", encoding="utf-8") as f:
    data = f.read()
with open("C:/users/yamat/appdata/local/.pycode/application/3.0.0/main.py", "r", encoding="utf-8") as f:
    read = f.readlines()
print(data,read)
for i in read:
    if 'version = ["3.0.0-Preview' in i:
        version = i[12:-12]
versionli = version.split(".")
versionli[-1] = str(int(versionli[-1]) + 1)
version_ = ""
for i in versionli:
    version_ += f"{i}."
version_ = version_[0:-1]
with open("C:/users/yamat/appdata/local/.pycode/application/3.0.0/main.py", "w", encoding="utf-8") as f:
    f.write(data.replace(version, version_))