import os
import appdata
import zlib
import base64
import json

iconsjson = appdata.iconsjson
icodata = iconsjson["pycode.ico"]

def setting(dir, setjsdata):
	if not os.path.isfile(f"{dir}/settings.json"):
		with open(f"{dir}/settings.json", "w", encoding = "utf-8") as settxt:settxt.write(setjsdata)

def makedir(dir):
	if not os.path.isdir(dir):
		os.makedirs(dir)

def main(dir, setjs):
	dirli = [dir, f"{dir}/Logs",f"{dir}/Content", f"{dir}/__Cache__", f"{dir}/Addons", f"{dir}/Content/icons", f"{dir}/__Cache__/icons"]
	for i in dirli:
		makedir(i)
		
	if not os.path.isfile(f"{dir}/Content/geometry.txt"):
		with open(f"{dir}/Content/geometry.txt", "w", encoding="utf-8") as temp:temp.write("1140x520\nzoomed\n0")

	if not os.path.isfile(f"{dir}/Content/Highlight-Blacklist.txt"):
		with open(f"{dir}/Content/Highlight-Blacklist.txt", "w", encoding="utf-8") as temp:temp.write(".txt\n")

	if not os.path.isfile(f"{dir}/Content/pycode.ico"):
		icohexdata = zlib.decompress(base64.b85decode(icodata)).decode()
		bytedata = bytes.fromhex(icohexdata)
		with open(f"{dir}/Content/pycode.ico", "wb") as ico:ico.write(bytedata)

	if not os.path.isfile(f"{dir}/Content/lexers.json"):
		extension_to_lexer = {".py": "PythonLexer", ".pyw": "PythonLexer", ".html": "HtmlLexer", ".css": "CssLexer", ".js": "JavascriptLexer", ".java": "JavaLexer", ".c": "CLexer", ".cpp": "CppLexer", ".cxx": "CppLexer", ".cs": "CSharpLexer", ".php": "PhpLexer", ".pl": "PerlLexer", ".rb": "RubyLexer", ".swift": "SwiftLexer", ".sql": "SqlLexer", ".xml": "XmlLexer", ".xhtml": "XmlLexer", ".json": "JsonLexer", ".yaml": "YamlLexer", ".yml": "YamlLexer", ".md": "MarkdownLexer", ".tex": "TexLexer", ".ini": "IniLexer", ".sh": "BashLexer", ".diff": "DiffLexer", ".makefile": "MakefileLexer", ".dockerfile": "DockerLexer"}
		with open(f"{dir}/Content/lexers.json", "w", encoding="utf-8") as f:
			json.dump(extension_to_lexer, f, indent=4)

	setting(dir, setjs)