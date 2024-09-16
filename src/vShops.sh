#!/bin/bash

py=python3.12
File=~/virt/$py/bin/activate
echo $File
source $File

#$py -V
$py -B vShops.py
