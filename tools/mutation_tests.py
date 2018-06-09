import glob
import os
import subprocess

path = os.path

files = [path.splitext(path.basename(f))[0] for f in glob.glob("simulator/*.py") if path.basename(f) != "__init__.py"]


for f in files:

    print("###", f, "###")

    subprocess.call(["mut", "-q", "-t", "simulator.%s" % f , "-u", "simulator.tests"], shell=True)
