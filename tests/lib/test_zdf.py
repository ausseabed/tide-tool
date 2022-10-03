import pytest

from tidetool.lib.zdf import ZdfParser, ZoneDefinitionFile, \
    ZdfTideStation, ZdfParsingException
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

    assert len(zdf.blocks) == 5


def test_zdf_tidestation():
    lines = [
        "tide11,-13.954114,141.055087,0.0,0.01,ga0276_11_msl.tid",
        "tide12,-12.707922,141.676960,0.0,0.01,ga0276_12_msl.tid"
    ]
    
    ts = ZdfTideStation('TIDE_STATION')
    ts.from_strings(lines)

    assert ts.data[0][0] == "tide11"
    assert ts.data[0][1] == -13.954114
    assert ts.data[1][5] == "ga0276_12_msl.tid"


def test_zdf_tidestation_exceptions():
    # string where a float is expected
    lines = [
        "tide11,asddf,141.055087,0.0,0.01,ga0276_11_msl.tid",
    ]
    ts = ZdfTideStation('TIDE_STATION')

    with pytest.raises(ZdfParsingException) as e_info:
        ts.from_strings(lines)

    # 5 segments where 6 is expected
    lines = [
        "tide11,-13.0,141.055087,0.01,ga0276_11_msl.tid",
    ]
    with pytest.raises(ZdfParsingException) as e_info:
        ts.from_strings(lines)
