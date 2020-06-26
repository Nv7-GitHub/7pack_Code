from sys import executable
from os import system
from distutils.core import setup
from os import remove

# put shebang
lines = open("7pack.py").read().split("\n")
lines.insert(0, "#!" + executable)
lines = "\n".join(lines)
with open("7pack", "w+") as f:
    f.write(lines)
    system("chmod +x " + "7pack")

# Run Setup
setup(name="7pack",
      install_requires=["certifi", "chardet", "gitdb", "GitPython", "idna", "requests", "smmap", "urllib3"],
      scripts=["7pack", "indexed.json"]
      )
remove("7pack")
