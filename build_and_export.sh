#!/bin/zsh

rm -rf "/Applications/Pymote.app"
rm -rf "build" "dist"
python3 setup.py py2app
cp -r "dist/roku_main.app" "/Applications/Pymote.app"

if [[ "$1" == -o ]]; then
    open "/Applications/Pymote.app"
fi


