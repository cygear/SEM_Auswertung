from setuptools import setup, find_packages
from distutils import spawn
import subprocess
import os

package_data = {'': ['*.json']}
if os.path.isfile("src/qao/devices/digitizer2fw/scripts/Digitizer2Mixin.py"):
        package_data["qao"] = ["devices/digitizer2fw/scripts/Digitizer2Mixin.py"]

source_path = 'src'
packages = find_packages(source_path)

distribution = setup(name='qao',
               version='1.0.1',
               packages=packages,
               package_dir={'': source_path},
               package_data=package_data,
               scripts=['bin/messagebus'],
                entry_points = {
                    'console_scripts': ['qjobs=qao.io.remote.jobs.submit:main'],
                }
               )


if spawn.find_executable("qmake") and spawn.find_executable("make") and False:
    # install and deploy QaoQml
    QAOQML = 'QaoQml'
    cwd = os.getcwd()
    os.chdir(os.path.join(cwd, QAOQML))

    # create the makefile
    spawn.spawn(["qmake-qt5"] if spawn.find_executable("qmake-qt5") else ["qmake", "--qt=5"])

    # build the stuff
    spawn.spawn(["make"])

    # installation
    if 'develop' in distribution.commands:
        spawn.spawn(["make", "develop"])
    elif 'install' in distribution.commands:
        spawn.spawn(["make", "install"])
    os.chdir(cwd)
