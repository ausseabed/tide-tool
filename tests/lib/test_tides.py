from datetime import datetime, timedelta
from tidetool.lib.tides import \
    _generate_annual_dates, _generate_dates_between


def test_dates_generation_annual():
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


def test_dates_generation_between():
    start_date = datetime(2000, 1, 1)
    end_date = datetime(2000, 1, 6)
    dates = _generate_dates_between(start_date, end_date, 60)

    # 5 days, every 60 minutes (hour)
    assert len(dates) == 5 * 24

    assert dates[0] == datetime(2000, 1, 1, 0, 0, 0)
    assert dates[1] == datetime(2000, 1, 1, 1, 0, 0)
    assert dates[-1] == datetime(2000, 1, 5, 23, 0, 0)
