from connect import PrologConnecter


class Translator:

    def __init__(self):
        pass

    def eat(self, something):
        # TODO: Parse ↑↑↑ this
        parsed = self.parse_food(something)
        instructions: str = parsed
        out = self.connect_to_prolog(instructions)
        self.feedback(...)
        return out

    # TODO: Write me
    def parse_food(self, food):
        pass

    # TODO: Write me
    def feedback(self, cls):
        pass

    @staticmethod
    def connect_to_prolog(instructions: str, results=-1) -> [dict]:
        pc = PrologConnecter()
        pc.consult_file('Prolog/Axioms.pro')
        pc.consult_file('Prolog/Something')
        return pc.get_all_ans(instructions, maxresults=results)  # FIXME: may be unfinished(and broken)
