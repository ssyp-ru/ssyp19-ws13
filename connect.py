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

    def get_all_ans(self, instructions):
        functors, vars = self.parse_ins(instructions)
        q = Query(*(functors[i](*vars[i]) for i in range(len(functors))))
        while q.nextSolution():
            pass
        q.closeQuery()
        return vars

    @staticmethod
    def parse_ins(instruction):
        preds = re.findall('(\w[\S]+|\w)\(([\w\d\,\ ]+)\)', instruction)
        functors = []
        vars = []
        for pred, atoms in preds:
            v = []
            functors.append(Functor(pred, len(atoms.split(','))))
            for atom in atoms.split(','):
                atom = atom.strip()
                if atom[0].isupper():
                    v.append(Variable())
                elif atom.isdigit():
                    v.append(int(atom))
                else:
                    try:
                        v.append(float(atom))
                    except ValueError:
                        v.append(atom)
            vars.append(v)
        return functors, vars

# test1
instructions1 = 'fi(10, X), f(10, Y), qsort([1,2,9,5,3], Z), coins(A, 100, 500), solve(B)'
instructions = 'parent(ash, X), f(10, Y), solve(Z)'
p = PrologConnecter()
p.consult_file('../coins.pl', delete=False)
p.consult_file('../lst1.pl', delete=False)
p.consult_file('../lst2.pl', delete=False)
p.consult_file('../fib.pl', delete=False)
p.consult_file('../puzzle1.pro', delete=False)
print(p.get_all_ans(instructions1))
from random import shuffle
# # test0
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
# print(fib(0, vars[0]))
# qmfib = Query(mfib(0, vars[0]), fib(10, vars[1]), qsort(a, vars[2]), coins(vars[3], 100, 500), puzzle1(vars[4]))
# while qmfib.nextSolution():
#     print(*map(lambda x: x.value, vars))
# qmfib.closeQuery()