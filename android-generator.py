import os, sys, json, re
from ManifestDomHandler import ManifestDomHandler

PACKAGE = "<PACKAGE>"
CLASS_NAME = "<CLASS_NAME>"
LAYOUT_CLASS_NAME = "<LAYOUT_CLASS_NAME>"
TYPE = "<TYPE>"
PACKAGE_DETAIL = "PACKAGE_DETAIL"
OBJECT = "OBJECT"

template_dir = r"./templates"
values = {
        PACKAGE : "com.test.test", 
        CLASS_NAME : "TestActivity",
        LAYOUT_CLASS_NAME : "test_activity",
        TYPE : "test",
        PACKAGE_DETAIL : "",
        OBJECT : "",
        }

template_list = []

conf_file_name = r"./android-scaffolding.conf"
default_conf_file_name = r"./Android-Scaffolding/android-scaffolding.conf"
project_dir_name = r"./Android-Scaffolding/"


def parse_string(line):
    for k in values.keys():
        if line.find(k) != -1:
            if (k == PACKAGE and line.startswith("package")):
                line = line.replace(k, values[k])
                line = line.replace(";", "." + values[PACKAGE_DETAIL] + ";")
            elif (k == CLASS_NAME):
                line = line.replace(k, get_class_name())
            else:
                line = line.replace(k, values[k])
    return line

def get_class_name():
    class_name = values[CLASS_NAME]
    name_substrings = get_camel_case_substrings(class_name)
    if (name_substrings[-1] == values[OBJECT]):
        return class_name 
    else:
        name_substrings[-1] = values[OBJECT] 
        string = ""
        for t in name_substrings:
            tl = list(t)
            tl[0] = tl[0].upper()
            string += "".join(tl)
        return string 

def copy_java_file(in_file_path, out_file_path, package_name):

    split_out_path = out_file_path.split("/")
    split_out_path.insert(len(split_out_path) - 1, package_name)
    new_out_path = ""
    for d in split_out_path[:-1]:
        new_out_path += d + "/"

    if (not os.path.exists(in_file_path)):
        in_file_path = project_dir_name + in_file_path 

    if (not os.path.exists(new_out_path)):
        os.makedirs(new_out_path)

    new_out_path += get_new_file_name(split_out_path[-1], values[OBJECT])
    out_file_path = new_out_path
    values[PACKAGE_DETAIL] = package_name
    try:
        in_file = open(in_file_path)
        out_file = open(out_file_path, "w")
        
        for line in in_file:
            out_file.write(parse_string(line))

        in_file.close()
        out_file.close()
        print "      create :: " + out_file_path
    except: 
        print "Something went wrong... ", sys.exc_info()[1]

def get_new_file_name(in_file_name, package_name):
    in_file_name = in_file_name.replace(".java","")
    name_substrings = get_camel_case_substrings(in_file_name)
    if (name_substrings[-1] == package_name):
        return in_file_name
    else:
        name_substrings.insert(len(name_substrings), package_name)
        string = ""
        for t in name_substrings:
            tl = list(t)
            tl[0] = tl[0].upper()
            string += "".join(tl)
        return string + ".java"



def copy_file(in_file_path, out_file_path):
    if (not os.path.exists(in_file_path)):
        in_file_path = project_dir_name + in_file_path
    try:
        in_file = open(in_file_path)
        out_file = open(out_file_path, "w")
        
        for line in in_file:
            out_file.write(line)

        in_file.close()
        out_file.close()
        print "      create :: " + out_file_path
    except: 
        print "Something went wrong... ", sys.exc_info()[1]
    
def usage():
    print "android-generator -- usage: \n" + \
          "    android-generator <template type> <class name> [<layout name>]" 
    print_template_types()

def print_template_types():
    global template_list
    if (template_list == None or len(template_list) == 0):
        get_template_list()
    print "    Possible template types: "
    for key in template_list.keys():
        print "        " + key

def get_template_list():
    in_str = ""
    global template_list
    try: 
        f = None
        if (os.path.exists(r"./template.list")):
            f = open(r"./template.list", "r")
        elif (os.path.exists(project_dir_name + "template.list")):
            f = open(project_dir_name + "template.list", "r")
        in_str = f.read().replace("\n","")
        f.close()
    except:
        print "Could not open the template list"

    template_list = json.loads(in_str)

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
        if (len(param) < 2):
            continue
        if (param[0] == "PACKAGE"):
            values[PACKAGE] = param[1].replace("\n","")
        else: 
            values[param[0]] = param[1].replace("\n","")

def set_parameters(argv):
    values[TYPE] = argv[0]
    values[CLASS_NAME] = argv[1]
    if (len(argv) > 2):
        values[LAYOUT_CLASS_NAME] = argv[2]
    else:
        values[LAYOUT_CLASS_NAME] = infer_layout_name()

def infer_layout_name():
    """Infer the layout name based on the class name, convention is 
    blah_blah_layout.xml
    """
    class_name = values[CLASS_NAME]
    name_substrings = get_camel_case_substrings(class_name)
    layout_name = ""
    length = len(name_substrings) - 1 if name_substrings[-1].lower() == values[OBJECT] else len(name_substrings)
    print length
    for i in range(0, length):
        if (i == 0):
            layout_name = name_substrings[i].lower()
        else:
            layout_name += "_" + name_substrings[i].lower()
    layout_name += "_layout"
    return layout_name

def get_camel_case_substrings(string):
    return re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z]))', ' ', string).strip().split(" ")


def generate_files():
    template_item = None
    for key in template_list.keys():
        if (values[TYPE] == key):
            template_item = template_list[key]
            break 

    if (template_item == None):
        print "ERROR :: Could not find the template item"
        usage()
        return

    for item in template_item:
        out = ""
        if (item["object"] == "manifest"):
            update_manifest()
        elif (item["type"] == "java"): 
            out = r"./" + item["out"] + values[PACKAGE].replace(".", "/") + "/" + values[CLASS_NAME] + "." + item["type"]
            values[OBJECT] = item["object"]
            copy_java_file(r"./templates/"+item["in"], out, item["package"])
        elif (item["object"] == "layout"):
            if (values.get(LAYOUT_CLASS_NAME) != None):
                out = r"./" + item["out"] + values[LAYOUT_CLASS_NAME] + "." + item["type"]
            else:
                out = r"./" + item["out"] + item["default"] + "." + item["type"]
                print "ERROR :: missing layout file name, using template default"
            copy_file(r"./templates/"+item["in"], out)
        else: 
            out = r"./" + item["out"] + values[CLASS_NAME] + "." + item["type"]
            copy_file(r"./templates/"+item["in"], out)

def update_manifest(): 
     handler = ManifestDomHandler("AndroidManifest.xml")
     handler.add_activity_node(values[CLASS_NAME])
     print "    Manifest :: Added " + values[CLASS_NAME]

def setup():
    global project_dir_name 
    path = os.path.realpath(__file__)
    split_path = path.split('/')
    project_dir_name = path.replace(split_path[len(split_path) - 1], "",)
    default_conf_file_name = project_dir_name + "android-scaffolding.conf"

    handler = ManifestDomHandler("AndroidManifest.xml")
    values[PACKAGE] = handler.get_package_name()


def main(argv):
    setup()
    if (len(argv) < 2):
        usage()
        sys.exit(2)
   
    set_parameters(argv)
    get_template_list()
    
    generate_files()

if __name__ == "__main__":
    main(sys.argv[1:])

