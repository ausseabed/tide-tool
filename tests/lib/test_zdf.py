import pytest

from tidetool.lib.zdf import ZdfParser, ZoneDefinitionFile
from tests.lib.mock_data import mock_data_01


def test_zdfparser_gettype():
    parser = ZdfParser()

    assert parser._get_type('  a   [ZONE]     d    ') == 'ZONE'
    assert parser._get_type('[ZONE]') == 'ZONE'
    assert parser._get_type('[FOO BAR]') == 'FOO BAR'
    

def test_zdf_parser_processlines():

    zdf = ZoneDefinitionFile(filename=None)
    parser = ZdfParser()
    parser.zdf = zdf

    parser._process_lines(mock_data_01)
    print(zdf.blocks)
    assert len(zdf.blocks) == 5

