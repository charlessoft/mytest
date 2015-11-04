#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2015-11-03 10:47:43
# @Last Modified by:   mithril
# @Last Modified time: 2015-11-04 15:08:54


from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with
import time

import logging
logger = logging.getLogger('webui')

from .app import app, api


@api.resource('/spider/project/<project>')
class SpiderProject(SpiderSettingBase):

    def get(self, project):
        projectdb = app.config['projectdb']
        if not projectdb.verify_project_name(project):
            return 'project name is not allowed!', 400
        info = projectdb.get(project, fields=['name', 'script'])
        return json.dumps(utils.unicode_obj(info)), \
            200, {'Content-Type': 'application/json'}

    def post(self, project):
        projectdb = app.config['projectdb']
            if not projectdb.verify_project_name(project):
                return 'project name is not allowed!', 400
            script = request.form['script']
            project_info = projectdb.get(project, fields=['name', 'status', 'group'])
            if project_info and 'lock' in projectdb.split_group(project_info.get('group')) \
                    and not login.current_user.is_active():
                return app.login_response

            if project_info:
                info = {
                    'script': script,
                }
                if project_info.get('status') in ('DEBUG', 'RUNNING', ):
                    info['status'] = 'CHECKING'
                projectdb.update(project, info)
            else:
                info = {
                    'name': project,
                    'script': script,
                    'status': 'TODO',
                    'rate': app.config.get('max_rate', 1),
                    'burst': app.config.get('max_burst', 3),
                }
                projectdb.insert(project, info)

            rpc = app.config['scheduler_rpc']
            if rpc is not None:
                try:
                    rpc.update_project()
                except socket.error as e:
                    app.logger.warning('connect to scheduler rpc error: %r', e)
                    return 'rpc error', 200

            return 'ok', 200