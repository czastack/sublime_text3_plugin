import re
from array import array


def strsq(a, b, split=''):
    """生成字符序列"""
    def check_param(ch):
        ok = False
        if isinstance(ch, str):
            if len(ch) == 1:
                ch = ord(ch)
                ok = True
        elif isinstance(ch, int):
            ok = True
        if ok:
            return ch
        else:
            raise ValueError('参数必须是字符或者整数')
    a = check_param(a)
    b = check_param(b)
    if a > b:
        a, b = b, a
    sq = (chr(x) for x in range(a, b + 1))
    return split.join(sq) if isinstance(split, str) else sq


def str2codes(s):
    return [ord(ch) for ch in s]


def codes2str(cs):
    return ''.join(chr(c) for c in cs)


def matchAll(reg, text, fn):
    if isinstance(fn, (list, tuple)):
        arg = fn

        def fn(x):
            return [x.group(i) for i in arg]

    elif isinstance(fn, int):
        arg = fn

        def fn(x):
            return x.group(arg)

    return [fn(m) for m in re.finditer(reg, text)]


def replace(s, rulers):
    """字符串批量替换"""
    for patterm, rep in rulers:
        s = re.sub(patterm, rep, s)
    return s


def toggle_bc_case(text, sbc=True, dbc=True):
    """切换全角半角
    :param sbc: 全角转换成半角
    :param dbc: 半角转换成全角
    """
    result = array('u', text)
    for i in range(len(result)):
        ch = ord(result[i])
        if sbc and 32 < ch < 127:
            ch += 65248
        elif dbc and 65280 < ch < 65375:
            ch -= 65248
        result[i] = chr(ch)
    return result.tounicode()
