import click
import os
import sys

# This config object will be created and instanciated so we can share 
# global parameters and options to share with the other groups of 
# applications.
class Config(object):
    def __init__(self):
        # We define the properties here
        self.verbose = False

# We define a pass_config variable, so we pass the config.
pass_config = click.make_pass_decorator(Config, ensure=True)

###########################################################################
# WEBUTILS
###########################################################################
@click.group()
@click.option('--verbose', help="Enables verbose mode", is_flag="True")
@pass_config
def cli(config, verbose):
    """
    WebUtils by Matias Navarro Carter
    
    Version: 1.1

    This program contains some useful tools for web development.

    If you happen to have a copy of this, consider yourself lucky.

    In this current version (1.1) we only have some apache utilities related
    to Virtual Hosts management.

    You can suggest improvements or report bugs at: https://github.com/mnavarrocarter/WebUtils/issues
    """
    config.verbose = verbose

###########################################################################
# WEBUTILS->APACHE
###########################################################################
@cli.group()
@pass_config
def apache(config):
    """Apache useful commands."""
    pass

###########################################################################
# WEBUTILS->APACHE->NEWVHOST
###########################################################################
@apache.command('vhost:new', short_help='Creates a new Apache2 Virtual Host.')

@click.argument('name')

@click.option('--here', is_flag="True", 
    help="Sets the DocumentRoot to your current working directory.")
@click.option('--laravel', is_flag="True", 
    help="Adds /public to the DocumentRoot.")

@pass_config
def newvhost(config, name, here, laravel):
    """
    This command creates a new Apache2 Virtual Host

    Providing a name, it will create *.vhost-conf file in your Apache2
    virtualhost directory. We recommend the name to be something.dev like.
    Dev is a good top-level fake domain name to use for your development
    projects.

    It will create a record in your /etc/hosts file so your fake domain
    name can be resolvable in your browser.

    This script will automatically create the DocumentRoot within your 
    /var/www/vhostname.dev directory. The --here flag will set the DocumentRoot to your
    current working directory, but keep in mind that Apache will need
    permissions to access that folder. Check 'webutils apache set_perm
    --help' for more info.

    This script will require sudo privileges.
    """
    if os.getuid() != 0:
        click.echo('You need superpowers to run this thing!')
        quit()

    if '.dev' not in name:
        if click.confirm('Do you want to add .dev to the name of your vHost? (recommended)'):
            name = name + '.dev'

    if here:
        path = os.getcwd()
        click.echo("Setting DocumentRoot to %s..." % path)
    else:
        path = '/var/www/' + name
        click.echo("Setting DocumentRoot to %s..." % path )
        if not os.path.exists('%s' % path):
            os.system('sudo mkdir %s -m 775' % path)

    if laravel:
        laravel = '/public'
        click.echo('Adding /public to the DocumentRoot for Laravel...')
    else:
        laravel = ''
    
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

    click.echo('Creating log files...')
    if not os.path.exists('%s/logs' % path):
        os.system('sudo mkdir %s/logs' % path)
    os.system('sudo touch %s/logs/error.log' % path)
    os.system('sudo touch %s/logs/access.log' % path)

    os.system('sudo echo -e "%s" >> /etc/apache2/sites-available/%s.conf' % (out, name))

    src = '/etc/apache2/sites-available/%s.conf' % name
    link = '/etc/apache2/sites-enabled/%s.conf' % name
    os.system('sudo ln -s %s %s' % (src, link))
    
    click.echo('Modifying the hosts file...')
    os.system('sudo echo -e "\n127.0.0.1 %s" >> /etc/hosts' % name)

    click.echo('Reloading Apache...')
    os.system('sudo service apache2 reload')

    click.echo('Done! Now you can visit http://%s in your browser!' % name)

###########################################################################
# WEBUTILS->APACHE->SETPERM
###########################################################################
@apache.command('perm:set', short_help='Sets special permissions for a directory.')

@click.argument('directory', default=os.getcwd())

@click.option('--apache-user', default='www-data',
    help='Overrides the default Apache User')
@click.option('--apache-group', default='www-data',
    help='Overrides the default Apache Group')
@click.option('--laravel', is_flag="True",
    help='Sets permissions for Laravel installations.')

@pass_config
def setperm(config, directory, apache_user, apache_group, laravel):
    """
    This command sets special Apache permissions for a directory.

    What this command does is that sets a directory's ownership to www-data
    user and group, so Apache can write there no matter what.
    
    If no directory is specified, then the current working directory
    is used.

    Keep in mind that you will no longer have access to that directory, because
    you are not the www-data user and you do not belong to the www-data group.
    The "webutils apache adduser" command will solve that for you, and will add your user
    to the www-data group so you can read and write those files.
    
    This command will also override your permissions in that folder,
    recursively, to 775 for folders and 664 for files.

    This command is intended to be used to give permissions to a Projects 
    folder of some sort in your home directory or alike, where you will
    have your web projects to be served.
    
    All this will require sudo privileges.
    """ 
    if os.getuid() != 0:
        click.echo('You need superpowers to run this thing!')
        quit()

    os.system('sudo chown -R ' + apache_user + ':' + apache_group + ' ' + directory)
    os.system('sudo find ' + directory + ' -type d -exec chmod 775 {} +')
    os.system('sudo find ' + directory + ' -type d -exec chmod ug+s {} +')
    os.system('sudo find ' + directory +' -type f -exec chmod 664 {} +')
    if laravel:
        os.system('sudo chmod -R 777 ' + directory + '/storage')
        os.system('sudo chmod -R 777 ' + directory + '/bootstrap/cache')
    click.echo('Permissions applied succesfully.')
    if laravel: click.echo('Laravel special config applied.')

###########################################################################
# WEBUTILS->APACHE->UNSETPERM
###########################################################################
@apache.command('perm:unset', short_help='Unsets special permissions for a directory.')

@click.argument('directory', default=os.getcwd())

@pass_config
def unsetperm(config, directory):
    """
    This command unsets special Apache permissions for a directory.

    It will leave all folders (755) and files (664) owned by your user.
    
    If no directory is specified, then the current working directory
    is used.
    
    All this will require sudo privileges.
    """
    if os.getuid() != 0:
        click.echo('You need superpowers to run this thing!')
        quit()

    os.system('sudo chown -R $USER:$USER ' + directory)
    os.system('sudo chmod -R 750 ' + directory)
    os.system('sudo find ' + directory +' -type f -exec chmod 660 {} +')
    click.echo('Permissions restored to default.')

###########################################################################
# WEBUTILS->APACHE->ADDUSER
###########################################################################
@apache.command('user:add', short_help='Adds the current user to the www-data group.')

@click.option('--apache-group', default='www-data',
    help='Overrides the default Apache Group')

@pass_config
def adduser(config, apache_group):
    """
    This command adds the current user to the www-data group.

    This will help you to still have access to your files while Apache controls
    them.

    You can use the --apache-group 
    """
    if os.getuid() == 0:
        click.echo('Run this as your user, duh!')
        quit()

    os.system('sudo adduser $USER ' + apache_group)

###########################################################################
# WEBUTILS->APACHE->REMUSER
###########################################################################
@apache.command('user:rem', short_help='Removes the current user from the www-data group.')

@click.option('--apache-group', default='www-data',
    help='Overrides the default Apache Group')

@pass_config
def remuser(config, apache_group):
    """
    This command removes the current user from the www-data group.

    You can use the --apache-group flag to override the www-data group.
    """ 
    if os.getuid() == 0:
        click.echo('Run this as your user, duh!')
        quit()

    os.system('sudo deluser $USER ' + apache_group)

###########################################################################
# WEBUTILS->GITHUB
###########################################################################