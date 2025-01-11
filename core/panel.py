# This script panelises the metadata of energy policies
#
# Created by Yi at 28/12/2024.
#

import json

from tqdm import tqdm
from pathlib import Path
from collections import Counter

import pandas as pd
import numpy as np

from core.utils import init_logger

# general logging config
logger = init_logger('preprocessing')

# fields of metadata json
""" Fields with optional status
Country: string (when it's a national/local document); a list of strings (when it's a multi-lateral document)
Title: optional, title of the document or report
Files: optional, links
Draft: Yes or No
Draft Year: 2007
Revision of previous policy?: Yes or No
Effective Start Year: numeric, int
Scope: multilateral or others
Document Type: string, e.g, Plan, Regulatory, Law
Economic Sector: a list of multiple sectoral names, e.g., Energy, Power, Industry, Transport, Multi-Sector, Other
Energy Types: a list of energy types, e.g., Power, Gas, Other
Issued by: string, a person or authority
Source: ignored 
File: ignored (string), filename 
Overall Summary: ignored
Full Document Text: optional
"""

VALID_META = ['Country', 'Issued by', 'Title', 'Draft Year', 'Effective Start Year', 'Effective End Year',
                'Scope', 'Document Type', 'Economic Sector', 'Energy Types', 'Revision of previous policy?']
VALID_FIELDS = ['Governance', 'Renewable Energy', 'Efficiency', 'Environment', 'Investment', 'Pricing',
                'Technology', 'Access', 'Trade', 'Energy Supply and Infrastructure']

def read(root: Path):
    """Read metadata from local storage."""
    temp_keys = []
    temp_fields = []
    rows = []  # ... final outputs organised by rows
    for each in tqdm(root.glob(r'node_*'), desc='File loading', leave=True):
        # ... put each column of data in the `row` item
        # [node, <metadata>, <fields>] as the format leaving missing values as empty
        row = [each.name]

        # ... each item is a folder, and there are 4,398 documents in total!
        found = each.glob('metadata*.json')
        found = list(found)
        if not found:
            logger.warning(f'No metadata found in {str(each)}')

        # read and process the file content
        f = found.pop()
        f = json.loads(f.read_text())

        # regarding `Other fieldsets`, use prefix: `aspect_<xxx>`
        temp_keys += list(f['Metadata'].keys())
        temp_fields += list(f['Other fieldsets'].keys())

        # collect the info of interest in the following format:
        for k in VALID_META:
            row += [f['Metadata'].get(k, np.nan)]

        for k in VALID_FIELDS:
            row += [f['Other fieldsets'].get(k, np.nan)]

        rows += [row]

    # panelise the final output with some rows being empty
    out = pd.DataFrame(rows, columns=['Node'] + VALID_META + VALID_FIELDS)
    print(out[out.Country.isna()].shape)
    # ... reporting
    logger.info(f'Fieldsets: {Counter(temp_fields)}')
    logger.info(f'Metadata: {Counter(temp_keys)}')
    return

def extend_panel():
    """Extend the basic panel into an extensive mode where each policy element has been aligned

    example: https://asiapacificenergy.org/apef/index.html#main/lang/en/time/[1990,2025]/geo/[THA]/matrix
    """

    return


if __name__ == '__main__':
    # various tests should be implemented here
    root = Path('data') / 'national' / 'apac-data'
