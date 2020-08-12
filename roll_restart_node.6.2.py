#!/usr/bin/env python
# coding=utf8

# usage: 修改如下参数

from config import *

import sys
import urllib
import urllib2
import urlparse
import json
import time

if host_reg:
  import re
  host_p = re.compile(host_reg, re.IGNORECASE)

# url: UrlParse
def build_opener(url):
  if not url.username:
    return urllib2.build_opener()
  #print "user:", url.username
  #print "pass:", url.password
  password=urllib.unquote(url.password)
  #print password

  passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
  #passman.add_password(None, "%s://%s:%d" % (url.scheme, url.hostname, url.port), url.username, url.password)
  passman.add_password(None, "%s://%s:%d" % (url.scheme, url.hostname, url.port), url.username, password)
  authhandler = urllib2.HTTPBasicAuthHandler(passman)
  opener = urllib2.build_opener(authhandler)
  return opener

def get(url):
  #print "get", url
  url = urlparse.urlparse(url)
  opener = build_opener(url)
  url = urlparse.urlunparse((url.scheme, "%s:%d" % (url.hostname, url.port), url.path, url.params, url.query, url.fragment))
  #print url
  f = opener.open(url)
  return f.read()

def post(url, data, headers):
  #print "post", url, data, headers
  url = urlparse.urlparse(url)
  opener = build_opener(url)
  url = urlparse.urlunparse((url.scheme, "%s:%d" % (url.hostname, url.port), url.path, url.params, url.query, url.fragment))
  req = urllib2.Request(url, data, headers)
  f = opener.open(req)
  return f.read()

def hostId2Hostname(hostId):
  #http://cnode756:7180/api/v10/hosts/60bb7200-a3e0-4315-9831-b9340210f8b1
  url = "%s/hosts/%s" % (API, hostId)
  host = get(url)
  host = json.loads(host)
  hostname = host['hostname']
  return hostname

def restart(name):
  #print "restart", name
  if 'hdfs-BALANCER' in name:
    url = "%s/clusters/%s/services/%s/roleCommands/start" % (API, clusterName, serviceName)
  else: 
    url = "%s/clusters/%s/services/%s/roleCommands/restart" % (API, clusterName, serviceName)
  data = "{\"items\":[\"%s\"]}" % name
  headers = {"Content-Type": "application/json"}
  rep = post(url, data, headers)
  rep = json.loads(rep)
  return rep['errors']

def info(name):
  #print "info", name
  url = "%s/clusters/%s/services/%s/roles/%s" % (API, clusterName, serviceName, name)
  rep = get(url)
  #print rep
  rep = json.loads(rep)
  return rep

url="http://%s:%s@%s:%d/api/version" % (user, passwd, host, port)
version = get(url)
API = "http://%s:%s@%s:%d/api/%s" % (user, passwd, host, port, version)

#url="%s/clusters" % API
#clusters = get(url)
#clusters = json.loads(clusters)
#clusterName = clusters['items'][0]['name']
#print clusterName
#clusterName = urllib.quote(clusterName)

url="%s/clusters/%s/services" % (API, clusterName)
services = get(url)
#print services
services = json.loads(services)
#serviceName = services['items'][0]['name']
#serviceName = "%s1" % service
serviceName = service
#####

url = "%s/clusters/%s/services/%s/roles" % (API, clusterName, serviceName)
#print url
roles = get(url)
#print roles
roles = json.loads(roles)
roleNames = {}


for item in roles['items']:
  if item['type'] != role: continue
  hostId = item['hostRef']['hostId']
  roleHost = hostId2Hostname(hostId)
  if host_reg:
    m = host_p.match(roleHost)
    if not m:
      print "INFO: %s not match host reg rule, skip it" % roleHost
      continue
  # 启动状态并且配置不过时，总是跳过
  if item['roleState'] == 'STARTED':
    if ('configStale' in item and not item['configStale']) or \
       ('configStalenessStatus' in item and item['configStalenessStatus'] == 'FRESH'):
      print "INFO: %s's config is not statle, skip it" % roleHost
      continue
  # 非启动状态，如果没有设定restart_all，跳过
  if item['roleState'] != 'STARTED':
    if not restart_all:
      print "INFO: %s is not started, forget it" % roleHost
      continue
  roleNames[roleHost]=item['name']


first = True
for khost, kname in roleNames.items():
  if just_show_host:
    print "%s@%s" % (kname,khost)
    continue
  if first:
    first = False
  else:
    print "Sleep ..."
    time.sleep(interval)

  print "restart", khost, kname
  expect_state='STARTED'
  if 'hdfs-BALANCER' in kname:
    expect_state='BUSY'

  errs = restart(kname)
  if errs:
    print "ERROR:", errs
    break
  for i in xrange(1, 100):
    time.sleep(3)
    krole = info(kname)
    state = krole['roleState']
    print "INFO:", khost, "state", state
    if state == expect_state: break
  if i == 100:
    print "ERROR:", "waiting restart timeout"
    break

  print "INFO:", "restart OK"
