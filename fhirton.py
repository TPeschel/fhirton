from itertools import chain
import pandas as PA
import re as RE
import requests as REQ
import math as MA
import lxml.etree as LX


def which_1st(x, y):
    return x.index(y) if y in x else None


def which_all(x, y):
    _ = []
    for __ in range(len(x)):
        if x[__] == y:
            _.append(__)
    return _


def which_fun(x, fun):
    _ = []
    for __ in range(len(x)):
        if fun(x[__]):
            _.append(__)
    return _


def list_fun(val_list, fun):
    return [fun(v) for v in val_list]


def log_from_list(val_list, fun):
    _ = []
    for v in val_list:
        if fun(v):
            _.append(v)
    return _


def list_sel_id(val_list, id_list):
    return [val_list[_] if _ in range(len(val_list)) else None for _ in id_list]


def list_sel_log(val_list, log_list):
    return list_sel_id(val_list, [_ for _ in which_all(log_list, True)])


def dict_sel_key(val_list, id_list):
    return [val_list[_] if _ in val_list.keys() else None for _ in id_list]


def dict_sel_id(val_list, id_list):
    return [val_list[_] if _ in val_list.keys() else None for _ in id_list]


def dict_sel_log(val_list, log_list):
    _ = []
    for __, ___ in zip(val_list.keys(), log_list):
        if ___:
            _ = [*_, val_list[__]]
    return _


def get_bundle(req: str):
    bundle = REQ.get(req)
    bundle_str = str(bundle.content, encoding="utf-8")
    if bundle_str:
        bundle_str = RE.sub('\s*xmlns\s*=\s*"[^"]+\s*"', '', bundle_str)
        return LX.fromstring(bundle_str)


def load_bundle(path: str):
    bundle_str = open(path, "r", encoding='utf-8')
    if bundle_str:
        bundle_str = bundle_str.read()
        bundle_str = RE.sub('\s*xmlns\s*=\s*"[^"]+\s*"', '', bundle_str)
        return LX.fromstring(bundle_str)


def which_design(design):
    if design and type(design) == tuple:
        if 1 < len(design):
            if dict == type(design[1]):
                return 1
            else:
                return 2
        else:
            return 3


def list2string(lst, sep):
    return sep.join([str(s) for s in lst]) if lst and list == type(lst) else lst


def path2name(path):
    p = RE.sub('^/[^/]+/', '', path)
    p = RE.sub('([^]])/', '\\1[1]/', p)
    p = RE.sub('([^]])$', '\\1[1]', p)
    p = RE.sub('/', '.', p)
    p = RE.sub('\\[([0-9]+)]', '.\\1', p)
    i = ".".join(RE.findall('[0-9]+', p))
    p = RE.sub('.[0-9]+', '', p)
    return p, i




def row2table(row_xml, design, sep, typ):
    rt = LX.ElementTree(row_xml)
    if typ == 1:
        _ = {}
        for k in design[1].keys():
            xp = design[1][k]
            for u in row_xml.xpath(xp):
                if 'value' in u.attrib:
                    pt = rt.getpath(u)
                    n, i = path2name(pt)
                    attr = u.attrib['value']
                    if k in _:
                        _[k] = _[k] + sep + '[' + i + ']' + attr
                    else:
                        _[k] = '[' + i + ']' + attr
        return _
    if 2 <= typ:
        xp = design[1] if typ == 2 else ".//*"
        _ = {}
        for u in row_xml.xpath(xp):
            if 'value' in u.attrib:
                pt = rt.getpath(u)
                n, i = path2name(pt)
                attr = u.attrib['value']
                if n in _:
                    _[n] = _[n] + sep + '[' + i + ']' + attr
                else:
                    _[n] = '[' + i + ']' + attr
        return _


def bundle2table(bundle, design, sep, typ):
    xp_res = design[0]
    xml_res = bundle.xpath(xp_res)
    _ = []
    for row in xml_res:
        _.append(row2table(row, design, sep, typ))
    return _
    # return [row2table(row, design, sep, typ) for row in xml_res]


def bundles2table(bundles, design, sep, typ):
    _ = []
    for bundle in bundles:
        _.extend(bundle2table(bundle, design, sep, typ))
    print('#', end='')
    return _


#    return [bundle2table(bundle, design, sep, typ) for bundle in bundles]


def bundles2tables(bundles, designs, sep):
    _ = dict()
    for k in designs.keys():
        typ = which_design(designs[k])
        d = bundles2table(bundles, designs[k], sep, typ)
        if 1 == typ:
            cn = [n for n in designs[k][1].keys()]
            tb = dict([(k, list()) for k in cn])
        else:
            cn = []
            for e in d:
                cn.extend(e.keys())
            cn = list(set(cn))
        tb = dict([(k, list()) for k in cn])
        for n in cn:
            tb[n] = [e[n] if n in e.keys() else None for e in d]
        __ = PA.DataFrame(tb)
        if 1 < typ:
            n = __.columns.values
            for i in n:
                if __[i].isna().all():
                    __ = __.drop(columns=i)
        _[k] = __
    return _

def rm_indices(df, cols=None):
    if cols:
        for c in cols:
            df[c] = [RE.sub('\\[[0-9+.]+]', '', d) if d else None for d in df[c]]
    else:
        for c in df.columns.values :
            df[c] = [RE.sub('\\[[0-9+.]+]', '', d) if d else None for d in df[c]]
    return df

def fhir_ton(bundles, designs, sep=' '):
    _ = bundles2tables(bundles, designs, sep)
    return _


# def dsgn1(bundle, design1_df, sep=' '):
#     xpath_resource = design1_df[0]
#     xml_res = bundle.findall(xpath_resource)
#     table_design = design1_df[1]
#     if 0 < len(xml_res):
#         df = [[0 for x in range(len(table_design.keys()))] for y in range(len(xml_res))]
#         row = 0
#         for r in xml_res:
#             col = 0
#             for col_name in table_design.keys():
#                 xp = table_design[col_name]
#                 y = r.findall(xp)
#                 z = [x.attrib['value'] if 'value' in x.attrib else '' for x in y]
#                 df[row][col] = sep.join(z)
#                 col += 1
#             row += 1
#         df = PA.DataFrame(df)
#         df.columns = [str(k) for k in table_design.keys()]
#         return df
#
#
# #   return None
#
# def dsgn2(bundle, design2_df, sep=' '):
#     xpath_resource = design2_df[0]
#     xml_res = bundle.xpath(xpath_resource)
#
#     xp_col = design2_df[1]
#
#     nv = []
#     if 0 < len(xml_res):
#         for r in xml_res:
#             res = r.xpath(xp_col)
#             rt = LX.ElementTree(r)
#             nv.append(
#                 dict([(RE.sub("(\\[)([0-9]+)(])", ".\\2", RE.sub("/", ".", RE.sub("^/[^/]+/", "", rt.getpath(e)))),
#                        e.attrib['value'] if 'value' in e.attrib else PA.NA) for e in res]))
#
#     cn = []
#     for i in nv:
#         cn.append([i for i in i.keys()])
#     cn.sort()
#
#     df = [[y[x] for x in cn] for y in nv]
#     df = PA.DataFrame(df)
#
#     n = df.columns.values
#     for i in n:
#         if df[i].isna().all():
#             df = df.drop(columns=i)
#     return df
#
#
# """        df = [[0 for x in range(len(table_design.keys()))] for y in range(len(xml_res))]
#         row = 0
#         for r in xml_res:
#             col = 0
#             for col_name in table_design.keys():
#                 xp = table_design[col_name]
#                 y = r.findall(xp)
#                 z = [x.attrib['value'] if 'value' in x.attrib else '' for x in y]
#                 df[row][col] = sep.join(z)
#                 col += 1
#             row += 1
#         df = PA.DataFrame(df)
#         df.columns = [str(k) for k in table_design.keys()]
#         return df
#  #   return None
# """
#
#
# def dsgn3(bundle, design2_df, sep=' '):
#     xpath_resource = design2_df[0]
#     xml_res = bundle.xpath(xpath_resource)
#
#
# def bundle2df(bundle, design_df, sep=' '):
#     if 1 < len(design_df):
#         table_design = design_df[1]
#         if list == type(table_design):
#             return dsgn1(bundle, design_df, sep=sep)
#         else:
#             return dsgn2(bundle, design_df, sep=sep)
#     return dsgn3(bundle, design_df, sep=sep)


def fhir_search(req, max_bundles=MA.inf):
    bundles = []
    r_cnt = 0
    while req:
        if max_bundles <= r_cnt:
            print(str(r_cnt) + " bundles downloaded.")
            return bundles
        r_cnt += 1
        print(str(r_cnt) + " : " + req)
        bundle = get_bundle(req=req)
        req = None
        if 0 < len(bundle):
            bundles.append(bundle)
        r = bundle.xpath(".//link/relation")
        if r:
            u = bundle.xpath(".//link/url")
            s = [x.attrib['value'] for x in r]
            if 0 < len(s):
                n = which_1st(s, 'next')
                if n:
                    req = u[n].attrib['value']
    print("All (", str(r_cnt) + " ) bundles downloaded.")
    return bundles

# def fhir_ton(bundles, design, sep=' '):
#     dfs = [[bundle2df(bundle, design[k], sep) for bundle in bundles] for k in design.keys()]
#     dfs = dict([(d[1], PA.concat(d[0])) for d in zip(dfs, design.keys())])
#     return dfs
