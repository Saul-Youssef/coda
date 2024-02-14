#
#    Jupyter kernel
#
#    jupyter kernelspec install --user coda
#    jupyter kernelspec list
#
from ipykernel.kernelbase import Kernel

import base,Language,Evaluate,IO,Source
IO.OUT.kernel() # set stdout to kernel mode
#Evaluate.resolve(Language.lang('homecontext:', base.data(),base.data()),1000)
#D = Evaluate.evaluate(100,base.CONTEXT,Language.lang('ap use1 : localdef:',base.data(),base.data()))
#D = base.CONTEXT.evaluate(100,Language.lang('ap use1 : localdef:',base.data(),base.data()))
LANG = Language.lang('ap use1 : localdef:',base.data(),base.data())
#D = base.data(*[d for d in Evaluate.evaluate(100,base.CONTEXT,LANG)])
#D = Evaluate.Eval(10*Evaluate.STEPS,10*Evaluate.EVALS,base.CONTEXT)(LANG)
#if not D.empty(): raise error('Local definition error '+str(D))
D = Evaluate.Eval(Evaluate.STEPS,Evaluate.SECONDS,base.CONTEXT)(LANG)
EV = Evaluate.Eval(500,Evaluate.SECONDS,base.CONTEXT)
if not D.empty(): raise error('Local definition error '+str(D))

class EchoKernel(Kernel):
    implementation = 'Echo'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {
        'name': 'Any text',
        'mimetype': 'text/plain',
        'file_extension': '.co',
    }
    banner = "Coda"
#
#    def do_execute(self, code, silent, store_history=True, user_expressions=None,
#                   allow_stdin=False):
    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=True):
#        EV = Evaluate.Eval(Evaluate.STEPS,Evaluate.EVALS,base.CONTEXT)
        if not silent:
            L = []
            for d in Source.language(code):
                try:
                    D = EV(d)
                    IO.OUT(str(D))
                    s = IO.OUT.flush()
                    if len(s)>0: L.append(s)
                except Exception as e:
                    L.append(IO.OUT.flush()+'...traceback: '+str(e))
            stream_content = {'name': 'stdout', 'text': '\n'.join(L)}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=EchoKernel)
