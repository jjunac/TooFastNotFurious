import glob
import os
import subprocess

path = os.path

files = [path.splitext(path.basename(f))[0] for f in glob.glob("simulator/*.py") if path.basename(f) != "__init__.py"]

#report = open("mutation-testing-report.txt", 'w')

for f in files:

    config_file_name = "cosmic-ray.%s.yml" % f
    config_file = open(config_file_name, 'w')
    config_file.write("""module: {module_name}

baseline: 10

exclude-modules:

test-runner:
  name: unittest
  args:

execution-engine:
  name: local
""".format(module_name="simulator." + f))
    config_file.close()

    print("Generating session...")
    session_name = "session_" + f
    subprocess.call(["cosmic-ray", "init", config_file_name, session_name])

    subprocess.call(["cosmic-ray", "exec", session_name])

    print("Survival rate for %s:" % f, end='')
    os.system("cosmic-ray dump %s | cr-rate" % session_name)
