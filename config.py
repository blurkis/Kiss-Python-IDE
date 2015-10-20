import sys
import os
import configparser

def save_config_file(self, file_to_save):
    print("Saving project..")
    Config = configparser.ConfigParser()
    Config.add_section("PyIDE")
    Config.set("PyIDE","VERSION", self.ProjectDict["ProjectVersion"] )
    Config.set("PyIDE", "PRJ_FILES", self.ProjectDict["ProjectFiles"])
    Config.set("PyIDE", "PRJ_NAME", self.ProjectDict["ProjectName"])
    Config.set("PyIDE", "AUTHOR", self.ProjectDict["Author"])
    Config.set("PyIDE", "EMAIL", self.ProjectDict["Email"])
    Config.write(file_to_save)



def check_config_file(self, file_to_open):
    print("PRJ file to check " + str(file_to_open))
    ConfigOK=1
    Config = configparser.ConfigParser()
    Config.read(file_to_open)
    try:
        Config.get('PyIDE','VERSION')
    except:
        ConfigOK=0
    try:
        self.ProjectDict["ProjectFiles"] =  Config.get('PyIDE','PRJ_FILES')
    except:
        ConfigOK=0
    try:
       self.ProjectDict["ProjectName"] =  Config.get('PyIDE','PRJ_NAME')
    except:
        ConfigOK=0
    if ConfigOK ==1:
       print("Config OK")
       return Config.get('PyIDE', 'PRJ_FILES')
    else:
       print("Config not ok.")
       return "FALSE"
    
