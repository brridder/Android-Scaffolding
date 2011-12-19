# Installation

Currently, this project is to be used as a submodule

1. Clone the project as a submodule in the project directory.
    > git submodule init
    > git submodule add git@github.com:brridder/Android-Scaffolding.git
2. Copy the file "android-scaffolding.conf" to the root directory.
    > cp ./Android-Scaffolding/android-scaffolding.conf ./
3. Edit the conf file and change the package name to the root package of your project.

# Usage
Since this currently works as a submodule, to run this script you need to reference it in the submodule directory.
> ./Android-Scaffolding/android-generator.py <template> <class_name> [<layout_name>]


