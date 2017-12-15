"""
/******************************************************************
 * Copyright (C) PeerReview, Inc - All Rights Reserved
 *
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential. This Project can not be copied    and / or
 * distributed without the express permission of Dipankar Dutta
 *
 * Written by Dipankar Dutta <dutta.dipankar08@gmail.com>, September 2015
 *
 ******************************************************************/
"""
import subprocess
import pdb
import fcntl, os
from Logs import Log, LE
#import utils
BASE_PATH = '/tmp/'
OK = 1
ERROR = 0
DEBUG = True

from languageConfig import LangConfig
import string
# # # # # # # # # # # # # # # #     GLOBAL DEFINATION Must be matched with CodeStudio.JS# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
SUPPORED_LANGUAGE = ['Python', 'C++', 'C', 'Obj-C', 'Java', 'C++11', 'C++98', 'C++14', 'CLang', 'Go', 'C# ', 'Perl', 'Ruby', 'Node', 'Scala', 'Haskell', 'Python3', 'Prolog', 'PHP', 'Clojure']
C_STYLE_SUPPORED_LANGUAGE = ['C++', 'C', 'Obj-C', 'C++11', 'C++98', 'C++14', 'CLang']
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# --------------    Sub process Thread model to execute the program ---------
import subprocess as sub, shlex
import threading

class RunCmd(threading.Thread):

    def __init__(self, cmd, inp, timeout=5, shell=False, lang = 'c'): # Time-out in second.
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.inp =inp
        self.timeout = timeout
        self.shell = shell
        self.lang = lang

    def run(self): # this is intertal.
        # pdb.set_trace()
        # Note VVI: Always use shell=False and for that we need to use shlex.split(...)
        self.p = sub.Popen(shlex.split(self.cmd), shell=False, bufsize=0, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE)
        self.p.stdin.flush()
        # self.p.stdout.flush()
        # self.p.stderr.flush()
        # Log.i(self.p.communicate(self.inp)
        self.p.stdin.write(self.inp)
        self.p.stdin.flush()
        self.p.wait()

    def Run(self):
        # pdb.set_trace()
        res = {'stdout': '', 'stderr': ''}
        Log.i('[INFO]: RunCmd: Running command : '+self.cmd)
        self.start()
        self.join(self.timeout)
        if self.is_alive():
            Log.i('Killing the process fourcefully..PID: ' + str(self.p.pid))
            try:
                self.p.terminate() # use self.p.kill() if process needs a kill -9
                self.p.kill()            #  needs for valgrind
            except:
                    Log.i('killed..')
            self.join()
            res['is_timeout'] = True
            Log.i('[INFO]: RunCmd: Timeout command : '+self.cmd)
            res['msg'] = 'TimeOut: review your code :\n Q1. is your program contins a infinite loop?\n Q2    did you provide all the    necessary inputs ?\n Q3. is your program can run in 30 sec ?'
            res['can_run'] = 'no'
        else:
            Log.i('[INFO]: RunCmd: Complete command : '+self.cmd)
            res['is_timeout'] = False
            res['msg'] = ''
        # pdb.set_trace()
        try:
            res['stdout'] = self.p.stdout.read()
            res['stderr'] = self.p.stderr.read()
            res['lang'] = self.lang
            res['return_code'] = self.p.returncode
        except Exception as e:
            LE(e)
            res['status'] = 'error'
            res['msg'] = 'Looks like some compiler is not installed in the remote server! please talk to dipankar'
            return res

        if res['msg']:
            res['output'] = res['msg']+'\n'+'-'*50+'\n'+ res['stderr'] + res['stdout']
        else:
            res['output'] = res['stderr'] + res['stdout']
        res['status'] = 'success'
        if DEBUG:
                Log.i('*'*50)
                Log.i(res)
                Log.i('*'*50)
        return res
# Unit Test..
# Log.i('before run'
# data = RunCmd(["./NCAD.exe", "arg1"], '', 10).Run()
# Log.i('After run'


def normFileName(sentence):
    import re
    sentence = re.sub('[^A-Za-z0-9]+', '', sentence)
    return sentence

def GCC_FORMETTED_ERROR(a):
    # pdb.set_trace()
    try:
        a1 = [ x.split(': ') for x in a.split('\n') if ('warning' in x)] # waring then Error
        a2 = [ x.split(': ') for x in a.split('\n') if ('error' in x)]
        a=a1+a2
        #  filter valid data
        a = [x for x in a if x[1].isdigit()]
        #  Modify common error message
        for i in a:
             j = i[3]
             if j.find('(') != -1: j = j[:j.find('(')]
             if j.find('{') != -1: j = j[:j.find('{')]
             if j.find('[') != -1: j = j[:j.find('[')]
             i[3] = j
        return a
    except Exception as e:
        LE(e)
        Log.i('Error: Not able to generated formated Error'+str(e))
        return []


import urllib
def NameURLLocalPath(jar):
    res =[]
    jars = [ j.strip() for j in jar.split(', ') if j ]
    for j in jars:
        fname = j[j.rfind('/')+1:]
        fname_mod = fname.replace('.zip', '') #  Name shoud not include .zip like abc.jar.zip => abc.jar
        res.append((fname_mod, j, BASE_PATH+fname))
    return res

def DownloadAndResolveJar(jars):
    " We willd ownlad the jar in /tmp/ and put it dr."
    try:
        NUP = NameURLLocalPath(jars) #  << <name, url, path >>
        alreay_have = os.listdir(BASE_PATH)
        succ_list=[]
        k = None
        for j in NUP:
            if j[0] not in alreay_have:
                Log.i('>>> Downloading jar/zip ... '+str(j))
                k =j
                testfile = urllib.URLopener()
                testfile.retrieve(j[1], j[2])
                if(j[2].endswith('.zip')):
                    Log.i('Unzipping '+j[2]+'....')
                    os.system('unzip '+j[2]+' -d /tmp/')
            else:
                Log.i('\n[INFO] Skipping Download for Jar file as already exist'+j[0])

        #  Let Recheck and Very fy...
        for j in NUP:
            if j[0] in alreay_have:
                succ_list.append(j[0])
        return (OK, 'Successfully Ported:\n...'+ '\n...'.join(succ_list))
    except Exception as e :
        LE(e)
        return (ERROR, 'Not able to resove dependency\n...For File: '+str(k)+'\n...Due to: '+str(e))

def tips(a):
    return '<div style="border: 1px solid bluecolor: bluefont-weight: boldpadding: 10pxwhite-space:normal"><i>Tips: </i><br>'+a+'</div>'


class Execute:
    """Please call this, it will generate all language specifc command...
    depends: will be list of url or jar file in case of java
    """
    def __init__(self, lang="c", name= '', main= '', func= '', input= '', depends= '', testcases=None):

        # Normalized name a single string.. as you know that..
        # Spdb.set_trace()
        this_config = LangConfig.get(lang)
        if not this_config:
            Log.i('Error>>> Config not found for '+ lang)

        if(this_config.get('classname_is_same_as_file_name') == True ):
            name = 'Solution'
        name = normFileName(name)

        # Setting up self veriables.
        self.name = name
        self.main = main
        self.func = func
        self.input = input+'\n'
        self.lang=lang
        self.depends = depends
        self.testcases = testcases

        #  if you want to support a new language please add here
        global SUPPORED_LANGUAGE
        if self.lang not in SUPPORED_LANGUAGE:
            self.lang = 'c'
        Log.i('-'*50)
        Log.i('>>> INFO    We are executing :File name : '+name+' Language: '+self.lang)
        Log.i('-'*50)

        # build dependency paths : Now it is only suppoted for java..
        dps = ''
        if self.lang == 'java' and self.depends:
            dps = ': '.join([ BASE_PATH+a[0] for a in NameURLLocalPath(self.depends) ])

        # Building Uniform Commnads
        try:
            # pdb.set_trace()

            ext = '.'+this_config['ext']

            self.prog_file_name=BASE_PATH+name+ext
            self.func_file_name = BASE_PATH +name+'_func'+ext
            self.input_file_name= BASE_PATH+name+'.in'
            self.prog_obj_name= BASE_PATH+name+'.exe' if this_config.get('prog_obj_name') == None else string.Template(this_config['prog_obj_name']).substitute({'name':name})

            data = {'prog_obj_name': self.prog_obj_name, 'prog_file_name':self.prog_file_name, 'input_file_name':self.input_file_name, 'BASE_PATH':BASE_PATH, 'dps':dps}

            if not self.depends:
                self.compile_cmd = string.Template(this_config['compile_cmd']).substitute(data)
                self.run_cmd = string.Template(this_config['run_cmd']).substitute(data)
            else:
                self.compile_cmd = string.Template(this_config['compile_cmd_with_depends']).substitute(data)
                self.run_cmd = string.Template(this_config['run_cmd_with_depends']).substitute(data)

            # Thease only supports for C, C++
            self.crash_bt_cmd = 'gdb  ' +self.prog_obj_name+' -x '+BASE_PATH+'gdb_cmd_file.txt'+ ' < '+self.input_file_name
            self.memory_leak_cmd = 'valgrind --leak-check=full ' +self.prog_obj_name
            self.make_debug_trace = 'gdb  -x '+BASE_PATH+'gdb_trace_cmd_temp.txt ' +self.prog_obj_name

        except Exception as e:
                LE(e)
                Log.i('Error>>> Building Uniform Commnads '+str(e))
        Log.i('INFO: We compleed the configuatiuon for the language: Now you can compile, run etc ...')
        Log.i('*'*50)

    def ResolveDependency(self):
        " Resolve dependency .."
        r = (ERROR, 'Look linke language is wrong ')
        if self.lang == 'java':
            r = DownloadAndResolveJar(self.depends)
        return r

    def save(self, name= 'hello', main="", func='', input=""):
        # pdb.set_trace()
        # Include func
        if func:
            Log.i('using Module....')
            if self.lang == 'c' or self.lang == 'cpp':
                main = '# include "'+self.func_file_name+'"\n'+main
        # Write files...
        with open (self.prog_file_name, 'w+') as f: f.write (main)
        with open (self.func_file_name, 'w+') as f: f.write (func)
        with open (self.input_file_name, 'w+') as f: f.write (input)
        self.input =input+'\n'
        return self

    def compile(self, name= 'hello'):
        Log.i('Compiling cmd: '+self.compile_cmd)
        # pdb.set_trace()
        res= {}
        # Decide if some depency to be solved before compile the app.
        if self.depends:
            ret = self.ResolveDependency()
            if ret[0] == ERROR:
                res['can_run'] = 'no'
                res['output'] = ret[1] + '\n'
                return res
            else:
                res['output'] = ret[1] + '\n'
        else:
            res['output'] = ''

        try:
            res = RunCmd(self.compile_cmd, self.input, shell=True, lang = self.lang).Run()
            res['output'] = ''
        except Exception as e:
            LE(e)
            Log.i('Error: RunCmd Failed..')
            res['callstack']= LE(e)

        # pdb.set_trace()
        # 3. Analize Result
        res['formated_error'] =[]
        if self.lang == 'py':
            if 'E: ' in res['stdout']:
                res['msg']= 'syntax Error : Not able to compile'
                res['output'] += res['stdout']
                res['can_run'] = 'no'
                res['status'] = 'error' #  This is compilation status
            elif 'W: ' in res['stdout']:
                res['msg'] = 'Compiled succesully with warning'
                # res['output'] +=res['stdout'] #  No need to show lot of gurbae for python
                res['can_run'] = 'yes'
                res['status'] = 'info' #  This is compilation status
            else:
                res['msg']= 'Compiled succesully.'
                res['output'] += res['msg']
                res['can_run'] = 'yes'
                res['status']= 'success' #  This is compilation status
        else: #  for c, c++, java Code..
            Log.i(res)
            if self.lang == 'c' or self.lang == 'cpp' or self.lang == 'cpp98' or self.lang == 'cpp11' or self.lang == 'cpp14':
                        res['formated_error'] = GCC_FORMETTED_ERROR(res['stderr'])
            if 'error' in res['stderr']:
                res['msg']= 'Syntax Error : Not able to compile'
                res['output'] = res['stderr']
                res['can_run'] = 'no'
                res['status']= 'error'
            elif 'warning: ' in res['stderr']:
                res['msg']= 'Compiled succesully with warning\n'
                res['output'] = res['stderr']
                res['can_run'] = 'yes'
                res['status']= 'info' #  This is compilation status
            else:
                res['msg']= 'Compiled succesully.'
                res['output'] = 'Your program run successfully !'
                res['can_run'] = 'yes'
                res['status']= 'success'
        return res

    # Remove this
    def SmartTips(self, err):
        res = ''
        if self.lang == 'java':
            if 'error: cannot find symbol' in err:
                res += tips('Opps! looks like you are using external lib. Search it at <a TARGET="_blank" href ="http://www.java2s.com/Code/Jar/CatalogJar.htm">Here</a> and add it in editor as "$DEPENDS http://www.java2s.com/.../abc.jar". Hope this helps!')
        return res

    # Just a run.
    def run(self, name=None):
        res= {'stdout': '', 'stderr': ''}
        try:
            res = RunCmd(self.run_cmd, self.input, lang=self.lang).Run()
            res['msg'] = 'Run successfully..'
        except Exception as e:
            LE(e)
            Log.i('Error: RunCmd Failed..')
            res['callstack']= LE(e)
        return res

    # Run with with perticular given input
    def runwithinput(self, name=None, input= ''):
        res= {'stdout': '', 'stderr': ''}
        try:
            res = RunCmd(self.run_cmd, input, lang=self.lang).Run()
            res['msg'] = 'Run successfully..'
        except Exception as e:
            LE(e)
            Log.i('Error: RunCmd Failed..')
            res['callstack']= LE(e)
        return res

    # This will taken care to comple and run in one short, run with all test cases
    def fullrun(self, name=None):
        res= {'stdout': '', 'stderr': ''}
        # pdb.set_trace()
        try:
            if LangConfig.get(self.lang).get('compile_is_run') == True :
                return self.compile()
            else:
                # we need to do both
                res = self.compile()
                if res['can_run'] == 'yes' and self.testcases:
                    res['testcaseresult']=[]
                    for tc in self.testcases :
                        ret = self.runwithinput(None, tc['input']+'\n')
                        comment = ''
                        if ret['is_timeout']:
                            comment = 'Time limit Exceed'
                        elif ret['return_code'] < 0:
                            comment = 'Program Crashed'
                        res['testcaseresult'].append({'input':tc['input'], 'expected':tc['output'], 'observed': ret['stdout'], 'comment': comment})
                        res['msg'] = 'All testcase executed successfully.'
                        return res
                elif res['can_run'] == 'yes':
                    return self.run()
                else:
                    return res
        except Exception as e:
            LE(e)
            Log.i('Error: fullrun Failed..')
            res['callstack'] = Log(e)
        return res


    # --------------------------------------------------
    #         This function allow you to get the call stack
    # ---------------------------------------------------
    def getCrashBackTrace(self):
        res= {'stdout': '', 'stderr': ''}
        if(self.lang not in C_STYLE_SUPPORED_LANGUAGE):
            return {'status': 'error', 'msg': 'we can only have callstack if you are using c or cpp'}
        try:
            res = RunCmd(self.crash_bt_cmd, self.input, shell=True).Run()
        except Exception as e:
            LE(e)
            Log.i('Error: RunCmd Failed..')
            res['callstack']= LE(e)
        return res


    # --------------------------------------------------
    #         This function allow you to get Memory leaks for C/C++
    # ---------------------------------------------------
    def getMemoryleaks(self):
        res= {'stdout': '', 'stderr': ''}
        if(self.lang not in C_STYLE_SUPPORED_LANGUAGE):
            return {'status': 'error', 'msg': 'we can only have callstack if you are using c or cpp'}
        try:
            res = RunCmd(self.memory_leak_cmd, self.input).Run()
        except Exception as e:
            LE(e)
            Log.i('Error: RunCmd Failed..')
            res['callstack']= Log(e)
        return res



    # --------------------------------------------------
    #         This function allow you to get Memory leaks for C/C++
    # ---------------------------------------------------
    def makeDebugTrace(self):
        res= {'stdout': '', 'stderr': ''}
        if(self.lang not in C_STYLE_SUPPORED_LANGUAGE):
            return {'status': 'error', 'msg': 'we can only have makeDebugTrace if you are using c or cpp'}
        try:
            # pdb.set_trace()
            import utils
            file_data = utils.GDB_SCRIPT_TRACE % ('rbreak '+self.prog_file_name+':.* \n' )
            with open('/tmp/gdb_trace_cmd_temp.txt', 'w') as the_file:
                the_file.write(file_data)

            res = RunCmd(self.make_debug_trace, '\n\n\n\n', timeout=10).Run() #  we will give almost 20 sec to run..

            res['stdout'] = utils.parseDebugTrace(res['stdout'])
            # res['output'] = 'Total steps returned is : '+ str(len(res['stdout']))
        except Exception as e:
            LE(e)
            Log.i('Error: RunCmd Failed..')
            res['callstack']= LE(e)
        return res


    def testperf(self, name=None):
        # TODO for python
        Log.i('Testing Performance...')
        cmd = "time ./%s.exe" %(name)
        Log.i("Launching command: " + cmd)
        sp = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out= sp.communicate(input=self.input)
        res= {}
        res['time'] = out[1]
        sp.poll()

        cmd = "./memusg %s.exe" %(name)
        Log.i("Launching command: " + cmd)
        sp = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out= sp.communicate(input=self.input)
        res['space'] = out[1]
        sp.poll()
        res['output'] = res['time']+res['space']
        return res
