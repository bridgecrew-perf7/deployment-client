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
13  Edit the env file as per your environment. Refer files: files/dev or files/prod for reference.
    `vi /etc/default/dclient`

14  chown deployment:deployment /etc/default/dclient
15  mkdir /etc/deployment
16  chown deployment:deployment /etc/deployment/
17  cp /vagrant/files/dclient.conf /etc/deployment/
18  chown deployment:deployment /etc/deployment/dclient.conf
19  Edit the config file as per your environment. Refer files: files/dclient.conf for reference.
    `vi /etc/deployment/dclient.conf`

20  systemctl enable dclient
21  systemctl status dclient
22  systemctl start dclient
On making a change to service file, run `systemctl daemon-reload
