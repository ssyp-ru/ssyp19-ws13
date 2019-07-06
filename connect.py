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
    def create_temp_file(code) -> str:  # create temp file for Prolog code

        if 'connect_files' not in os.listdir():  # custom dir
            try:
                os.mkdir('connect_files')
            except PermissionError:
                raise PermissionError("Don't have permission for create a dir")

        file = tempfile.NamedTemporaryFile('w', delete=False, suffix='.pro', dir='connect_files')
        with file as f:
            f.write(code)

        return file.name[file.name.rfind('\\') + 1::]

    def consult_code(self, code: str, delete=True):  # consult Prolog code via temp file
        self.consult_file('connect_files/' + self.create_temp_file(code), delete)

    def consult_file(self, file_name: str, delete=False):
        self.prolog.consult(file_name)
        self.files_name.append((file_name, delete))

    def get_n_ans(self, instructions: str, maxresult=1, **kwargs):  # warning! can be broken if maxresult != 1

        res = list(self.prolog.query(instructions, maxresult=maxresult, **kwargs))  # old simple way

        for file, delete in self.files_name:  # deleting temp files
            if delete:
                os.remove('connect_files\\' + file)
        return res

    # rewrite old way
    def get_all_ans(self, instructions, maxresults=-1) -> list(dict):  # warning! can be broken(x9000)
        functors, items, vars = self.parse_ins(instructions)  # functors and items of predicates, variables
        ans = []  # list of variable values
        q = Query(*(functors[i](*items[i]) for i in range(len(functors))))  # make query
        while q.nextSolution() and maxresults:  # find solutions
            maxresults -= 1
            ans.append({k: v.value for k, v in vars})  # append values
        q.closeQuery()
        return ans

    @staticmethod
    def parse_ins(instruction) -> list and list and list:  # parsing instruction.
        preds = re.findall('(\w[\S]+|\w)\(([\w\d\,\ \[\]]+)\)', instruction)  # find predirects
        functors = []
        items = []
        vars = []
        for pred, atoms in preds:
            atoms = re.findall('\[[\d\w\,]+\]|[\w\d]+',atoms)  # find names(vars|lists|strings|ints) in atoms
            citems = []
            functors.append(Functor(pred, len(atoms)))
            # print(re.findall('\[[\d\w\,]+\]|[\w\d]+',atoms))
            for atom in atoms:
                atom = atom.strip()
                if atom[0].isupper():  # check for var
                    any_var = Variable()  # link to Prologs var
                    citems.append(any_var)
                    vars.append((atom, any_var))
                elif atom.isdigit():  # check for int
                    citems.append(int(atom))
                elif atom[0] == '[' and atom[-1] == ']':  # check for list
                    citems.append(literal_eval(atom))
                else:
                    try:  # check for float
                        citems.append(float(atom))
                    except ValueError:
                        citems.append(atom)
            items.append(citems)
        return functors, items, vars
