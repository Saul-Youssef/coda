#
#    Jupyter kernel
#
#    jupyter kernelspec install --user coda
#    jupyter kernelspec list
#
from ipykernel.kernelbase import Kernel

import base,Language,Evaluate,IO,Compile
IO.OUT.kernel() # set stdout to kernel mode
Evaluate.resolve(Language.lang('homecontext:', base.data(),base.data()),1000)

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
        if not silent:
            L = []
            for d in Compile.coda(code):
                for c in d: L.append(c)
            D = base.data(*L)
            try:
#                IO.OUT(str(Evaluate.depth(D,100)[0]))
                IO.OUT(str(Evaluate.default(D)))
                out = IO.OUT.flush()
            except Exception as e:
                out = IO.OUT.flush()+'...traceback: '+str(e)
            stream_content = {'name': 'stdout', 'text': out}
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
