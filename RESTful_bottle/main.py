# coding=utf-8
"""
synopsis: main entrance of bottle restful-api
author: haoranzeus@gmail.com (zhanghaoran)
"""
import codecs
import getopt
import logging.config
import os
import sys
import yaml

import port_workers

from bottle import abort
from bottle import request
from bottle import Bottle

logger = logging.getLogger(__name__)
_app = Bottle()


def usage():
    print('some usage information')
    # TODO (dengxinjie)


def main(argv):
    try:
        opts, args = getopt.getopt(
                argv, "h:p:c:", ["host=", "port=", "configure=", "help"])
    except getopt.GetoptError:
        usage()
        sys.exit()

    host = 'localhost'
    port = 8082
    conf_path = os.path.join(os.path.abspath("."), 'conf')
    for opt, arg in opts:
        if opt == '--help':
            usage()
            sys.exit()
        elif opt in ('-h', '--host'):
            host = arg
        elif opt in ('-p', '--port'):
            port = int(arg)
        elif opt in ('-c', '--configure'):
            conf_path = arg
        else:
            usage()
            exit()

    def _exit_w_info(info):
        print('\n%s\n' % info)
        usage()
        exit()

    def _ok_conf(conf):
        def check_cfg(cfg):
            cpath = os.path.join(conf, cfg)
            return ((os.path.exists(cpath) and cpath)
                    or _exit_w_info('missing %s.' % cpath))
        return [check_cfg(cfg) for cfg in ('api.yaml', 'logging.yaml')]

    api_conf, logging_conf = _ok_conf(conf_path)
    woodenwaiter_conf = {}
    with codecs.open(logging_conf, 'r', 'utf-8') as logging_file:
        logging.config.dictConfig(yaml.load(logging_file))
    with codecs.open(api_conf, 'r', 'utf-8') as conff:
        woodenwaiter_conf.update(yaml.load(conff))
    print(woodenwaiter_conf)
    main_app = Bottle()
    main_app.mount(woodenwaiter_conf['url_root'], _app)

    main_app.run(host=host, port=port, debug=True)


@_app.post('/addcooker')
@_app.post('/addcooker/')
def add_customer():
    logger.debug('add customer: datas=%s', request.json)
    return request_handler(lambda: port_workers.add_cooker(request.json))


def request_handler(func):
    try:
        result = {'status': 'SUCCESS', "result": {}}
        res = func()

    # TODO handle exceptions here

    except Exception as e:
        logger.exception('Error when handle request: %s', e)
        abort(500, e)
    else:
        if res is not None:
            result['result'] = res
        result['status'] = 'SUCCESS'
        logger.debug('result = %s', result)
        return result


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
