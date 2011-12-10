#! /usr/bin/python2

# TODO :: figure out how to switch between python2 and python

#import re, shlex, os, sys
import os, sys, json

PACKAGE = "<PACKAGE>"
CLASS_NAME = "<CLASS_NAME>"
LAYOUT_CLASS_NAME = "<LAYOUT_CLASS_NAME>"
TYPE = "<TYPE>"

template_dir = r"./templates"
values = {
        PACKAGE : "com.test.test", 
        CLASS_NAME : "TestActivity",
        LAYOUT_CLASS_NAME : "test_activity",
        TYPE : "test",
        }

template_list = []
conf_file_name = r"./android-scaffolding.conf"

default_conf_file_name = r"./Android-Scaffolding/android-scaffolding.conf"

def parse_string(line):
    for k in values.keys():
        if line.find(k):
            line = line.replace(k, values[k])
    return line

def copy_file(in_file_path, out_file_path):
    print in_file_path +  " " + out_file_path
    try:
        in_file = open(in_file_path)
        out_file = open(out_file_path, "w")
        
        for line in in_file:
            out_file.write(parse_string(line))

        in_file.close()
        out_file.close()

    except: 
        print "Something went wrong... ", sys.exc_info()[0]
    
def usage():
    # TODO :: this
    print "android-generator -- "

def get_template_list():
    in_str = ""
    global template_list
    try: 
        f = open(r"./template.list", "r")
        in_str = f.read().replace("\n","")
        f.close()
    except:
        print "Could not open the template list"

    template_list = json.loads(in_str)
    #DEBUG
    #print template_list

def load_config():
    lines = []
    if (os.path.exists(conf_file_name)):
        try:
            f = open(conf_file_name, "r")
            lines = f.readlines()
        except:
            print "ERROR :: Could not open the configuration file"
    else:
        try:
            f = open(default_conf_file_name, "r")
            lines = f.readlines()
        except:
            print "ERROR :: Could not open the default configuration file"
    parse_config(lines)

def parse_config(lines):
    for line in lines:
        param = line.split("=")
        values["<"+param[0]+">"] = param[1]

def set_parameters(argv):
    # TODO :: figure out how to get the package
    values[TYPE] = argv[0]
    values[CLASS_NAME] = argv[1]
    if (len(argv) > 2):
        values[LAYOUT_CLASS_NAME] = argv[2]
    else:
        values.pop(LAYOUT_CLASS_NAME)

def generate_files():
    template_item = None
    for key in template_list.keys():
        if (values[TYPE] == key):
            template_item = template_list[key]
            print "FOUND"
            break 

    if (template_item == None):
        print "ERROR :: Could not find the template item"
        usage()
        return

    for key in template_item.keys():
        item = template_item[key]
        out = ""
        if (item["type"] == "java"): 
            out = r"./" + item["out"] + values[PACKAGE].replace(".", "/") + "/" + values[CLASS_NAME] + "." + item["type"]
        elif (key == "layout" && values.get(LAYOUT_CLASS_NAME) != None)):
            if (values.get(LAYOUT_CLASS_NAME != None)):
                out = r"./" + item["out"] + values[LAYOUT_CLASS_NAME] + "." + item["type"]
            else:
                out = r"./" + item["out"] + item["default"] + "." + item["type"]
                print "ERROR :: missing layout file name, using template default"
        else: 
            out = r"./" + item["out"] + values[CLASS_NAME] + "." + item["type"]
        copy_file(r"./templates/"+item["in"], out)

def main(argv):
    # DEBUG
#    print argv
    print "starting"
    # END_DEBUG 

    if (len(argv) < 2):
        usage()
        sys.exit(2)
   
    load_config()
    set_parameters(argv)
    get_template_list()
    
    generate_files()
    
#    if (argv[0].lower() == "activity"):
#        copy_file(r"./templates/src/Activity.java", r"./" + values[CLASS_NAME] + ".java")
#        #update_manifest()
#    else:
#        usage()


    print "done" 

if __name__ == "__main__":
    main(sys.argv[1:])

