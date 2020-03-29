import collections
import datetime

COUNTRY_COLOR = collections.defaultdict(lambda: 'k')
COUNTRY_COLOR.update({"US": "C0", "France": "C1", "Italy": "C2",
                      "China": "C3", "India": "C4", "Spain": "C5",
                      "Germany": "C6"})

LOCKDOWN_DATES = collections.defaultdict(list)
LOCKDOWN_DATES.update({
    'China': [datetime.date(2020, 1, 23)],
    'Italy': [datetime.date(2020, 2, 21),
              datetime.date(2020, 3, 9)],
    'France': [datetime.date(2020, 3, 17)],
    'Spain': [datetime.date(2020, 3, 16)],
    'India': [datetime.date(2020, 3, 25)]
})
