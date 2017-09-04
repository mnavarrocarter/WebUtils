Rush
====

A CLI tool written in pyhton for rushing web developers.

Download the latest .deb package [here](https://github.com/mnavarrocarter/rush/raw/master/dist/rush_latest_all.deb).

## Usage

This is an application in active development. No stable release has been 
published yet, so API is still undocumented.

## For Developers

To create a dev environment you need python-pip and virtualenv. 

1. Pip: `sudo install python-pip`

2. Virtualenv: `sudo pip install virtualenv`

Once you have the required packages, then you can clone the repo and 
configure your python virtual environment.

    git clone https://github.com/mnavarrocarter/rush.git Rush
    cd Rush
    virtualenv venv
    . venv/bin/activate
    pip install --editable .

Just that and you're good to go for development. Remember when you're done
to execute `deactivate`.

You can build the debian package running `./build.sh`. You will need the
following packages: 

1. `sudo apt-get install devscripts build-essential lintian`
