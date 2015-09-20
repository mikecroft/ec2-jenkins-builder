#!/usr/bin/python3

import boto3.ec2
import configparser
import json
import urllib
import jenkins


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



def buildJob(jobName):
    svr = jenkins.Jenkins('http://' + jenkinsIP + ':8080')
    print(svr.build_job(jobName))
    print(svr.get_job_config(jobName))







startInstance('i-f5095b58')
while (!(isServiceUp('http://' + jenkinsIP + ':8080'))):
    time.sleep(2)

buildJob('Payara')


#stopInstance('i-f5095b58')


