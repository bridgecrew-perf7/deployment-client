Deployment Client

#########################################
###       MUST RUN ON CENTOS7         ###
#########################################

##Setup
Have a VM setup (either using LXD or Vagrant and expose port 8003 )
Inside thew VM, do the following:
1  yum install python3 -y
2  useradd deployment -G wheel -d /opt/deployment -m
3  mkdir  /var/log/deployment/
4  chown deployment:deployment -R /var/log/deployment/
5  vi /etc/pip.conf >>>

[global]
index-url = https://pypi.unifiedlayer.com/root/stable/

[search]
index = https://pypi.unifiedlayer.com/root/stable/


6  vi /etc/hosts >>> 
           <host system IP address> <deployment proxy hostname >
           Example: 192.168.0.232 deployment-proxy.unifiedlayer.com

7  Install dclient from pypi:
       ` pip3 install dclient`
   If already Installed, Upgrade the dclient package to the latest version:
        `pip3 install --upgrade dclient`

8  cp /vagrant/files/dclient.service /usr/lib/systemd/system/
9  vi /usr/lib/systemd/system/dclient.service. >>> Change User and Group to deployment
10  mkdir /opt/deployment/client
11  chown deployment:deployment /opt/deployment/client/
12  cp /vagrant/files/dev /etc/default/dclient
13  vi /etc/default/dclient >>>

    HOSTNAME=<VM's hostname> Example: deployment-client.com
    IP=<Host system IP> Example: 192.168.0.232
    STATE=NEW
    GROUP=hp_web
    ENVIRONMENT=PRODUCTION
    LOCATION=PROVO
    URL=<VM's URL> Example:http://deployment-client.com:8003
    DEPLOYMENT_PROXY=<Deployment Proxy Hostname> Example: deployment-proxy.unifiedlayer.com
    DEPLOYMENT_SERVER_URL=<Deployment Proxy's URL>Example: http://deployment-proxy.unifiedlayer.com:8002/api/1.0.0

14  chown deployment:deployment /etc/default/dclient
15  mkdir /etc/deployment
16  chown deployment:deployment /etc/deployment/
17  cp /vagrant/files/dclient.conf /etc/deployment/
18  chown deployment:deployment /etc/deployment/dclient.conf
19  vi /etc/deployment/dclient.conf >>>


# All values can be overwritten by using environment variables.
# default environment file /etc/default/dclient
# set environment file export ENV_FILE=
# default configuration file /etc/deployment/dclient.conf
# set configuration file export CONFIG_FILE=

# hostname to use for the deployment-proxy
# must be resolveable and reachable from the deployment-api and deployment-clients
HOSTNAME=<VM's Hostname>"deployment-client.com"
IP=<Host's IP>"192.168.0.232"

# api endpoint url for the deployment-proxy
# running on port 8002
# api version 1.0.0
DEPLOYMENT_PROXY="deployment-proxy.unifiedlayer.com"

# api endpoint url for the deployment-api
# running on port 443 behind nginx (port 8000)
# api version 1.0.0
DEPLOYMENT_API_URI="http://deployment-proxy.unifiedlayer.com:8002/api/1.0.0"

# the url endpoint for dclient
URL="http://deployment-client.com:8003"

# the environment file to load environment variables from.
# default /etc/default/dclient
ENV_FILE="/etc/default/dclient"

# HTTP HELPER
# number of times to retry requests
RETRY=10
# {backoff factor} * (2 ** ({number of total retries} - 1))
#For example, if the backoff factor is set to:
#1 second the successive sleeps will be 0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256.
#2 seconds - 1, 2, 4, 8, 16, 32, 64, 128, 256, 512
#10 seconds - 5, 10, 20, 40, 80, 160, 320, 640, 1280, 2560
BACKOFF_FACTOR=1
# the http status codes to retry
STATUS_FORCELIST=[429, 500, 502, 503, 504]
# the http methods to retry
METHOD_WHITELIST=["HEAD", "GET", "OPTIONS", "TRACE", "DELETE", "PUT", "PATCH", "POST"]
# default timeout in seconds
DEFAULT_TIMEOUT=3

20  systemctl enable dclient
21  systemctl status dclient
22  systemctl start dclient
   On making a change to service file, run `systemctl daemon-reload
