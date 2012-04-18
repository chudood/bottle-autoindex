#!/usr/bin/env python
from bottle import route, run,view,template
from os.path import dirname
import os
import stat
import datetime
import time
import urllib
from operator import attrgetter
from settings import *
from local_settings import *


STATIC_LOCAL = os.path.abspath(STATIC_LOCAL)

FOLDER = "<tr><td width=100>%s</td><td width=100 >%s</td><td ><b><a href='%s'>%s</a></b></td></tr>"
FILE = "<tr><td width=100>%s</td><td width=100 >%s</td><td ><a href='%s'>%s</a></td></tr>"
FILE_PARAGRAPH = "<a href='%s'>%s</a><br>"

def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size

def get_size(start_path = '.'):
    """
    RETURNS SIZE OF FOLDER
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size


@route('/favicon.ico')
def favicon():
    return None

@route(subdir)
@route(subdir+'<sort_type>')
@route(subdir+'<sort_type>/')
@route(subdir+'<sort_type>/'+'<path:path>')
def index(sort_type='date',path=''):
    
    path = path.lstrip('/')
    if not path:
        path = ''

    joined_path = os.path.abspath(os.path.join(STATIC_LOCAL,path))+"/"

    if not os.path.abspath(joined_path).startswith(STATIC_LOCAL):
        return "ERROR: Incorrect path or path does not exist"
    joined_path = joined_path.rstrip('/')
    
    if not os.path.exists(joined_path):
        return "ERROR: Incorrect path or path does not exist"

    #ERROR CATCHING
    try:
        list_dir = [os.path.join(joined_path,f) for f in os.listdir(joined_path)]
    except OSError:
        return "OS_ERROR: Incorrect path or path does not exist"
    print list_dir
    folders =[]
    files = []
    for f in list_dir:

        s = os.stat(f)
        fd = {}
        fd['basename'] = os.path.basename(f)
        fd['path'] = f
        fd['relpath'] = subdir+sort_type+"/"+os.path.relpath(f,STATIC_LOCAL)  
        fd['mtime'] = s.st_mtime
        fd['date_mtime'] = datetime.datetime.fromtimestamp(s.st_mtime)
        fd['ctime'] = s.st_ctime
        fd['date_ctime'] = datetime.datetime.fromtimestamp(s.st_ctime)         
        if stat.S_ISDIR(s.st_mode):
           # fd['size'] = get_size(f)
            folders.append(fd)
        else:
            href = STATIC_URL+os.path.relpath(f,STATIC_LOCAL)
            fd['href']=	urllib.quote(href,'/:')
            fd['size'] = s.st_size
            files.append(fd)
    if sort_type == 'date':
        folders_sorted = sorted(folders,key=lambda x: x['ctime'],reverse=True)
        files_sorted = sorted(files, key=lambda x: x['ctime'],reverse=True)        
    elif sort_type == 'size':
        folders_sorted = sorted(folders,key=lambda x: x['basename'].lower() )
        files_sorted = sorted(files, key=lambda x: x['size'],reverse=True )        
    elif sort_type == 'name':
        folders_sorted = sorted(folders,key=lambda x: x['basename'].lower() )
        files_sorted = sorted(files, key=lambda x: x['basename'].lower() )        
    else:
        return 'ERROR, incorrect sorting parameter'
    
    previous_path =  subdir+sort_type+"/"+os.path.relpath(os.path.abspath(dirname(joined_path)),STATIC_LOCAL)
    current_path = subdir+"%s/"+os.path.relpath(os.path.abspath(joined_path),STATIC_LOCAL)
    html = """
    <html>
    <head> <title>%s</title>
    </head>
    <h1>%s</h1>
    <body style="font-family:courier; ">
    <table width='100%%' align='left' cellpadding='2'>
    """%(os.path.basename(joined_path),os.path.basename(joined_path),)
    html+="""<hr>
    <tr">
    <td width=100><i><a href='%s'>Size</a></i></td>
    <td width=100><i><a href='%s'>Date</a></i></td>
    <td width=200><i><a href='%s'>Name</a></i></td>    
    <td ></td>
    </tr>
    """%(current_path%'size',current_path%'date',current_path%'name',)
    html += FOLDER%(".","-",previous_path,"Parent Directory")
    html += "".join([FOLDER%(".",x['date_ctime'].strftime(DATE_FORMAT),x['relpath'],x['basename']) for x in folders_sorted])
    html +="".join([FILE%(convert_bytes(x['size']),x['date_ctime'].strftime(DATE_FORMAT),x['href'],x['basename']) for x in files_sorted])
    html += "</table>"
    html += "<hr><p>"
    if LIST_FILE_URLS:
        html +="".join([FILE_PARAGRAPH%(x['href'],x['href']) for x in files_sorted])
    
    html+="</p></body></html>"
    
    return html

if __name__ == "__main__":
    run(host=HOST,port=PORT,debug=True)
