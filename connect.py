from pyswip import Prolog, Query, Variable, Functor, call
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
                os.remove(file)
        return res

    # rewrite old way
    def get_all_ans(self, instructions, maxresults=-1) -> list:  # warning! can be broken(x9000)
        terms, vars, statements = self.parse_ins(instructions)  # functors and items of predicates, variables
        # print(terms,vars,statements)
        vars_ans = []  # list of variable values
        statements_ans = {}  # list of statements
        if terms:
            q = Query(*terms)  # make query
            while q.nextSolution() and maxresults:  # find solutions
                maxresults -= 1
                vars_ans.append({k: v.value for k, v in vars})  # append values
            q.closeQuery()
        if statements:
            for statement in statements:
                statements_ans.update({statement[1]: call(statement[0])})
        return vars_ans, statements_ans

    @staticmethod
    def parse_ins(instruction) -> list and list and list:  # parsing instruction.
        preds = re.findall('([^\(\)\,\s]+|\S)(\([\w\d\,\ \[\]]+\))', instruction)  # find predirects
        terms = []  # if need var(s)
        vars = []
        statements = []  # if need True or False
        for pred, atoms in preds:
            names = re.findall('\[[\d\w\,]+\]|[\w\d]+', atoms)  # find names(vars|lists|strings|ints) in atoms
            items = []
            there_is_var = False
            for atom in names:
                atom = atom.strip()
                if atom[0].isupper():  # check for var
                    any_var = Variable()  # link to Prolog var
                    items.append(any_var)
                    vars.append((atom, any_var))
                    there_is_var = True
                elif atom.isdigit():  # check for int
                    items.append(int(atom))
                elif atom[0] == '[' and atom[-1] == ']':  # check for list
                    items.append(literal_eval(atom))
                else:
                    try:  # check for float
                        items.append(float(atom))
                    except ValueError:
                        items.append(atom)
            if there_is_var:
                terms.append(Functor(pred, len(names))(*items))
            else:
                statements.append((Functor(pred, len(names))(*items), pred + atoms))
        return terms, vars, statements
