#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
import os
import logging

app = Flask(__name__)
log=logging.getLogger(__name__)

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
        image=request.form['image']
        tag = request.form.get('tag',-1)
        log.info('DRY_param:[Image:%s  Tag:%s]',image,tag)
        if tag==-1 :
            print('delete respoitory')
            re=os.popen('delete_docker_registry_image --image %s -p --dry-run' % image).read()
        else :
            print('delete tag')
            re = os.popen('delete_docker_registry_image --image %s:%s  -p --dry-run' %(image,tag)).read()
        return re
    return '<h3>Bad password.</h3>'

@app.route('/delete', methods=['POST'])
def delete():
    # 需要从request对象读取表单内容：
    if request.form.get('password',-1)=='p':
        image=request.form['image']
        tag = request.form.get('tag',-1)
        log.info('DELTET_param:[Image:%s  Tag:%s]', image, tag)
        if tag==-1 :
            print('delete respoitory')
            re=os.popen('delete_docker_registry_image --image %s -p' % image).read()
        else :
            print('delete tag')
            re = os.popen('delete_docker_registry_image --image %s:%s -p' %(image,tag)).read()
        return re
    return '<h3>Bad password.</h3>'

if __name__ == '__main__':
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s - [%(asctime)s] - %(message)s'))
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    app.run(host='0.0.0.0',port='7777')


