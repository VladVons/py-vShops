#!/bin/bash
# Created: 2022.10.15
# Vladimir Vons, VladVons@gmail.com


Install() 
{
    pip3 install pylint
}

Check()
{
    File="pylint_err.log"

    #Ignore="C0103|C0114|C0115|C0116|C0209|C0325|C0301|R0903|R0914"

IgnoreErr="\
invalid-name|\
missing-function-docstring|\
missing-module-docstring|\
missing-class-docstring|\
too-few-public-methods|\
too-many-arguments|\
too-many-locals|\
too-many-instance-attributes|\
too-many-public-methods|\
too-many-branches|\
too-many-nested-blocks|\
line-too-long|\
superfluous-parens|\
consider-using-f-string\
"
    echo "Creating $File ..."
    #time pylint --recursive=y ./src > $File
    time pylint --recursive=y ./src | egrep -v $IgnoreErr > $File
}


#Install
Check

