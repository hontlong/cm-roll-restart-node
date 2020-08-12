#!/usr/bin/env python
# coding=utf8

# usage: 修改如下参数

user   = "admin"
passwd = "admin"
host   = "cnode01"
port   = 7180

clusterName = "cluster"

#service= "hdfs"
#role   = "datanode"

service= "yarn"
role   = "nodemanager"

#service= "solr"
#role   = "SOLR_SERVER"

#service= "zookeeper"
#role   = "server"

#service= "hbase"
#role   = "regionserver"

#host_reg = r"hadoop[5-8]" # host的匹配正在，如果配置，只有匹配到host才执行
#                        # 注意前面的r代表raw字符串，修改需要明白其含义
#host_reg = r"hadoop(43[1-4]|5\d+|45[7-9]|46\d)" # host的匹配正在，如果配置，只有匹配到host才执行
#host_reg = r"cnode(73[13459]|76[0245])" # host的匹配正在，如果配置，只有匹配到host才执行
#host_reg = r"cnode(7[1-6][0-9])" # host的匹配正在，如果配置，只有匹配到host才执行
#host_reg = r"cnode(7[1-3][0-9])" # host的匹配正在，如果配置，只有匹配到host才执行
#host_reg = r"cnode(78[0-9])" # host的匹配正在，如果配置，只有匹配到host才执行
#host_reg = r"wx-ucgc.*" # host的匹配正在，如果配置，只有匹配到host才执行
host_reg = r"cnode741|cnode769" # host的匹配正在，如果配置，只有匹配到host才执行
#host_reg = r"cnode8\d\d" # host的匹配正在，如果配置，只有匹配到host才执行
#host_reg = r".*" # host的匹配正在，如果配置，只有匹配到host才执行
just_show_host = False # 仅显示选中要执行的机器Host, 不实际执行
#just_show_host = True # 仅显示选中要执行的机器Host, 不实际执行

interval = 15 * 60 # seconds， 两台机器的时间间隔

# restart-all = True # 重启全部, 即便一个role之前是关闭的
restart_all = False

##############################
role = role.upper()
import urllib
passwd=urllib.quote_plus(passwd,safe='')
clusterName=urllib.quote(clusterName,safe='')
##############################

if __name__ == "main":
    import sys
    sys.exit(1)
