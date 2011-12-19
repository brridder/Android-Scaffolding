# Installation

To install this project:

1. Clone the project into your workspace.
    
    `git clone git@github.com:brridder/Android-Scaffolding.git`

2. Add the `bin` directory to your path in your bash rc.


# Usage

Once added to the path, usage is:

    android-generator <template> <class_name> [<layout_name>]

To see a list of available templates, run the script without any parameters.

Currently, the package name is grabbed from the android manifest file. Eventually, the package name will be modified
based on the template provided.
