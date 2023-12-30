#!/bin/bash

File="filemanager.j2"
#File="product.j2"

#tidy -wrap 0 -ashtml -indent --indent-spaces 2 --show-body-only yes -o $File.new $File
html-beautify -s 2 --outfile $File.new $File
