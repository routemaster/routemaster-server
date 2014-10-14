from fabric.api import *

deps = "less nginx python3-pip tree uwsgi-plugin-python3"
files = "debug-server.py routemaster server.wsgi setup.py".split()
env.user = "root"
env.hosts = ["routemaster.lumeh.org"]

def deploy():
    # Install dependencies
    run("apt-get --quiet --quiet update")
    run("apt-get --quiet --yes install %s" % deps)

    # Create rmserver user and homedir
    with settings(warn_only=True):
        run("useradd --system --create-home --user-group rmserver")

    # Copy and install routemaster package
    run("rm -rf /home/rmserver/routemaster")
    run("mkdir /home/rmserver/routemaster")
    for file in files:
        put(file, "/home/rmserver/routemaster/")
    with cd("/home/rmserver/routemaster"):
        run("pip3 uninstall --quiet --yes rm-server")
        run("pip3 install --quiet .")

    # Copy configurations
    put("etc/routemaster-server.conf", "/etc/init/routemaster-server.conf")
    put("etc/nginx.conf", "/etc/nginx/sites-enabled/routemaster")

    # Restart services
    run("service nginx restart")
    with settings(warn_only=True):
        run("service routemaster-server stop")
    run("service routemaster-server start")
