import traceback
import sys

def format_exception(e):
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    # Removing the last \n
    exception_str = exception_str[:-1]

    return exception_str
def LE(e):
        if not e:
            print(' We dont have e')
            return
        print ("#"*50)
        print ("Printing only the traceback above the current stack frame")
        print ("".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])))
        print ("Printing the full traceback as if we had not caught it here...")
        x =  format_exception(e)
        print (x)
        print ("#"*50)
        return str(x)


class Log(object):
    @staticmethod
    def e(msg):
        print ('[ERROR]'+ str(msg))

    @staticmethod
    def d(msg):
        print ('[DEBUG]'+ str(msg))

    @staticmethod
    def i(msg):
        print ('[INFO] '+ str(msg))
