import xml.etree.ElementTree as ET
import pandas as PA
# import xml.parsers.expat as EP
import re as RE
import os
import requests as REQ
from typing import Dict, Any


def which(x, y):
    f = [z == y for z in x]
    i = 0
    for z in x:
        if z == y:
            return i
            break
        i += 1

    return None


def get_bundle(req):
    bundle = REQ.get(req)
    bundle_str = str(bundle.content, encoding="utf-8")
    if bundle_str:
        bundle_str = RE.sub('\s*xmlns\s*=\s*"[^"]+\s*"', '', bundle_str)
        return ET.fromstring(bundle_str)
    return None


def load_bundle(path: str):
    bundle_str = open(path, "r", encoding='utf-8')
    if bundle_str:
        bundle_str = bundle_str.read()
        bundle_str = RE.sub('\s*xmlns\s*=\s*"[^"]+\s*"', '', bundle_str)
        return ET.fromstring(bundle_str)
    return None


def bundle2df(bundle, design_df, sep=' '):
    xpath_resource = design_df[0]
    table_design = design_df[1]

    xml_res = bundle.findall(xpath_resource)

    if 0 < len(xml_res):

        df = [[0 for x in range(len(table_design.keys()))] for y in range(len(xml_res))]

        row = 0
        for r in xml_res:
            col = 0
            for col_name in table_design.keys():
                # xp = RE.sub("/@[-\w]+$", "", table_design[col_name])
                xp = table_design[col_name]
                y = r.findall(xp)
                z = [x.attrib['value'] if 'value' in x.attrib else 'NA' for x in y]
                df[row][col] = sep.join(z)
                col += 1
            row += 1

        df = PA.DataFrame(df)
        df.columns = [str(k) for k in table_design.keys()]

        return df

    return None


def fhir_search(req):
    bundles = []

    r_cnt = 0

    while req:
        r_cnt += 1
        print(str(r_cnt) + " : " + req)
        bundle = get_bundle(req=req)
        req = None
        if bundle:
            bundles.append(bundle)
        r = bundle.findall(".//link/relation")

        if r:
            u = bundle.findall(".//link/url")
            s = [x.attrib['value'] for x in r]
            if 0 < len(s):
                n = which(s, 'next')
                if n:
                    req = u[n].attrib['value']

    return bundles


def fhir_table(bundles, design, sep=' '):
    dfs = [[bundle2df(bundle, design[k], sep) for bundle in bundles] for k in design.keys()]

    dfs = dict([(d[1], PA.concat(d[0])) for d in zip(dfs, design.keys())])

    return dfs
