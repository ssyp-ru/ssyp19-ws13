from pyswip import Prolog, Query, Variable, Functor, call
import tempfile
import re
import os
from ast import literal_eval


class PrologConnector:

    def __init__(self):
        self.prolog = Prolog()

    @staticmethod
    def create_temp_file(code) -> str:  # create temp file for Prolog code

        if 'connect_files' not in os.listdir():  # custom dir
            try:
                os.mkdir('connect_files')
            except PermissionError:
                raise PermissionError("Don't have permission for create a dir")

        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.pro', dir='connect_files') as file:
            file.write(code)
            return file.name[file.name.rfind('\\') + 1::]

    def consult_code(self, code: str, delete=True):  # consult Prolog code via temp file
        self.consult_file('connect_files/' + self.create_temp_file(code), delete)

    def consult_file(self, file_name: str, delete=False):
        self.prolog.consult(file_name)
        if delete:
            os.remove(file_name)

    def get_n_ans(self, instructions: str, maxresult=1, **kwargs) -> [dict]:  # warning! can be broken if maxresult != 1

        return self.prolog.query(instructions, maxresult=maxresult, **kwargs)  # old simple way

    # rewrite old way
    def get_n_ans_new(self, instructions: str, maxresults=-1, solves=True) -> list:  # warning! can be broken(x9000)
        terms, vars, statements = self.parse_ins(instructions)  # functors and items of predicates, variables
        vars_ans = [] if solves else {i[0]: [] for i in vars}  # list of variable values
        statements_ans = {}  # list of statements
        if terms:
            q = Query(*terms)  # make query
            while q.nextSolution() and maxresults:  # find solutions
                maxresults -= 1
                if solves:
                    vars_ans.append({k: v.value for k, v in vars})  # append values
                else:
                    for k, v in vars:
                        vars_ans[k].append(v.value)
            q.closeQuery()
        if statements:
            for statement in statements:
                statements_ans.update({statement[1]: call(statement[0])})
        return vars_ans, statements_ans

    @staticmethod
    def parse_ins(instruction) -> list and list and list:  # parsing instruction.
        terms = []  # if need var(s)
        vars = []
        statements = []  # if need True or False
        for pred, atoms in re.findall('([^\(\)\,\s]+|\S)(\([\w\d\,\ \[\]]+\))', instruction):  # find predirects
            names = re.findall('\[[\d\w\,]+\]|[\w\d]+', atoms)  # find names(vars|lists|strings|ints) in atoms
            items = []
            there_is_var = False
            for atom in names:
                atom = atom.strip()

                if atom[0].isupper():  # check for var
                    any_var = Variable()  # link to Prologs var
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

    def make_req(self, command, solve=False):
        a = self.get_n_ans_new(command, maxresults=-1, solve=solve)
        if a[0]:
            return a[0]
        else:
            for i in a[1].values():
                return i

    def assert_code(self, ins):
        for i in ins.split(','):
            self.prolog.assertz(i)