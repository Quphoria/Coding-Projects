import os, sys, os.path
from time import gmtime, strftime

script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
version_filename = script_path + "\\version.id"
version_file = open(version_filename,"r")
version = version_file.read()
version_file.close()

def dns_version():
    return version

version_num = float(version)

update_settings_template = """{
  "auto-update":true,
  "update_src":"https://portfw.ddns.net:4443/dns_server/",
  "pid-file":"dns.pid",
  "update-logfile":"Logs\\\\update.log",
  "old-update-logfile":"Logs\\\\Old\\\\update.log",
  "update_files":[
    "dns_server.py",
    "update_settings.json",
    "check_update.py",
    "version.id"
  ],
  "pre-update-commands":[
  ],
  "pre-copy-commands":[
  ],
  "post-update-commands":[
  ]
}"""

import json

updatesettingsfilename = "%s\\update_settings.json" % script_path
if (not os.path.isfile(updatesettingsfilename)):
    updatesettingsfile = open(updatesettingsfilename,"w")
    updatesettingsfile.write(update_settings_template)
    updatesettingsfile.close()
updatesettingsfile = open(updatesettingsfilename,"r")
updatesettingsdata = json.load(updatesettingsfile)
updatesettingsfile.close()

LoadTime = strftime("%Y-%m-%d %H-%M-%S", gmtime())
LogFileName = updatesettingsdata["update-logfile"]
TLogFileName = updatesettingsdata["old-update-logfile"].rsplit(".",1)[0] + " @ " + LoadTime + "." + updatesettingsdata["old-update-logfile"].rsplit(".",1)[1]
if os.path.exists(LogFileName):
    try:
        os.remove(LogFileName)
    except:
        pass
        
def Log(text="",end="\r\n"):
    if not os.path.exists(os.path.split(updatesettingsdata["old-update-logfile"])[0]):
        os.mkdir(os.path.split(updatesettingsdata["old-update-logfile"])[0])
    # sys.stdout.write((("%s" % text) + end))
    # sys.stdout.flush()
    LogFile = open(LogFileName,"ab")
    LogFile.write((("%s" % text) + end).encode())
    LogFile.close()
    LogFile = open(TLogFileName,"ab")
    LogFile.write((("%s" % text) + end).encode())
    LogFile.close()

import requests, threading

class UpdateThread (threading.Thread):
    def __init__(self,update_settings,script_path):
        import os, time, requests, subprocess
        threading.Thread.__init__(self)
        self.update_settings = update_settings
        self.script_path = script_path + "\\"
        self.os = os
        self.time = time
        self.requests = requests
        self.subprocess = subprocess
    def wget(self,file,filepath):
        os = self.os
        time = self.time
        requests = self.requests
        subprocess = self.subprocess
        Log("Downloading %s..." % file, end="")
        webdata = requests.get(self.update_settings["update_src"] + file.replace("\\","/"))
        if webdata.status_code == 200:
            up_file = open(filepath,"wb")
            up_file.write(webdata.content)
            up_file.close()
            Log("Done")
        else:
            Log("Failed, Error: %s" % webdata.status_code)
            webdata.raise_for_status()
    def run(self):
        os = self.os
        time = self.time
        requests = self.requests
        subprocess = self.subprocess
        os.chdir(self.script_path)
        pid_file = open(self.script_path + self.update_settings["pid-file"],"w")
        pid_file.write("-1")
        pid_file.close()
        time.sleep(1)
        Log("Starting Update Thread")
        Log("Waiting for program to finish...")
        time.sleep(1)
        Log("Running Pre-update commands...")
        for command in self.update_settings["pre-update-commands"]:
            try:
                Log("Running pre update command: %s" % command)
                outdata = subprocess.check_output(command, encoding='UTF-8', shell=True)
                Log("Command Output: %s" % outdata)
            except Exception as ex:
                Log("An Error Occurred with the pre update command: %s, Error: %s" % (command,ex))
        time.sleep(1)
        Log("Updating Program...")
        invalid_update = False

        for file in self.update_settings["update_files"]:
            try:
                self.wget(file, self.script_path + file + ".tmp")
            except Exception as ex:
                Log(str(ex))
                invalid_update = True
        copy_status = 0
        Log("Running Pre-copy commands...")

        for command in self.update_settings["pre-copy-commands"]:
            try:
                Log("Running pre copy command: %s" % command)
                outdata = subprocess.check_output(command, encoding='UTF-8', shell=True)
                Log("Command Output: %s" % outdata)
            except Exception as ex:
                Log("An Error Occurred with the pre copy command: %s, Error: %s" % (command,ex))
        try:
            if not invalid_update:
                for file in self.update_settings["update_files"]:
                    try:
                        os.remove(self.script_path + file + ".tmp2")
                    except:
                        pass
                    os.rename(self.script_path + file, self.script_path + file + ".tmp2")
                copy_status = 1
                for file in self.update_settings["update_files"]:
                    os.rename(self.script_path + file + ".tmp", self.script_path + file)
                copy_status = 2
                for file in self.update_settings["update_files"]:
                    os.remove(self.script_path + file + ".tmp2")
                copy_status = 3
                Log("Update Complete.")
        except Exception as ex:
            Log("An error occurred while copying update files, Error: %s" % ex)
            invalid_update = True
            Log("Reverting Changes...",end="")
            if copy_status == 2:
                for file in self.update_settings["update_files"]:
                    try:
                        os.remove(self.script_path + file)
                    except:
                        pass
                    try:
                        os.rename(self.script_path + file + ".tmp2", self.script_path + file)
                    except Exception as ex:
                        Log("An error occurred when restoring the file %s, Error: %s" % (file,ex))
                    try:
                        os.remove(self.script_path + file + ".tmp")
                    except:
                        pass
            Log("Done")

        if invalid_update:
            Log("Update Failed.")
        time.sleep(1)
        Log("Running Post-update commands...")
        for command in self.update_settings["post-update-commands"]:
            try:
                Log("Running post update command: %s" % command)
                outdata = subprocess.check_output(command, encoding='UTF-8', shell=True)
                Log("Command Output: %s" % outdata)
            except Exception as ex:
                Log("An Error Occurred with the post update command: %s, Error: %s" % (command,ex))
        Log("Done.")
        Log("Exiting Update Thread...")
        Log()
        if not invalid_update:
            pid_file = open(self.update_settings["pid-file"],"w")
            pid_file.write("-1")
            pid_file.close()

def check_for_update():
    # Log("Checking for update...")
    try:
        web_version = float(requests.get(updatesettingsdata["update_src"] + "version.id").content.decode())
        if web_version <= version_num:
            pass
            # Log("Program Up-to-date")
        else:
            Log("Update Available")
            if updatesettingsdata["auto-update"]:
                Log("[%s] Starting Update..." % strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                UThread = UpdateThread(updatesettingsdata,script_path)
                UThread.run()
    except Exception as ex:
        Log("Update Check Failed. Error: %s" % ex)

if __name__ == "__main__":
    check_for_update()
