#!/usr/bin/python3

import boto3.ec2
import configparser
import json
import urllib
import jenkins
import xml.etree.ElementTree as ET

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
#    print(svr.build_job(jobName))
    config = svr.get_job_config(jobName)
    defineBuild(config, brName, goals)


def defineBuild(config, brName, goals):
    # maven2-modulset >> scm >> branches >> hudson.plugins.git.BranchSpec >> name
    root = ET.fromstring(config)
    branch = root.find('scm/branches/hudson.plugins.git.BranchSpec/name')
    g = root.find('goals')
    print('goals = ' + g.text)
    print('branch name = ' +  branch.text  )



startInstance('i-f5095b58')
while (not (isServiceUp('http://' + jenkinsIP + ':8080'))):
    time.sleep(2)

buildJob('Payara')


#stopInstance('i-f5095b58')


