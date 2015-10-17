import configparser

def check_config_file(file_to_open):
    print("PRJ file to check " + str(file_to_open))
    ConfigOK=1
    Config = ConfigParser.ConfigParser()
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
    
