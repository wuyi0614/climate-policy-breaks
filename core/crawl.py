# Crawling Script for Asia-Pacific Energy Policy Database (version: December 2019)
#
# Created by Yi Wu in 2019.
#

import json
import time

from datetime import datetime

import requests
import pandas as pd

from tqdm import tqdm
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Connection": "keep-alive",
    'Referer': 'https://asiapacificenergy.org/'
}


# new functions of statistics for crawling
def write(string, file: Path):
    """Write string content into files"""
    file.write_text(string)


def parse(r: requests.Response, root: Path):
    """Customised response parser"""
    cont = r.content
    cont = cont[42:-2]  # ... skip the head and bottom
    d = json.loads(cont)['response']
    # get parsed metadata

    rows = []
    for doc in d['docs']:
        nid = doc['entity_id']
        eng = str(doc.pop('content'))
        raw = str(' '.join(doc.pop('spell')))
        # write the node file:
        # `spell` is written in raw language; `content` is written in english
        write(raw, root / f'node-{nid}-raw.text')
        write(eng, root / f'node-{nid}-eng.text')
        rows += [doc]

    return rows


def get_total(countries: list):
    """
    Get total number of documents listed by asiapacific energy policy portal.
    According to the framework of solr's responses, several attributes should be extracted!

    example:
        https://solr.asiapacificenergy.org/solr/collection1/select?wt=json&fl=id,score,label,url,bs_field_draft,its_field_adoption_year,its_field_effective_start_year,its_field_effective_end_year,sm_field_countries,ss_field_agency,teaser&facet=true&start=0&rows=1000&hl=true&hl.simple.pre=%3Cem%3E&hl.simple.post=%3C%2Fem%3E&hl.usePhraseHighlighter=true&hl.highlightMultiTerm=true&hl.snippets=5&q=(%20its_field_adoption_year:[%201990%20TO%202025%20]%20OR%20its_field_effective_start_year:[*%20TO%20*]%20AND%20NOT%20(its_field_effective_start_year:[2026%20TO%20*%20]%20OR%20its_field_effective_end_year:[*%20TO%201989]%20OR%20(its_field_effective_start_year:[*%20TO%201989]%20AND%20its_field_effective_end_year:[*%20TO%201989])%20OR%20(its_field_effective_start_year:[2026%20TO%20*%20]%20AND%20its_field_effective_end_year:[2026%20TO%20*%20]))%20)&fq=sm_field_countries:(%22CHN%22)&sort=score+desc&json.wrf=jQuery214046485703155566505_1736410735395&_=1736410735397
    """
    url = 'https://solr.asiapacificenergy.org/solr/collection1/select'
    skip = ['id', 'site', 'hash', 'entity_type', 'bundle', 'bundle_name', 'path',
            'ss_name_formatted', 'ss_name', 'tos_name', 'bs_status',
            'bs_sticky', 'bs_promote', 'is_tnid', 'bs_translate', '_version_']
    o1 = ['entity_id', 'ss_language', 'url', 'label', 'teaser', 'tos_name_formatted', 'is_uid', 'ds_created',
          'ds_changed', 'ds_last_comment_or_change', 'bm_field_draft', 'bs_field_draft', 'sm_field_countries',
          'itm_field_adoption_year', 'its_field_adoption_year', 'sm_field_energy_types', 'sm_field_document_type',
          'sm_field_related_documents', 'sm_field_scope', 'bm_field_revision', 'bs_field_revision',
          'sm_field_economic_sector', 'itm_field_effective_start_year', 'its_field_effective_start_year',
          'ss_field_agency', 'ss_field_title_in_english', 'timestamp', 'ss_field_notes',
          'itm_field_effective_end_year', 'its_field_effective_end_year', 'ss_field_title_national_language']
    o2 = ['ts_field_EA1', 'ts_field_EA2', 'ts_field_EA3', 'ts_field_EA4', 'ts_field_EA5', 'ts_field_EA6',
          'ts_field_EA7', 'ts_field_EE1', 'ts_field_EE2', 'ts_field_EE3', 'ts_field_EE4', 'ts_field_EE5',
          'ts_field_EE6', 'ts_field_EE7', 'ts_field_EE8', 'ts_field_EE9', 'ts_field_EE10', 'ts_field_EE11',
          'ts_field_EE12', 'ts_field_EE13', 'ts_field_EN00', 'ts_field_EN1', 'ts_field_EN2',
          'ts_field_EN3', 'ts_field_EN4', 'ts_field_EN5', 'ts_field_EN6', 'ts_field_EN7', 'ts_field_EN8',
          'ts_field_EN9', 'ts_field_EN10', 'ts_field_ES1', 'ts_field_ES2', 'ts_field_ES3', 'ts_field_ES4',
          'ts_field_ES5', 'ts_field_ES6', 'ts_field_GV1', 'ts_field_GV2', 'ts_field_GV3', 'ts_field_GV4',
          'ts_field_GV5', 'ts_field_GV6', 'ts_field_GV7', 'ts_field_GV8', 'ts_field_IN1', 'ts_field_IN10',
          'ts_field_IN11', 'ts_field_IN12', 'ts_field_IN2', 'ts_field_IN3', 'ts_field_IN4', 'ts_field_IN5',
          'ts_field_IN6', 'ts_field_IN7', 'ts_field_IN8', 'ts_field_IN9', 'ts_field_PR1', 'ts_field_PR2',
          'ts_field_PR3', 'ts_field_PR4', 'ts_field_PR5', 'ts_field_PR6', 'ts_field_RE1',
          'ts_field_RE2', 'ts_field_RE3', 'ts_field_RE4', 'ts_field_RE5', 'ts_field_RE6', 'ts_field_RE7',
          'ts_field_RE8', 'ts_field_RE9', 'ts_field_RE10', 'ts_field_RE11',
          'ts_field_RE12', 'ts_field_RE13', 'ts_field_RE14', 'ts_field_RE15', 'ts_field_RE16',
          'ts_field_RE17', 'ts_field_TC1', 'ts_field_TC2', 'ts_field_TC3', 'ts_field_TC4', 'ts_field_TC5',
          'ts_field_TC6', 'ts_field_TC7', 'ts_field_TC8', 'ts_field_TC9', 'ts_field_TC10', 'ts_field_TC11',
          'ts_field_TC12', 'ts_field_TC13', 'ts_field_TC14', 'ts_field_TR1', 'ts_field_TR2',
          'ts_field_TR3', 'ts_field_TR4', 'ts_field_TR5', 'ts_field_TR6', 'ts_field_TR7']

    rows = []
    for c in tqdm(countries, desc="Downloading"):
        # make requests
        param = ['wt=json', 'facet=false', 'start=0', 'rows=1000',
                 f'fq=sm_field_countries:(%22{c}%22)',
                 'json.wrf=jQuery214046485703155566505_1736410735395',
                 '_=1736410735397']
        u = url + '?' + '&'.join(param)
        r = requests.get(u, headers=HEADERS)
        # parse response
        root = Path('data') / 'national' / 'apac-update' / c
        root.mkdir(parents=True, exist_ok=True)
        rows += parse(r, root)
        time.sleep(8)

    out = pd.DataFrame(rows)
    out = out[o1 + o2]
    ts = datetime.now().strftime("%m%d")
    out.to_excel(f'data/national/apac-full-{ts}.xlsx', index=False)
    # delete columns
    out.drop(labels=skip, axis=1, inplace=True)
    out.to_excel(f'data/national/apac-metadata-{ts}.xlsx', index=False)
    return out


if __name__ == "__main__":
    # load countries' ISO
    cfile = Path('data') / 'national' / 'country-iso.txt'
    countries = cfile.read_text().split("\n")
    rows = get_total(countries)
