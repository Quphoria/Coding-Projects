import os, sys, os.path

script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
version_filename = script_path + "\\version.id"
version_file = open(version_filename,"r")
version = version_file.read()
version_file.close()

print("Python DNS Server version %s" % version)
version_num = float(version)

update_settings_template = """{
  "auto-update":true,
  "update_src":"https://portfw.ddns.net:4443/dns_server/",
  "pid-file":"dns.pid",
  "update_files":[
    "dns_server.py",
    "update_settings.json",
    "check_update.py",
    "NSSM/nssm.exe",
    "version.id"
  ],
  "pre-update-commands":[
    "NSSM/nssm.exe stop \"Python DNS Server\""
  ],
  "post-update-commands":[
    "NSSM/nssm.exe start \"Python DNS Sever\""
  ],
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

import requests, threading

class UpdateThread (threading.Thread):
    def __init__(self,update_settings,script_path):
        import os, time, requests, subprocess, sys
        threading.Thread.__init__(self)
        self.update_settings = update_settings
        self.script_path = script_path + "\\"
        self.os = os
        self.time = time
        self.requests = requests
        self.subprocess = subprocess
        self.sys = sys
    def wget(self,file,filepath):
        os = self.os
        time = self.time
        requests = self.requests
        subprocess = self.subprocess
        sys = self.sys
        print("Downloading %s..." % file, end="")
        sys.stdout.flush()
        webdata = requests.get(self.update_settings["update_src"] + file)
        if webdata.status_code == 200:
            up_file = open(filepath,"wb")
            up_file.write(webdata.content)
            up_file.close()
            print("Done")
        else:
            print("Failed, Error: %s" % webdata.status_code)
            webdata.raise_for_status()
    def run(self):
        os = self.os
        time = self.time
        requests = self.requests
        subprocess = self.subprocess
        sys = self.sys
        os.chdir(self.script_path)
        pid_file = open(self.script_path + self.update_settings["pid-file"],"w")
        pid_file.write("-1")
        pid_file.close()
        time.sleep(1)
        print("Starting Update Thread")
        print("Waiting for program to finish...")
        time.sleep(1)
        print("Running Pre-update commands...")
        for command in self.update_settings["pre-update-commands"]:
            try:
                os.system(command)
            except Exception as ex:
                print("An Error Occurred with the pre update command: %s, Error: %s" % (command,ex))
        time.sleep(1)
        print("Updating Program...")
        invalid_update = False

        for file in self.update_settings["update_files"]:
            try:
                self.wget(file, self.script_path + file + ".tmp")
            except Exception as ex:
                print(str(ex))
                invalid_update = True
        copy_status = 0
        try:
            if not invalid_update:
                for file in self.update_settings["update_files"]:
                    os.rename(self.script_path + file, self.script_path + file + ".tmp2")
                copy_status = 1
                for file in self.update_settings["update_files"]:
                    os.rename(self.script_path + file + ".tmp", self.script_path + file)
                copy_status = 2
                for file in self.update_settings["update_files"]:
                    os.remove(self.script_path + file + ".tmp2")
                copy_status = 3
                print("Update Complete.")
        except Exception as ex:
            print("An error occurred while copying update files, Error: %s" % ex)
            invalid_update = True
            print("Reverting Changes...",end="")
            sys.stdout.flush()
            if copy_status == 2:
                for file in self.update_settings["update_files"]:
                    os.remove(self.script_path + file)
                    os.rename(self.script_path + file + ".tmp2", self.script_path + file)
                    try:
                        os.remove(self.script_path + file + ".tmp")
                    except:
                        pass
            print("Done")

        if invalid_update:
            print("Update Failed.")
        print("Exiting Update Thread")
        print()
        time.sleep(1)
        print("Running Post-update commands...")
        for command in self.update_settings["post-update-commands"]:
            try:
                os.system(command)
            except Exception as ex:
                print("An Error Occurred with the post update command: %s, Error: %s" % (command,ex))
        time.sleep(1)
        print("Done.")
        time.sleep(2)

def check_for_update():
    print("Checking for update...")
    try:
        web_version = float(requests.get(updatesettingsdata["update_src"] + "version.id").content.decode())
        if web_version <= version_num:
            print("Program Up-to-date")
        else:
            print("Update Available")
            if updatesettingsdata["auto-update"]:
                print("Starting Update...")
                UThread = UpdateThread(updatesettingsdata,script_path)
                UThread.run()
    except Exception as ex:
        print("Update Check Failed. Error: %s" % ex)
# check_for_update()
