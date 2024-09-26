#!/bin/bash
# Created: 2023.12.08
# Vladimir Vons, VladVons@gmail.com

py=python3.12


VSCode()
{
    code --list-extensions

    code --force --install-extension ms-python.python
    code --force --install-extension ms-python.pylint
    code --force --install-extension sonarsource.sonarlint-vscode
    code --force --install-extension tabnine.tabnine-vscode
    code --force --install-extension shardulm94.trailing-spaces
    #code --force --install-extension fallenmax.mithril-emmet
    code --force --install-extension anteprimorac.html-end-tag-labels
    code --force --install-extension naumovs.color-highlight
}

Python()
{
    sudo apt update
    sudo apt dist-upgrade

    sudo apt install --no-install-recommends software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install --no-install-recommends $py $py-dev $py-distutils $py-venv virtualenv

    sudo apt install postgresql-plpython3-16
    su postgres -c "python3 -m pip install geoip2"
    service postgresql restart
}

PythonPkg()
{
    Dir=~/virt/$py

    $py -m venv $Dir
    source $Dir/bin/activate

    pip3 install --upgrade pip
    pip3 install --requirement requires.lst
}

VSCode

#Python
#PythonPkg
