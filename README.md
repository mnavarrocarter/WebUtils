WebUtils: CLI utility for Web Developers
========================================
A python cli tool with utilities for web developers in Debian derivatives.

Download the latest .deb package [here](https://github.com/mnavarrocarter/WebUtils/raw/master/dist/webutils_latest_all.deb).

## Usage

`webutils` will list all the available commands. At the minute only the
`apache` group is available. You can check the commands with `webutils apache`.

For example, to make a virtual host:

1. `cd` into the directory you want to serve files from

2. Then execute `webutils apache vhost:new yourfakename.dev --here`. If you
are creating a virtual host for a laravel app, you can use the `--laravel`
flag too (but remember, you have to be in the )

3. Then you have to make sure apache has the proper permissions for the folder
where you created the virtual host, so run `sudo webutils apache perm:set` 
in that directory. You can also use the `--laravel` flag here.

4. In order to have write/read access to your files, run `webutils apache user:add`
to add your user to the www-data group.

## "Build" for Development

### Requirements:

1. Pip: `sudo install python-pip`

2. Virtualenv: `sudo pip install virtualenv`

### Instalation 

    git clone https://github.com/mnavarrocarter/WebUtils.git WebUtils
    cd WebUtils
    virtualenv venv
    . venv/bin/activate
    pip install --editable .

Just that and you're good to go for development. Remember when you're done
to execute `deactivate`.