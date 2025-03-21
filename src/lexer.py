from sly import Lexer

class DPLexer(Lexer):
    tokens = {
            ID, OPCODE, RAW_DATA,
            REGISTER, REL,
            LABEL, NUMBER, CONDITION,
            LBRACKET, RBRACKET, PLUS,
            PREPROC_DIRECTIVE # директива препроцессору
            }
    ignore = ' \t\n'
    ignore_comment = r';.*'

    @_(r"#\w*")
    def PREPROC_DIRECTIVE(self, t):
        t.value = t.value[1:]
        return t

    @_(r'r\d+')
    def REGISTER(self, t):
        if not 0x00 <= int(t.value[1:]) <= 0xFF:
            raise ValueError("Пожалуйста, исопльзуйте регистры из набора r1-r256")
        return t
    @_(r'[_a-zA-Z]\w*:')
    def LABEL(self, t):
        t.value = t.value[:-1]
        return t

    ID = r'[_a-zA-Z]\w*'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    PLUS = r'\+'

    @_(r'{i=[01][Vv]?[Nn]?[Zz]?}')
    def CONDITION(self, t):
        cond: str = t.value
        cond = cond[3:-1].lower()
        result = int(cond[0]) << 3
        result += 1 << 2 if 'v' in cond else 0
        result += 1 << 1 if 'n' in cond else 0
        result += 1 << 0 if 'z' in cond else 0
        t.value = result
        return t

    ID['add'] = OPCODE
    ID['sub'] = OPCODE
    ID['mul'] = OPCODE
    ID['div'] = OPCODE
    ID['and'] = OPCODE
    ID['or'] = OPCODE
    ID['xor'] = OPCODE
    ID['mask'] = OPCODE
    ID['load'] = OPCODE
    ID['store'] = OPCODE
    ID['branch'] = OPCODE
    ID['db'] = RAW_DATA
    ID['dh'] = RAW_DATA
    ID['dw'] = RAW_DATA
    ID['rel'] = REL

    @_(r"0x[0-9a-f]+",
       r"-?\d+")
    def NUMBER(self, t):
        if t.value.startswith("0x"):
            t.value = int(t.value, 16)
        else:
            t.value = int(t.value)
        return t


if __name__ == "__main__":
    l = DPLexer()
    prog = "-1"
    print(*l.tokenize(prog))
