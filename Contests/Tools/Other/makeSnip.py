## make snippets in sublime text based on .h files with capital first letters

import os,shutil,sys

PREFIX="""/Users/benq/Library/Application Support/Sublime Text 3/Packages/User"""
LOC=PREFIX+"""/algos/"""

if os.path.exists(LOC):
	shutil.rmtree(LOC)
os.makedirs(LOC)

pref = """
<snippet>
<!-- Hello, ${1:this} is a ${2:snippet}.-->
<content><![CDATA["""

mid="""
]]></content>
	<tabTrigger>"""

suf="""</tabTrigger>
	<scope>source.c++</scope>
	<!-- <description> demo description </description> -->
</snippet>"""

print("SNIPPETS LOC:\n\n",LOC.replace(' ','\\ '),'\n');

snippets = ""
temp = ""

for root, dirs, files in os.walk("/Users/benq/Documents/USACO/Implementations",topdown=False):
	# for name in dirs:
		# print(os.path.join(root, name))
	for name in files:
		if name.endswith(".h"):
			if name[0].isupper():
				short = name[:-2]
				if '(' in short:
					short = short[:short.find('(')]
				short = short.rstrip()
				PATH = LOC+short+".sublime-snippet"
				with open(os.path.join(root, name),"r") as fin:
					with open(PATH,"w") as fout:
						fout.write(pref)
						for a in fin:
							fout.write(a.replace('$','\\$'))
						fout.write(mid)
						fout.write(short)
						fout.write(suf)
				# print(os.path.join(root, name))
		if name.endswith(".cpp"):
			if "templateLong" in name:
				short = "Temp"
				PATH = LOC+short+".sublime-snippet"
				with open(os.path.join(root, name),"r") as fin:
					flag = False
					for a in fin:
						if "int main()" in a:
							flag = True
						a = a.replace('$','\\$')
						if flag and a == "\t\n":
							a = "\t$0\n"
						temp += a
				with open(PATH,"w") as fout:
					fout.write(pref)
					fout.write(temp)
					fout.write(mid)
					fout.write(short)
					fout.write(suf)
			elif "templateShort" in name:
				short = "TempShort"
				PATH = LOC+short+".sublime-snippet"
				with open(os.path.join(root, name),"r") as fin:
					with open(PATH,"w") as fout:
						fout.write(pref)
						flag = False
						for a in fin:
							if "int main()" in a:
								flag = True
							a = a.replace('$','\\$')
							if flag and "ios_base" in a:
								ind = a.find("ios_base")
								fout.write(a[:ind]+"\n")
								fout.write("\t"+a[ind:-2]+"\n")
								fout.write("\t$0\n}\n")
							else:
								fout.write(a)
						fout.write(mid)
						fout.write(short)
						fout.write(suf)
		if name == "Snippets.md":
			snippets = os.path.join(root, name)

assert len(snippets) > 0, "snippets not found"

# print("TEMPLATE",temp)
codes = []
names = []
with open(snippets,"r") as fin:
	lines = list(fin)
	flag = 0
	for i in range(len(lines)):
		if "```" in lines[i]: # entered or exited code
			flag ^= 1
			if flag == 1:
				codes.append([])
				names.append(lines[i-2][3:].rstrip())
				continue
		if flag == 1:
			codes[-1].append(lines[i])

ST = temp.find("int main()")
EN = ST
while temp[EN] != '}':
	EN += 1
EN += 2

for i in range(len(names)):
	short = names[i]
	PATH = LOC+short+".sublime-snippet"
	code = ""
	for a in codes[i]:
		# a = a.replace('$','\\$')
		# if "TC" in names[i]:
			# a = a.replace('Name','${1:Name}')
			# a = a.replace('method','${2:method}')
		code += a
	if "TC" in names[i] or "FHC" in names[i]:
		code = temp[:ST]+code+temp[EN:]
	with open(PATH,"w") as fout:
		fout.write(pref)
		fout.write(code)
		fout.write(mid)
		fout.write(short)
		fout.write(suf)
	# if "FHC" in names[i]:
	# 	with open(LOC+"GCJ"+".sublime-snippet","w") as fout:
	# 		fout.write(pref)
	# 		for a in codes[i]:
	# 			a = a.replace('$','\\$')
	# 			fout.write(a)
	# 		fout.write(mid)
	# 		fout.write("GCJ")
	# 		fout.write(suf)

