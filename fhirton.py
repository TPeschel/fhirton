import pandas as PA
import re as RE
import requests as REQ
import math as MA
import lxml.etree as LX


def remove_namespaces(xml):
    return RE.sub(' *xmlns *= *"[^"]+ *"', '', xml)


def get_bundle(req: str, rm_ns=True):
    bundle = REQ.get(req)
    bundle_str = str(bundle.content, encoding="utf-8")
    if bundle_str:
        if rm_ns:
            bundle_str = remove_namespaces(bundle_str)
        return LX.fromstring(bundle_str)


def load_bundle(path: str, rm_ns=True):
    bundle = open(path, "r", encoding='utf-8')
    if bundle:
        bundle_str = bundle.read()
        if rm_ns:
            bundle_str = remove_namespaces(bundle_str)
        return LX.fromstring(bundle_str)


def istype(value, types):
    if isinstance(types, list) or isinstance(types, tuple):
        return any([istype(value, t) for t in types])
    return isinstance(value, types)


def which_design(design):
    if istype(design, tuple):
        if 1 < len(design):
            if istype(design[1], dict):
                return 1
            else:
                return 2
        else:
            return 3


def esc(s):
    return RE.sub("([\\.|\\^|\\$|\\*|\\+|\\?|\\(|\\)|\\[|\\{|\\\\\\|\\|])", "\\\\\\1", s)


def rm_indices(df, cols=None, bra=('<', '>')):
    pt =  esc(bra[0]) + "[0-9*.*]{5}" + esc(bra[1])
    if not cols:
        cols = df.columns.values
    
    df = df.replace(to_replace=pt, value='', regex=True)
    return df


def get_name_and_id_from_path(path):
    p = RE.sub('^/[^/]+/', '', path)
    p = RE.sub('([^]])/', '\\1[1]/', p)
    p = RE.sub('([^]])$', '\\1[1]', p)
    p = RE.sub('/', '.', p)
    p = RE.sub('\\[([0-9]+)]', '.\\1', p)
    i = ".".join(RE.findall('[0-9]+', p))
    p = RE.sub('.[0-9]+', '', p)
    return p, i


def resource2row(resource_xml, design, sep, bra, typ, verbose=2):
    rt = LX.ElementTree(resource_xml)
    if typ == 1:
        _ = {}
        for k in design[1].keys():
            xp = design[1][k]
            for u in resource_xml.xpath(xp):
                for attr in u.attrib.values():
                    pt = rt.getpath(u)
                    if bra:
                        n, i = get_name_and_id_from_path(pt)
                        if k in _:
                            _[k] = _[k] + sep + bra[0] + i + bra[1] + attr
                        else:
                            _[k] = bra[0] + i + bra[1] + attr
                    else:
                        if k in _:
                            _[k] = _[k] + sep + attr
                        else:
                            _[k] = attr
        return _
    if 2 <= typ:
        xp = design[1] if typ == 2 else ".//*"
        _ = {}
        res = resource_xml.xpath(xp)
        for u in res:
            for attr in u.attrib.values():
                pt = rt.getpath(u)
                n, i = get_name_and_id_from_path(pt)
                if bra:
                    if n in _:
                        _[n] = _[n] + sep + bra[0] + i + bra[1] + attr
                    else:
                        _[n] = bra[0] + i + bra[1] + attr
                else:
                    if n in _:
                        _[n] = _[n] + sep + attr
                    else:
                        _[n] = attr
        return _


def bundle2table(bundle, design, sep, bra, typ, verbose=2):
    resource_xpath = design[0]
    resources_xml = bundle.xpath(resource_xpath)
    _ = []
    i = 0
    for resource_xml in resources_xml:
        row = resource2row(resource_xml, design, sep, bra, typ, verbose)
        if 2 < verbose:
            if i % 10 == 0:
                print('{:03d}'.format(i), end='')
            if row and any(row):
                print('.', end='')
            else:
                print('x', end='')
            if i % 100 == 99:
                print()
        i += 1
        _.append(row)
    if 1 < verbose:
        print('{:03d}'.format(len(_)))
    return _


def bundles2table(bundles, design, sep, bra, typ=3, verbose=2):
    _ = []
    for bundle in bundles:
        _.extend(bundle2table(bundle, design, sep, bra, typ, verbose))
    if 1 < verbose:
        print('total: {:03d}'.format(len(_)))
    return _


def bundles2tables(bundles, designs, sep, bra=None, verbose=2):
    if 0 < verbose:
        print('Extract bundles to tables.')
    _ = dict()
    for k in designs.keys():
        typ = which_design(designs[k])
        if not typ:
            continue
        if 1 < verbose:
            print(k)
        d = bundles2table(bundles, designs[k], sep, bra, typ, verbose)
        if 1 == typ:
            cn = [n for n in designs[k][1].keys()]
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


def fhir_ton(bundles, designs, sep=' | ', bra=None, verbose=1):
    _ = bundles2tables(bundles=bundles, designs=designs,
                       sep=sep, bra=bra, verbose=verbose)
    return _


def fhir_search(req, verbose=1, max_bundles=MA.inf):
    if 0 < verbose:
        url = RE.sub("(^https*://[^/]+/[^/]+).+", "\\1", req)
        res = RE.sub("(^https*://[^/]+/[^/]+)/([^?]+).*", "\\2", req)
        par = RE.sub("^.*\\?(.*)$", "\\1", req)
        print("Download " +
              ("all" if max_bundles is MA.inf else str(max_bundles)) + " bundles of type: " + res +
              "\nwith search parameters: " + par + "\nfrom fhir endpoint: " + url)
    bundles = []
    r_cnt = 0
    while req:
        if max_bundles <= r_cnt:
            if 0 < verbose:
                print(str(r_cnt) + " bundles downloaded.")
            return bundles
        r_cnt += 1
        if 1 < verbose:
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
                n = s.index('next') if 'next' in s else None
                if n:
                    req = u[n].attrib['value']
    if 0 < verbose:
        print("All (", str(r_cnt) + " ) bundles downloaded.")
    return bundles


    
