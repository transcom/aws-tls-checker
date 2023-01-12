#!/usr/bin/env bash

file_prefix="lambda_check_ssl-v"

# ask user to input a version number
echo "Enter a version number to build: "
read -r version

# make a directory with the version number
mkdir "$version"

# copy the source files from the src directory to the new directory
cp -r src/* "$version"/

# change into the new directory
cd "$version" || exit

# create a python environment in the directory
python3 -m venv env

# activate the python environment
source env/bin/activate

# install the requirements from the requirements.txt file
pip install -r requirements.txt -t ./

# deactivate the python environment
deactivate

# remove the bin and lib folders created by the python environment
rm -rf env

# archive all files in the new directory to a zip file
zip -q -r "../$file_prefix$version.zip" .

# remove the new directory
cd ..
rm -rf "$version"

echo ""
echo "Finished building, release file is: $file_prefix$version.zip"
