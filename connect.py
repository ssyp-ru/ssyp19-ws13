from pyswip import Prolog, Query, Variable, Functor
from random import shuffle
import tempfile
import os
'''
prolog = Prolog()
prolog.consult('coins.pl')
prolog.consult('lst1.pl')
prolog.consult('lst2.pl')
prolog.consult('fib.pl')
prolog.consult('puzzle1.pro')
vars = [Variable() for _ in range(10)]
fib = Functor('f', 2)
coins = Functor('coins', 3)
mfib = Functor('fi', 2)
qsort = Functor('qsort', 2)
puzzle1 = Functor('solve', 1)
a = list(range(10))
shuffle(a)
qmfib = Query(mfib(0, vars[0]), fib(10, vars[1]), qsort(a, vars[2]), coins(vars[3], 100, 500), puzzle1(vars[4]))
while qmfib.nextSolution():
    print(qmfib.fid, qmfib.qid)
    print(*map(lambda x: x.value, vars))
qmfib.closeQuery()
# for s in prolog.query('coins(X,100,500),solve(Y)'):
#     print(s['X'],s['Y'])
'''


class PrologConnecter:

    def __init__(self, file_name, delete=False):
        self.file_name = file_name
        self.delete_file_after_run = delete
        self.prolog = Prolog()
        self.prolog.consult('connect_files/' + self.file_name)

    @classmethod
    def via_code(cls, code, *args,**kwargs):

        if not 'connect_files' in os.listdir():
            os.mkdir('connect_files')

        file = tempfile.NamedTemporaryFile('w', delete=False, suffix='.pro', dir='connect_files')
        with file as f:
            f.write(code)
        return cls(file.name[file.name.rfind('\\') + 1::], *args, **kwargs)

    def get_ans(self, instructions, **kwargs):
        res = self.prolog.query(instructions, **kwargs)
        for i in res:
            return i

        ##FIXME: can return only 1 solve
        if self.delete_file_after_run:
            os.remove('connect_files\\' + self.file_name)
        return None


# code = '''parent(ash, cat).
# parent(kilo, mom).
# parent(ash, tom).
# f(1, 1).
# f(2, 1).
# f(X, Y):-
#     T1 is X - 1,
#     T2 is X - 2,
#     f(T1, R1),
#     f(T2, R2),
#     Y is R1 + R2.'''
# con = PrologConnecter.via_code(code)
# # con = PrologConnecter('../fib.pl')
# instructions = 'parent(ash, X),f(10, Y)'
# # instructions = 'f(10,Y)'
# ans = con.get_ans(instructions)
# print(ans)