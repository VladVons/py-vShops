#!/bin/bash
# VladVons, 2023.11.19


cssDirDst="build/css"
jsDirDst="build/js"


cssPurge() {
    DirSrc="assets/css"

    mkdir -p $cssDirDst

    purgecss \
    --css $DirSrc/bootstrap.css $DirSrc/fontawesome.css \
    --content html/*.html \
    --output $cssDirDst
}

cssCombine()
{
    DirSrc="../assets/css"
    FileSrc="$DirSrc/styles.css"
    FileDst="$cssDirDst/styles.all.css"

    mkdir -p $cssDirDst

    echo > $FileDst
    grep -o '".*"' $FileSrc | sed 's/"//g' |\
    while read x; do
        echo $x
        echo -e "\n/* file: $x */" >> $FileDst
        cat $DirSrc/$x >> $FileDst
    done
}

jsCombine()
{
    FileSrc="../index.shtml"
    FileDst="$jsDirDst/app.all.js"

    mkdir -p $jsDirDst

    echo > $FileDst
    grep "<script" $FileSrc | grep -o '".*"' | grep -v "vendor" | sed 's/"//g' |\
    while read x; do
        echo $x
        echo -e "\n/* file: $x */" >> $FileDst
        cat ../$x >> $FileDst
    done
}




cssPurge
#cssCombine
#jsCombine
