#Please add a new language if you want to support

BASE_PATH = '/tmp/'

LangConfig = {

	'C':{
		'ext':'c',
		
		'compile_cmd': 'gcc -g  -ldl -pthread  -std=c99 -o $prog_obj_name $prog_file_name',
		'run_cmd':'$prog_obj_name',
		
		'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
		'run_cmd_with_depends':'',
	},
	'Obj-C':{ #sudo apt-get install gobjc  sudo  && apt-get install gnustep-make  && sudo apt-get install gnustep-devel
		'ext':'m',
		#'compile_cmd': r'gcc $prog_file_name `gnustep-config --objc-flags` `gnustep-config --base-libs` -o $prog_obj_name',
		'compile_cmd': r'gcc $prog_file_name -o $prog_obj_name -MMD -MP -DGNUSTEP -DGNUSTEP_BASE_LIBRARY=1 -DGNU_GUI_LIBRARY=1 -DGNU_RUNTIME=1 -DGNUSTEP_BASE_LIBRARY=1 -fno-strict-aliasing -fexceptions -fobjc-exceptions -D_NATIVE_OBJC_EXCEPTIONS -pthread -fPIC -Wall -DGSWARN -DGSDIAGNOSE -Wno-import -g -O2 -fgnu-runtime -fconstant-string-class=NSConstantString -fexec-charset=UTF-8 -I. -I/home/dipankar/GNUstep/Library/Headers -I/usr/local/include/GNUstep -I/usr/include/GNUstep -rdynamic -pthread -shared-libgcc -fexceptions -fgnu-runtime -L/home/dipankar/GNUstep/Library/Libraries -L/usr/local/lib -L/usr/lib -lgnustep-base -lobjc -lm',
		'run_cmd':'$prog_obj_name',		
		'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
		'run_cmd_with_depends':'',
	},
	'C++':{
		'ext':'cpp',
		
		'compile_cmd': 'g++ -ldl -pthread -std=c++11 -g -o $prog_obj_name $prog_file_name',
		'run_cmd':'$prog_obj_name',
		
		'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
		'run_cmd_with_depends':'',
	},
	'C++98':{
		'ext':'cpp',
		
		'compile_cmd': 'g++ -ldl -pthread -g -o $prog_obj_name $prog_file_name',
		'run_cmd':'$prog_obj_name',
		
		'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
		'run_cmd_with_depends':'',
	},
	'C++11':{
		'ext':'cpp',
		
		'compile_cmd': 'g++ -ldl -pthread -std=c++11 -g -o $prog_obj_name $prog_file_name',
		'run_cmd':'$prog_obj_name',
		
		'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
		'run_cmd_with_depends':'',
	},
	'C++14':{
		'ext':'cpp',
		
		'compile_cmd': 'g++ -ldl -pthread  -std=c++1y -g -o $prog_obj_name $prog_file_name',
		'run_cmd':'$prog_obj_name',
		
		'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
		'run_cmd_with_depends':'',
	},
	'CLang':{ 
		'ext':'cpp',
		
		'compile_cmd': 'clang++ -ldl -pthread  -std=c++1y -g -o $prog_obj_name $prog_file_name',
		'run_cmd':'$prog_obj_name',
		
		'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
		'run_cmd_with_depends':'',
	},
	'Python':{
		'ext':'py',
		
		'compile_cmd': 'pylint  -E  --disable=print-statement  $prog_file_name',
		'run_cmd':'python $prog_file_name',
		
		'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
		'run_cmd_with_depends':'',
	},
	'Perl':{
		'ext':'pl',
		
		'compile_cmd': 'perl $prog_file_name',
		'run_cmd':'perl $prog_file_name',
		
		'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
		'run_cmd_with_depends':'',
	},
	'R':{
		'ext':'r',
		
		'compile_cmd': 'Rscript $prog_file_name',
		'run_cmd':'Rscript $prog_file_name',
		
		'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
		'run_cmd_with_depends':'',
	},
	'Ruby':{
		'ext':'rb',
		
		'compile_cmd': 'ruby $prog_file_name',
		'run_cmd':'ruby $prog_file_name',
		
		'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
		'run_cmd_with_depends':'',
	},
	'Node':{
		'ext':'js',
		
		'compile_cmd': 'node $prog_file_name',
		'run_cmd':'node $prog_file_name',
		
		'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
		'run_cmd_with_depends':'',
	},
	'Go':{
		'ext':'go',
		
		'compile_cmd': 'go build -o $prog_obj_name $prog_file_name',
		'run_cmd':'$prog_obj_name',
		
		'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
		'run_cmd_with_depends':'',
	},
	'Java':{ #sudo apt-get install  openjdk-7-jdk
		'ext':'java',
		'prog_obj_name':'$name',
		
		'compile_cmd': "javac -d $BASE_PATH $prog_file_name",# prog_obj_name, prog_file_name
		'run_cmd':"java -classpath $BASE_PATH $prog_obj_name ",
		
		'compile_cmd_with_depends': "javac -cp \"$dps\" -d $BASE_PATH $prog_file_name",# dps, prog_file_name
		'run_cmd_with_depends': "java -cp \"$BASE_PATH:$dps\" $prog_obj_name" ,
	},
	'Scala':{ #sudo apt-get install scala
		'ext':'scala',
		'prog_obj_name':'$name',
        'classname_is_same_as_file_name':True,
		
		'compile_cmd': "scalac  $prog_file_name",# prog_obj_name, prog_file_name
		'run_cmd':"scala $prog_obj_name ",
		
		'compile_cmd_with_depends': "",# dps, prog_file_name
		'run_cmd_with_depends': "" ,
	},
	'C#':{ #sudo apt-get install mono-xsp2 mono-xsp2-base
		'ext':'cs',
		
		'compile_cmd': 'gmcs  $prog_file_name',
		'run_cmd':'mono $prog_obj_name',
		
		'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
		'run_cmd_with_depends':'',
	},
    'Haskell':{ #sudo apt-get install haskell-platform
		'ext':'hs',
		
		'compile_cmd': 'ghc -O2 --make $prog_file_name -o $prog_obj_name -threaded -rtsopts  ',
		'run_cmd':'$prog_obj_name',
		
		'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
		'run_cmd_with_depends':'',
    },
    'Python3':{ #sudo apt-get install python3
                'ext':'py',

                'compile_cmd': 'pylint -E --disable=print-statement $prog_file_name',
                'run_cmd':'python3 $prog_file_name',
 
                'compile_cmd_with_depends': '',# prog_obj_name, prog_file_name
                'run_cmd_with_depends':'',
    },
    'Prolog':{ #sudo apt-get install gprolog
                   'ext':'pl',

                   'compile_cmd': 'gplc -o $prog_obj_name $prog_file_name',

                   'run_cmd': '$prog_obj_name',

                   'compile_cmd_with_depends': '',
                   'run_cmd_with_depends': '',
    },
    'PHP':{ #sudo apt-get install php5-cli
                'ext':'php',

                'compile_cmd': 'php $prog_file_name',
                'run_cmd': 'php $prog_file_name',

                'compile_cmd_with_depends': '',
                'run_cmd_with_depends': '',
    },
    'Clojure':{ #sudo apt-get install clojure1.4
                    'ext':'clj',

                    'compile_cmd': 'clojure $prog_file_name',
                    'run_cmd': 'clojure $prog_file_name',

                    'compile_cmd_with_depends': '',
                    'run_cmd_with_depends': '',
   },
}
