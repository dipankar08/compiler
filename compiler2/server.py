# Some code here
import tornado.escape
import tornado.ioloop
import tornado.web
import pdb
from execute import Execute
#from bson import json_util
import json
from Logs import LE, Log



class CompilerHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")

    def options(self, cmd):
        self.write("Not supported!")

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'OPTIONS, TRACE, GET, HEAD, POST, PUT')

    def get(self, cmd):
        args = self.request.arguments
        data = {}
        for k, v in args.items():
            if v[0] in ['True', 'true']:
                v[0] = True
            elif v[0] in ['False', 'false']:
                v[0] = False
            elif v[0].isdigit():
                v[0] = int(v[0])
            data[k] = v[0]
        self.handle(cmd, data)

    def post(self, cmd):
        data = None
        filedata = None

        if not self.request.body:
            res = {'status': 'error', 'msg': 'You must send some json data with post request'}
            #self.write(json.dumps(res, default=json_util.default))
            self.write(json.dumps(res))
            return

        if 'multipart/form-data' in self.request.headers.get('Content-Type'):
            is_json_data = False
        else:
            is_json_data = True

        if is_json_data:
            try:
                data = tornado.escape.json_decode(self.request.body)
            except Exception as e:
                LE(e)
                res = {'status':'error', 'msg':'You send an invalid json object.', 'help':'please paste the request body in https://jsonlint.com/ to check the error in your json'}
                self.write(json.dumps(res))
                #self.write(json.dumps(res, default=json_util.default))
                return
        else:
            data = dict([(k, v[0]) for k, v in self.request.arguments.items()])

            if self.request.files.get('file-0'):
                filedata = self.request.files.get('file-0')[0]['body']

        self.handle(cmd, data, filedata)

    def options(self,cmd):
        # no body
        print(' Optiosn called')
        #pdb.set_trace()
        self.set_status(204)
        self.finish()

    def handle(self, cmd, json_data, filedata = None):
        #python 3 conversion
        #cmd = cmd.decode('ascii')
        print("[INFO] Command sent:"+str(cmd))
        res = {}
        try:
            # pdb.set_trace()
            browserdata = {'remote_ip': self.request.remote_ip, 'browser': self.request.headers.get('User-Agent')}
            Log.i(browserdata)
            # Python 3 conversion needed.
            #pdb.set_trace()
            lang = json_data.get('lang', 'C')
            name = json_data.get('name', 'Solution')
            code = json_data.get('code', '')
            input= json_data.get('input', '')
            depends=json_data.get('depends', '')
            testcases=json_data.get('testcases', '')
            func = ''

            # Unicode
            #[ cmd, lang, name, code, input, depends] = [ xx.encode('utf8') if xx else '' for xx in [ cmd, lang, name, code, input, depends]]
            # Logic  Here ..
            try:
                #pdb.set_trace()
                if cmd == 'compile':
                    res = Execute(lang, name, code, func, input, depends, testcases).save(name, code, func, input).compile(name)
                elif cmd == 'run':
                    res = Execute(lang, name, code, func, input, depends, testcases).save(name, code, func, input).fullrun(name)
                elif cmd == 'crashbt':
                    res = Execute(lang, name, code, func, input, depends, testcases).getCrashBackTrace();
                elif cmd == 'mleaks':
                    res = Execute(lang, name, code, func, input, depends, testcases).getMemoryleaks()
                elif cmd == 'perf':
                    res = Execute(lang, name, code, func, input, depends, testcases).testperf(name)
                else:
                    res = {'status':'error', 'msg':'Invalid cmd send to codestudio', 'help':'valid command : run | compile | debug |'}
            except Exception as e:
                LE(e)
                res ={'status':'error', 'msg':'Internal error occure with codestudio. Please contact ddutta', 'sys_error':str(e)}
        except Exception as e:
            LE(e)
            res['status'] = 'error'
            res['msg'] = 'Some internal Error'
            res['help'] = 'Talk to dev ops:'+str(e)

        #self.write(json.dumps(res, default=json_util.default))
        self.write(json.dumps(res))

application = tornado.web.Application([
    (r"/([a-z0-9_/]*)", CompilerHandler),
], debug=True)


def start(port = None):
    if not port:
        port = 7777
    Log.i('Staring the server...')
    Log.i('Please open your brower and hit http://0.0.0.0:'+str(port)+'/')
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


start()
