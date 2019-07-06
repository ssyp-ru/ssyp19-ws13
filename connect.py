from pyswip import Prolog, Query, Variable, Functor
import tempfile
import re
import os


class PrologConnecter:

    def __init__(self):
        self.files_name = []
        self.prolog = Prolog()

    @staticmethod
    def create_temp_file(code) -> str:

        if 'connect_files' not in os.listdir():
            try:
                os.mkdir('connect_files')
            except PermissionError:
                raise PermissionError("Don't have permission for create a dir")

        file = tempfile.NamedTemporaryFile('w', delete=False, suffix='.pro', dir='connect_files')
        with file as f:
            f.write(code)

        return file.name[file.name.rfind('\\') + 1::]

    def consult_code(self, code, delete=True):
        self.consult_file(self.create_temp_file(code), delete)

    def consult_file(self, file_name: str, delete=True):
        self.prolog.consult('connect_files/' + file_name)
        self.files_name.append((file_name, delete))

    def get_n_ans(self, instructions: str, maxresult=1, **kwargs):  # warning! can be broken

        res = list(self.prolog.query(instructions, maxresult=maxresult, **kwargs))

        for file, delete in self.files_name:
            if delete:
                os.remove('connect_files\\' + file)
        return res

    # TODO: write this
    def get_all_ans(self, instructions):
        ...

    # TODO: write this
    @staticmethod
    def parse_ins(instruction):
        ...

# test1
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
# con = PrologConnecter()
# con.consult_code(code, delete=False)
# con.consult_file('../coins.pl', delete=False)
# con.consult_file('../lst1.pl', delete=False)
# con.consult_file('../lst2.pl', delete=False)
# con.consult_file('../fib.pl', delete=False)
# con.consult_file('../puzzle1.pro', delete=False)
# # instructions = 'parent(ash, X),f(10, Y),solve(Z)'
# instructions = 'coins(X,100,500),solve(Y)'
# ans = con.get_n_ans(instructions)
# print(ans)


# test0
# prolog = Prolog()
# prolog.consult('coins.pl')
# prolog.consult('lst1.pl')
# prolog.consult('lst2.pl')
# prolog.consult('fib.pl')
# prolog.consult('puzzle1.pro')
# vars = [Variable() for _ in range(10)]
# fib = Functor('f', 2)
# coins = Functor('coins', 3)
# mfib = Functor('fi', 2)
# qsort = Functor('qsort', 2)
# puzzle1 = Functor('solve', 1)
# a = list(range(10))
# shuffle(a)
# qmfib = Query(mfib(0, vars[0]), fib(10, vars[1]), qsort(a, vars[2]), coins(vars[3], 100, 500), puzzle1(vars[4]))
# while qmfib.nextSolution():
#     print(*map(lambda x: x.value, vars))
# qmfib.closeQuery()