import click
import os
import re

# This config object will be created and instanciated so we can share 
# global parameters and options to share with the other groups of 
# applications.
class Config(object):
    def __init__(self):
        # We define the properties here
        self.verbose = False

# We define a pass_config variable, so we pass the config.
pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--verbose', help="Enables verbose mode", is_flag="True")
@pass_config
def cli(config, verbose):
    """
    Rush by Matias Navarro Carter
    
    Version: 0.3-beta

    This cli tool contains some useful commands for web development.

    If you happen to have a copy of this, consider yourself lucky.

    Use carefully. This is not a stable release.

    You can suggest improvements or report bugs at: https://github.com/mnavarrocarter/rush/issues
    """
    config.verbose = verbose

###########################################################################
# RUSH->NEWVHOST
###########################################################################
@cli.command('vhost:make', short_help='Creates a new Apache2 Virtual Host in your current directory.')

@click.argument('name')

@click.option('--laravel', is_flag="True", 
    help="Adds /public to the DocumentRoot.")

@pass_config
def vhostmake(config, name, laravel):
    """
    This command creates a new Apache2 Virtual Host in the current directory

    Providing a name, it will create *.vhost-conf file in your Apache2/sites-available directory. 
    We recommend the name to be something.dev like. Dev is a good top-level
    fake domain name to use for your development projects.

    Then, it will create a record in your /etc/hosts file so your fake domain
    name can be resolvable in your browser.

    Lastly, it will create the error and access logs in your project 
    directory. Make sure not to include these in your version control.

    This command requires sudo privileges.
    """
    if os.getuid() != 0:
        click.echo('You need superpowers to run this thing!')
        quit()

    if '.dev' not in name:
        if click.confirm('Do you want to add .dev to the name of your vHost? (recommended)'):
            name = name + '.dev'

    if here:
        path = os.getcwd()
        if config.verbose:
            click.echo("Setting DocumentRoot to %s..." % path)
    else:
        path = '/var/www/' + name
        if config.verbose:
            click.echo("Setting DocumentRoot to %s..." % path )
        if not os.path.exists('%s' % path):
            os.system('sudo mkdir %s -m 775' % path)

    if laravel:
        laravel = '/public'
        if config.verbose:
            click.echo('Adding /public to the DocumentRoot for Laravel...')
    else:
        laravel = ''
    
    if config.verbose:
        click.echo('Creating the .conf file...')
    
    out = """<VirtualHost %s:80>
    DocumentRoot %s%s
    ServerName %s
    <Directory %s%s>
        Options -Indexes +FollowSymLinks +MultiViews
        AllowOverride All
        Order allow,deny
        Allow from all
        Require all granted
    </Directory>
    ErrorLog %s/logs/error.log
    CustomLog %s/logs/access.log combined
</VirtualHost>
""" % (name, path, laravel, name, path, laravel, path, path)

    if os.path.exists('/etc/apache2/sites-available/%s.conf' % name):
        click.echo('Virtualhost already exists! Aborting...')
        quit()

    if config.verbose:
        click.echo('Creating log files...')
    
    if not os.path.exists('%s/logs' % path):
        os.system('mkdir %s/logs' % path)
    os.system('touch %s/logs/error.log' % path)
    os.system('touch %s/logs/access.log' % path)
    os.system('chown 777 -R %s/logs/' %path)

    os.system('sudo echo -e "%s" >> /etc/apache2/sites-available/%s.conf' % (out, name))

    src = '/etc/apache2/sites-available/%s.conf' % name
    link = '/etc/apache2/sites-enabled/%s.conf' % name
    os.system('sudo ln -s %s %s' % (src, link))
    
    if config.verbose:
        click.echo('Modifying the hosts file...')
    os.system('sudo echo -e "\n127.0.0.1 %s" >> /etc/hosts' % name)

    if config.verbose:
        click.echo('Reloading Apache...')
    os.system('sudo service apache2 reload')

    click.echo('Done! Now you can visit http://%s in your browser!' % name)

###########################################################################
# RUSH->VHOST:DESTROY
###########################################################################
@cli.command('vhost:destroy', short_help='Destroys the given Apache2 Virtual Host.')

@click.argument('name')

@pass_config
def vhostmake(config, name):
    """
    This command destroys the given Apache2 VirtualHost. 

    This will delete the *.conf files associated with this vitualhost, as
    well as the /etc/hosts file entry, and restart Apache.

    This command requires sudo privileges.
    """
    if os.getuid() != 0:
        click.echo('You need superpowers to run this thing!')
        quit()

    os.system('rm /etc/apache2/sites-enabled/%s.conf' % name)
    os.system('rm /etc/apache2/sites-available/%s.conf' % name)

    readFile = open('/etc/hosts')
    lines = readFile.readlines()
    readFile.close()
    for key,value in lines.items():
        if name in value:
            del lines[key]
    writeFile = open('/etc/hosts', 'w')
    writeFile.writelines(lines)
    writeFile.close()
    click.echo('Done!')

###########################################################################
# RUSH->VHOST:DEACTIVATE
###########################################################################


###########################################################################
# RUSH->VHOST:ACTIVATE
###########################################################################


###########################################################################
# RUSH->USER:CHANGE
###########################################################################
@cli.command('apacheuser:change', short_help='Sets the Apache user to the selected user.')

@click.argument('user')

@pass_config
def userchange(config, user):
    """
    This command sets the Apache user to the selected user. It requires sudo
    privileges.

    What this does is that changes apache envvars file, APACHE_RUN_USER and
    APACHE_RUN_GROUP entries, and replaces www-data for your username.

    If you want to return to the original config, just run this command again
    using www-data for the user name.
    """
    if os.getuid() != 0:
        click.echo('You need superpowers to run this thing!')
        quit()
    
    readFile = open('/etc/apache2/envvars')
    lines = readFile.readlines()
    readFile.close()
    lines[15] = "export APACHE_RUN_USER %s\n" % user
    lines[16] = "export APACHE_RUN_GROUP %s\n" % user
    w = open('/etc/apache2/envvars', 'w')
    w.writelines(lines)
    w.close()

###########################################################################
# RUSH->USER:RESTORE
###########################################################################
@cli.command('apacheuser:restore', short_help='Restores the Apache user to the www-data.')

@click.option('--no-backup', is_flag=True, help='Leaves no backup of the Apache old config.')

@pass_config
def userchange(config, no_backup):
    click.echo('Is indented dumb!')