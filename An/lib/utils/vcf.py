import codecs
import collections
import re
Contact = collections.namedtuple('Contact', 'name phone')


class Vcf(object):
    BEGIN = 'BEGIN:VCARD'
    VERSION = 'VERSION:2.1'
    END = 'END:VCARD'
    STRING = ';CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:'
    N = 'N' + STRING
    FN = 'FN' + STRING
    TEL = 'TEL;VOICE;PREF:'

    __slots__ = ()

    def encode_string(text):
        return codecs.escape_encode(text.encode('UTF-8'))[0].decode().replace('\\x', '=').upper()

    def decode_string(text):
        return codecs.escape_decode(text.replace('=', '\\x'))[0].decode()

    @classmethod
    def fromtext(cls, text):
        items = []
        for line in text.splitlines():
            if line.startswith(cls.BEGIN):
                item = Contact()
            elif line.startswith(cls.N):
                # item.name
                name = line[len(cls.N):].replace(';', '')
                if re.match('(=[\\da-fA-F])+', name):
                    name = __class__.decode_string(name)
                item.name = name
            elif line.startswith(cls.TEL):
                item.phone = line[len(cls.TEL):]
            elif line.startswith(cls.END):
                items.append(item)
        return items

    @classmethod
    def totext(cls, items, utf8=True, end='\n'):
        result = []
        for item in items:
            result.append(cls.BEGIN)
            result.append(cls.VERSION)
            name = __class__.encode_string(item.name) if utf8 else item.name
            result.append(cls.N + name)
            result.append(cls.FN + name)
            result.append(cls.TEL + item.phone)
            result.append(cls.END)
        return end.join(result)

    def __repr__(self):
        return str({key: getattr(self, key) for key in __class__.__slots__})

    __str__ = __repr__


if __name__ == '__main__':
    raw = """
    BEGIN:VCARD
    VERSION:2.1
    N;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=E5=85=B0=E6=A0=BC;=E8=82=96;;;
    FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=E5=85=B0=E6=A0=BC=20=E8=82=96
    TEL;VOICE;PREF:1-352-013-0000
    END:VCARD
    BEGIN:VCARD
    VERSION:2.1
    N;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:;=E9=98=BF=E5=87=AF=32=30=30=39;;;
    FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=E9=98=BF=E5=87=AF=32=30=30=39
    TEL;VOICE;PREF:1-234-567-8900
    END:VCARD
    BEGIN:VCARD
    VERSION:2.1
    N;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:;=E7=A7=91=E6=8A=80=E6=B3=A2;;;
    FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=E7=A7=91=E6=8A=80=E6=B3=A2
    TEL;VOICE;PREF:1-328-354-0000
    END:VCARD
    """

    print(Vcf.fromtext(raw))
