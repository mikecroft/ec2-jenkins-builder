#!/usr/bin/python3

import boto3.ec2
import configparser
import json
import urllib
import jenkins
import xml.etree.ElementTree as ET
import time

ec2 = boto3.resource('ec2')
jenkinsIP = '0.0.0.0'

def startInstance(instname):
    global jenkinsIP
    inst = ec2.Instance(instname)
    print(json.dumps(inst.start(), indent=4))
    jenkinsIP = inst.public_ip_address
    print(jenkinsIP)

def stopInstance(instname):
    inst = ec2.Instance(instname)
    print(json.dumps(inst.stop(), indent=4))

def isServiceUp(URL):
    conn = urllib.request.urlopen(URL)
    return (conn.getcode() == 200)



def buildJob(jobName, brName='master', goals='clean install'):
    svr = jenkins.Jenkins('http://' + jenkinsIP + ':8080')
    config = svr.get_job_config(jobName)
    svr.reconfig_job(jobName, defineBuild(config, brName, goals))
    print(svr.build_job(jobName))

    while (True):
        print(svr.get_jobs())
        time.sleep(10)


def defineBuild(config, brName, goals):
    # maven2-modulset >> scm >> branches >> hudson.plugins.git.BranchSpec >> name
    root = ET.fromstring(config)
    branch = root.find('scm/branches/hudson.plugins.git.BranchSpec/name')
    g = root.find('goals')
    print('goals = ' + g.text)
    g.text = goals
    print('branch name = ' +  branch.text  )
    branch.text = brName
    return ET.tostring(root, encoding='unicode', method='xml')



startInstance('i-f5095b58')
while (isServiceUp('http://' + jenkinsIP + ':8080')) != True:
    time.sleep(2)

buildJob('Payara', 'payara-4.1.153-maintenance', 'clean install -Dbuild.number=PythonAutoBuild-77')


#stopInstance('i-f5095b58')


