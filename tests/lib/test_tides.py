from datetime import date, timedelta
from tidetool.lib.tides import _generate_annual_dates

def test_dates_generation():
    dates = _generate_annual_dates(2008, 10)

    # it's all within a year, so both start and
    # end dates should be 2008
    assert dates[0].year == 2008
    assert dates[-1].year == 2008

    # if every ten minutes there should be this many
    # datetimes in the list
    assert len(dates) == 6 * 24 * 365

    

    dates = _generate_annual_dates(2009, 30)

    assert dates[1] - dates[0] == timedelta(minutes=30)

    # if every ten minutes there should be this many
    # datetimes in the list
    assert len(dates) == 2 * 24 * 365
