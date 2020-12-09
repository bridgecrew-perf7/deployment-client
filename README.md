Deployment Client

#########################################
###       MUST RUN ON CENTOS7         ###
#########################################

##Setup
Have a VM setup (either using LXD or Vagrant and expose port 8003 )
Inside thew VM, do the following:
1  cp /vagrant/files/setup_dclient.sh ~
2 sudo ~/setup_dclient.sh

That's it



#Running Unit Tests
When running the unit tests, it sets the env variable: TESTING to 1
TESTING env variable is required and is set so that it does not try to make any API request to the deployment-api,
and the app can be mocked

To run the unit tests:
`pipenv install -e .`
`TESTING=1 pytest tests/unit_tests`
