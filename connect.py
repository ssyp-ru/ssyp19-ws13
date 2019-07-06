from pyswip import Prolog, Query, Variable, Functor
import tempfile
import re
import os
from ast import literal_eval


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

    def get_all_ans(self, instructions, maxresults=-1):
        functors, items, vars = self.parse_ins(instructions)
        ans = []
        q = Query(*(functors[i](*items[i]) for i in range(len(functors))))
        while q.nextSolution() and maxresults:
            maxresults -= 1
            ans.append({k: v.value for k, v in vars})
        q.closeQuery()
        return ans

    @staticmethod
    def parse_ins(instruction):
        preds = re.findall('(\w[\S]+|\w)\(([\w\d\,\ \[\]]+)\)', instruction)
        functors = []
        items = []
        vars = []
        for pred, atoms in preds:
            atoms = re.findall('\[[\d\w\,]+\]|[\w\d]+',atoms)
            citems = []
            functors.append(Functor(pred, len(atoms)))
            # print(re.findall('\[[\d\w\,]+\]|[\w\d]+',atoms))
            for atom in atoms:
                atom = atom.strip()
                if atom[0].isupper():
                    any_var = Variable()
                    citems.append(any_var)
                    vars.append((atom, any_var))
                elif atom.isdigit():
                    citems.append(int(atom))
                elif atom[0] == '[' and atom[-1] == ']':
                    citems.append(literal_eval(atom))
                else:
                    try:
                        citems.append(float(atom))
                    except ValueError:
                        citems.append(atom)
            items.append(citems)
        return functors, items, vars
