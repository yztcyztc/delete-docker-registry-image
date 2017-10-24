#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
import os
import logging

app = Flask(__name__)
logging.basicConfig( format='%(levelname)s - [%(asctime)s] - %(message)s',filename='gc_log.log')
log = logging.getLogger(__name__)
registry_name = "11"

@app.route('/test', methods=['GET'])
def test():
    return 'test text'

@app.route('/command', methods=['POST'])
def command():
    # 需要从request对象读取表单内容：
    if request.form.get('password',-1)=='p':
        c=request.form['command']
        print(c)
        re=os.popen(c).read()
        print(re)
        return re
    return '<h3>Bad password.</h3>'

@app.route('/dry', methods=['POST'])
def dry():
    # 需要从request对象读取表单内容：
    if request.form.get('password',-1)=='p':
        log.info('Start GC --dry')
        print('Start GC --dry')
        name=request.form.get('name',registry_name)
        re=os.popen('docker exec %s /bin/registry garbage-collect --dry-run /etc/docker/registry/config.yml' % name).read()
        log.info(re)
        log.info('End GC --dry')
        return re
    return '<h3>Bad password.</h3>'

@app.route('/delete', methods=['POST'])
def delete():
    # 需要从request对象读取表单内容：
    if request.form.get('password',-1)=='p':
        log.info('Start GC')
        print('Start GC --dry')
        name=request.form.get('name',registry_name)
        re=os.popen('docker exec %s /bin/registry garbage-collect --dry-run /etc/docker/registry/config.yml' % name).read()
        log.info(re)
        log.info('End GC')
        return re
    return '<h3>Bad password.</h3>'

if __name__ == '__main__':
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s - [%(asctime)s] - %(message)s'))
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    print('program started')
    app.run(host='0.0.0.0',port='7777')


