#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Main module."""

## --- Logging code
import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)
## --- End logger.code

import kanboard
from operator import itemgetter
import os
import base64
import pprint
import time
import configargparse
import datetime

#result = client.search_tasks(project_id = projectId, query=configDefinition)

# --- disable SSL certificate checks
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

if __name__ == '__main__':
	logger.info('kanboard_copier started')

	# --- configargparser configuration
	parser = configargparse.ArgParser(default_config_files=['./kanboard_copier.cnf', '~/.kanboard_copier.cnf'], add_help=True)

	parser.add('--left_kanboard_url', required=False, action='store', 
		   default='http://localhost:8100/jsonrpc.php', dest='left_kanboard_url', 
		   help='Left Kanboard backend: URL')
	parser.add('--left_kanboard_username', required=False, action='store', 
		   default=None, dest='left_kanboard_username', 
		   help='Left Kanboard backend: username')
	parser.add('--left_kanboard_token_apikey', required=False, action='store', dest='left_kanboard_token_apikey', 
		   help='Left Kanboard backend: API key')
	parser.add('--left_kanboard_projectid', required=False, action='store', dest='left_kanboard_projectid', 
		   help='Left Kanboard backend: Project ID')
	
	parser.add('--right_kanboard_url', required=False, action='store', 
		   default='http://localhost:8100/jsonrpc.php', dest='right_kanboard_url', 
		   help='Right Kanboard backend: URL')
	parser.add('--right_kanboard_username', required=False, action='store', 
		   default=None, dest='right_kanboard_username', 
		   help='Right Kanboard backend: username')
	parser.add('--right_kanboard_token_apikey', required=False, action='store', dest='right_kanboard_token_apikey', 
		   help='Right Kanboard backend: API key')
	parser.add('--right_kanboard_projectid', required=False, action='store', dest='right_kanboard_projectid', 
		   help='Right Kanboard backend: Project ID')

	config = parser.parse_args()

	left  = kanboard.Client(config.left_kanboard_url, config.left_kanboard_username, config.left_kanboard_token_apikey)
	logger.debug('left client connected "{left_kanboard_url}"'.format(**(vars(config))))
	right = kanboard.Client(config.right_kanboard_url, config.right_kanboard_username, config.right_kanboard_token_apikey)
	logger.debug('right client connected "{right_kanboard_url}"'.format(**(vars(config))))

	# step 1: check columns
	logger.info('step 1: copy columns from left with projectid {left_kanboard_projectid}'.format(**vars(config)))
	columns = left.get_columns(project_id = config.left_kanboard_projectid)
	for c in columns:
		# create column on right - it is not overwritten if already there
		c['result'] = right.add_column(project_id = config.right_kanboard_projectid, title=c['title'],
			task_limit=c['task_limit'], description=c['description'])
		logger.debug('-- adding column "{title}" to right gave {result}'.format(**c))
		if c['result']:
			# now update position
			detail = left.get_column(column_id=c['id'])
			logger.debug('-- updating position of column "{title}" to right'.format(**c))
			right.change_column_position(project_id = config.right_kanboard_projectid, column_id=c['result'], position=detail['position'])
 
	logger.info('kanboard_copier finished')
