#! /usr/bin/python

#import re, shlex, os, sys
import os, sys

template_dir = r"/Users/DX044/workspace/android-generator/templates"
values = {"<PACKAGE>" : "com.test.test", 
        "<CLASS_NAME>" : "TestActivity",
        "<LAYOUT_CLASS_NAME>" : "test_activity"}

template_list = []

def parse_string(line):
    for k in values.keys():
        if line.find(k):
            line = line.replace(k, values[k])
    return line

def copy_file(in_file_path, out_file_path):
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
    try: 
        f = open(r"./template.list", "r")
        for line in in_file:
            template_list.append(line)
        f.close()
    except:
        print "Could not open the template list"

def set_parameters(argv):
    values["<PACKAGE>"] = "com.xtremelabs.TODO"
    values["<CLASS_NAME>"] = argv[1]
    values["<LAYOUT_CLASS_NAME"] = argv[2]

def main(argv):
    # DEBUG
    print argv
    print "starting"
    # END_DEBUG 

    if (len(argv) < 3):
        usage()
        sys.exit(2)

    set_parameters(argv)

    if (argv[0].lower() == "activity"):
        copy_file(r"./templates/src/Activity.java", r"./" + values["<CLASS_NAME>"] +".java")
        update_manifest()
    else:
        usage()

    os.chdir(template_dir + r"/src")
    print os.getcwd()

    #copy_file("Activity.java", "activity_copy.java")

    print "done" 

if __name__ == "__main__":
    main(sys.argv[1:])

