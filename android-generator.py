#! /usr/bin/python2

# TODO :: figure out how to switch between python2 and python

#import re, shlex, os, sys
import os, sys, json

PACKAGE = "<PACKAGE>"
CLASS_NAME = "<CLASS_NAME>"
LAYOUT_CLASS_NAME = "<LAYOUT_CLASS_NAME>"
TYPE = "<TYPE>"

template_dir = r"./templates"
values = {PACKAGE : "com.test.test", 
        CLASS_NAME : "TestActivity",
        LAYOUT_CLASS_NAME : "test_activity",
        TYPE : "test",
        }

template_list = []

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

def set_parameters(argv):
    # TODO :: figure out how to get the package
    values[TYPE] = argv[0]
    values[PACKAGE] = "com.xtremelabs.TODO"
    values[CLASS_NAME] = argv[1]
    values[LAYOUT_CLASS_NAME] = argv[2]

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
        copy_file(r"./templates/"+item, r"./" + values[CLASS_NAME] + "." + key)

def main(argv):
    # DEBUG
#    print argv
    print "starting"
    # END_DEBUG 

    if (len(argv) < 3):
        usage()
        sys.exit(2)

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

