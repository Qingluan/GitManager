#!/usr/bin/env python3
import sys,os, subprocess,argparse, json
from qlib.log import LogControl as L
from Hacker.libs.networklib import Analyze

DOC ="""
this is a script to create git project in remote's server.
can supported gitlab, gitosc , github.
"""


L.LOG_LEVEL = L.OK
# create project's template data
data_tm = """{
    "project[import_url]": "*None*",
    "project[path]":"%s"
}"""

github_data_tm = """{
    "input": "*None*",
    "owner": "%s",
    "repository[auto_init]": "0",
    "repository[public]": "true",
    "repository[name]":"%s",
    "repository[description]":"%s",
    "repository[public]":"true",
    "repository[auto_init]":"0"
}"""

user_data = """{
    "user[login]": "%s",
    "user[password]": "%s"
}"""

github_data = """{
    "login":"%s",
    "password":"%s"
}"""


def args():
    parser = argparse.ArgumentParser(usage=" how to use this", description=DOC)
    parser.add_argument("-H", "--git-host", default="localhost:2333", help='set git\'s host. every git web site except no picture verify. ')
    parser.add_argument("-c", "--create-project", default=None, help='create project.')
    parser.add_argument("-l", "--create-project-link", default="/projects/new", help='create project.')
    parser.add_argument("-u", "--user", default=None, help='git user\'s  username.')
    parser.add_argument("-p", "--passwd", default=None, help='git user\'s  password.')
    parser.add_argument("-S", "--Sync", default=False,action='store_true', help='Synchrouns mode.')
    parser.add_argument("-G", "--Github", default=False,action='store_true', help='use github.com as host. default is "False"')
    parser.add_argument("-o", "--origin-name", default="origin", help='set origin\' name. default is "origin"')
    parser.add_argument("-ou", "--origin-url", default=None, help='set origin\' url name.')
    return parser.parse_args()


def init(host,link, user_data={}, github=False):
    if github:
        return Analyze("https://github.com/login").login("s",**user_data).Go("/new")    
    return Analyze(host).login("sign",**user_data).Go(link)

def create(name, project_web, github=False, user=None):
    data = data_tm
    data = json.loads(data % name)
    if github:
        data = github_data_tm
        data =  json.loads(data % (user, name, "this is a project name" + name))

    
    if github:
        res = project_web.post("rep", **data)
        return res("meta",property='og:url')[0]['content'] + '.git'
    res = project_web.post("project", **data)
    for i in res.text().split("\n"):
        if i.startswith("git") and "remote add" in i:
            return i.strip().split().pop()

def synchronization(dir, origin_name, uri=None, github=False):
    L.ok("info:", origin_name,uri)
    if uri != None :
        cmd = "cd " +dir+ " && git init ; git remote add " + origin_name+ " " + uri
        code, info = subprocess.getstatusoutput(cmd)
        if code != 0:
            L.err(info)
            L.info("add origin ", origin_name,uri)

        
    cmd = "cd " +dir+ " && git add -A && git commit -m 'synchronization' "
    code, info = subprocess.getstatusoutput(cmd)
    if code != 0:
        L.err(info)
    
    cmd = "cd " +dir+ " && git push " + origin_name + " master -u"
    code, info = subprocess.getstatusoutput(cmd)
    if code != 0:
        L.err(info)
        return 
    if uri != None:
        L.ok("create " + dir)
    else:
        L.ok("Sync " + dir)
    return True


def main():
    ag =  args()
    user = json.loads(user_data % (ag.user, ag.passwd))
    if ag.Github:
        user = json.loads(github_data % (ag.user, ag.passwd))

    project_web = init(ag.git_host, ag.create_project_link, user_data=user, github=ag.Github)
    if ag.create_project:
        if ag.Sync:
            synchronization(ag.create_project, ag.origin_name)
        elif os.path.isdir(ag.create_project):
            if ag.origin_url:
                synchronization(ag.create_project, ag.origin_name, ag.origin_url, github=ag.Github, user=ag.user)
            else:
                remote_uri = create(ag.create_project.split("/").pop(), project_web,github=ag.Github, user=ag.user)
                synchronization(ag.create_project, ag.origin_name, remote_uri,github=ag.Github)
        else:
            L.err("no such project dir.", ag.create_project)

if __name__ == '__main__':
    main()
