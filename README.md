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

##Running Unit Tests
Have your env_file and config file in place

When running the unit tests, set the env variable: TESTING to 1

TESTING env variable is required and is set so that it does not try to make any API request to the deployment-proxy,
and the app can be mocked

To run the unit tests:
Change the env_file(.env or /etc/default/dclient) value for TESTING to 1.
If TESTING=0:
     - ##It will not run the tests
     - ## It will run the application
If TESTING=1:
    - ##It will run the tests
    - ## It will not run the application as expected
`pipenv install -e .`
`pytest tests/unit_tests`!
