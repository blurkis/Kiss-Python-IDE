import sys
import os
import configparser

def save_config_file(file_to_save):
    print("Saving project..")
    Config = configparser.ConfigParser()
    Config.add_section("PyIDE")
    Config.set("PyIDE","VERSION", "1.0" )
    Config.set("PyIDE", "PRJ_FILES", "main.py,config.py")
    Config.set("PyIDE", "PRJ_NAME", "PyIDE")
    Config.set("PyIDE", "AUTHOR", "Kent Nyberg")
    Config.set("PyIDE", "EMAIL", "nyberg.kent@gmail.com")
    Config.write(file_to_save)
    


def check_config_file(file_to_open):
    print("PRJ file to check " + str(file_to_open))
    ConfigOK=1
    Config = configparser.ConfigParser()
    Config.read(file_to_open)
    try:
        Config.get('PyIDE','VERSION')
    except:
        ConfigOK=0
    try:
        Config.get('PyIDE','PRJ_FILES')
    except:
        ConfigOK=0
    try:
        Config.get('PyIDE','PRJ_NAME')
    except:
        ConfigOK=0
    if ConfigOK ==1:
       print("Config OK")
       return Config.get('PyIDE', 'PRJ_FILES')
    else:
       print("Config not ok.")
       return "FALSE"
    
