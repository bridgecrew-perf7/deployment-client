#!/bin/bash

mode=$1

#set up services
yum -y install epel-release
yum -y install perl python3 python-pip
yum -y install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
yum -y install yum-plugin-versionlock

#Overwrite /etc/pip.conf
cat > /etc/pip.conf <<-EOM
[global] 
index-url = https://pypi.unifiedlayer.com/root/stable/ 

[search] 
index = https://pypi.unifiedlayer.com/root/stable/
EOM

#Add custom.repo
cat > /etc/yum.repos.d/custom.repo <<-EOM
[Alpha]
name=Alpha
baseurl=http://mirrors.unifiedlayer.com/alpha/centos$releasever
gpgkey=http://mirrors.unifiedlayer.com/alpha/RPM-GPG-KEY-Alpha
enabled=0
gpgcheck=1
timeout=5
EOM

hostnamectl set-hostname deployment-client.com

printf "$(hostname -I) $HOSTNAME" >> /etc/hosts

username="hp_deploy"

#Create hp_deploy user
if [ $(id -u) -eq 0 ]; then
	password=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
	egrep "^$username" /etc/passwd >/dev/null
	if [ $? -eq 0 ]; then
		echo "$username exists!"
	else
		echo "Creating hp_deploy user"
		pass=$(perl -e 'print crypt($ARGV[0], "password")' $password)
		useradd -m -G wheel -d /opt/deployment -p "$pass" "$username"
		[ $? -eq 0 ] && echo "User has been added to system!" || echo "Failed to add a user!"
		sudoer_string="hp_deploy ALL=(ALL) NOPASSWD: /bin/yum, /var/hp/common/bin/buildall"
		if echo /etc/sudoers | grep -q "hp_deploy"
		then
			echo "Sudoers file already modified"
		else
			echo "hp_deploy ALL=(ALL) NOPASSWD: /bin/yum, /var/hp/common/bin/buildall" >> /etc/sudoers
		fi
		
		echo "hp_deploy ALL=(ALL) NOPASSWD: /bin/yum, /var/hp/common/bin/buildall" >> /etc/sudoers
		mkdir -p /var/log/deployment
		chown hp_deploy:hp_deploy -R /var/log/deployment
	fi
else
	echo "Only root may add a user to the system."
	exit 2
fi


environment="Alpha"

if [[ $mode == *"dev"* ]]
then
	if pip3 list | grep dclient
	then
		#Upgrade dclient
		pip3 install --upgrade dclient
	else
		#Install dclient
		pip3 install dclient
	fi
	environment="Alpha"
else
	echo "RPM install not implemented"
	#install dclient rpm
	#todo

fi

echo "Writing /usr/lib/systemd/system/dclient.service"
cat > /usr/lib/systemd/system/dclient.service <<- EOM
[Unit]
Description=Bluehost Deployment Client service
After=network.target

[Service]
User=$username
Group=$username
EnvironmentFile=/etc/default/dclient
RuntimeDirectory=dclient
WorkingDirectory=/opt/deployment/client
ExecStart=/usr/local/bin/gunicorn -b 0.0.0.0:8003 --log-level=INFO --workers=1 --timeout=90 'dclient.app:app'
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOM

mkdir -p /opt/deployment/client
chown $username:$username /opt/deployment/client

echo "Writing /etc/default/dclient"
cat > /etc/default/dclient <<- EOM
STATE=NEW
EOM

chown $username:$username /etc/default/dclient

mkdir -p /etc/deployment
chown $username:$username /etc/deployment/

echo "Writing /etc/deployment/dclient.conf"
cat > /etc/deployment/dclient.conf <<- EOM
# All values can be overwritten by using environment variables.
# default environment file /etc/default/dclient
# set environment file export ENV_FILE=
# default configuration file /etc/deployment/dclient.conf
# set configuration file export CONFIG_FILE=

# hostname to use for the deployment-proxy
# must be resolveable and reachable from the deployment-api and deployment-clients
DEPLOYMENT_CLIENT_HOSTNAME=www0.hp.provo1.endurancemb.com
DEPLOYMENT_CLIENT_IP=10.24.244.27
DEPLOYMENT_CLIENT_PROTOCOL=http
DEPLOYMENT_CLIENT_PORT=8003
DEPLOYMENT_CLIENT_VERSION=v1

# group or cluster this server belongs to
GROUP=hp_web

# environment this server belongs to
# Example: Alpha, Beta, Staging, Production
ENVIRONMENT=Alpha

# which datacenter is this server located in
LOCATION=Provo

# deployment-proxy hostname
DEPLOYMENT_PROXY_HOSTNAME=deploy-proxy.hp.provo1.endurancemb.com
# running on port 8002
DEPLOYMENT_PROXY_PORT=8002
# deployment proxy protocol (http/https)
DEPLOYMENT_PROXY_PROTOCOL=http
# api version v1
DEPLOYMENT_PROXY_VERSION=v1

# the environment file to load environment variables from.
# default /etc/default/dclient
ENV_FILE=/etc/default/dclient

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
DEFAULT_TIMEOUT=30
# default log file name

# LOG CONFIGURATION
# set log level
LOG_LEVEL=INFO
# set log file
LOG_FILE=/var/log/deployment/dclient.log
# max file size before roll
LOG_MAX_BYTES=1000000
# number of previous logs to retain
LOG_BACKUP_COUNT=10
EOM

chown $username:$username /etc/deployment/dclient.conf

if systemctl is-active --quiet service
then
	echo "Existing service running. Refreshing and restarting"
	systemctl daemon-reload
	systemctl restart dclient
else
	echo "Enabling and Starting the service"
	systemctl enable dclient
	systemctl status dclient
	systemctl start dclient
fi
 

# Initial setup performed by dclient bootstrap

