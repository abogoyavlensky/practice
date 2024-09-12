from datetime import date, timedelta
from typing import Optional


class Employment:
    def __init__(self, start_date: date, end_date: Optional[date]):
        """

        Parameters
        ----------
        start_date
            The date the employment started.
        end_date
            The date the employment ended (set to None if the employment is still active).
        """
        self.start_date = start_date
        self.end_date = end_date



class EmploymentHistory:
    def __init__(self, employments: list[Employment]):
        self.employments = employments

    @property
    def earliest(self) -> Employment:
        """Returns the employment started the earliest."""
        if self.is_empty():
            return None
        else:
            earliest_empl = sorted(self.employments, key = lambda item: item.start_date) # O(log n)
            return earliest_empl[0]

    @property
    def current(self) -> list[Employment]:
        """Return a list of ongoing employments."""
        curretn_empoyments = [i for i in self.employments if not i.end_date]
        return curretn_empoyments
        
    @property
    def is_empty(self) -> bool:
        """Return True if the employment history is empty, False otherwise"""
        return not self.employments

    @property
    def total_time_employed(self) -> timedelta:
        """Returns the total amount of time spent employed..
        If working multiple jobs concurrently, they should not be double counted."""
        total_time = None
        time_periods = []

        sorted_employments = sorted(self.employments, key = lambda item: item.start_date)

        for item in sorted_employments:
            if not item.end_date:
                end_date = date.today()
            else:
                end_date = item.end_date

            if not time_periods:
                time_periods.append([item.start_date, end_date])
                total_time = end_date - item.start_date
            else:
                for idx, period in enumerate(time_periods):
                    if period[0] <= item.start_date <= period[1]:
                        if period[1] < end_date:
                            total_time += end_date - period[1]
                            time_periods[idx][1] = end_date
                    else:
                        time_periods.append([item.start_date, end_date])
                        total_time += end_date - item.start_date
        
        return total_time
                        
                            

# Tests

def test_total_time_employed():
    employemnts = [Employment(date(2021, 1, 20), date(2021, 1, 25)),
                   Employment(date(2021, 1, 23), date(2021, 1, 28)),
                   Employment(date(2021, 2, 10), date(2021, 2, 25))]

    history = EmploymentHistory(employemnts)
    expected_total_time = (date(2021, 1, 28) - date(2021, 1, 20)) + (date(2021, 2, 25) - date(2021, 2, 10))
    assert expected_total_time == history.total_time_employed



# A quick summary of the behaviour of timedelta:
# d1 = date(2021, 4, 23)
# d2 = date(2023, 5, 21)
# 
# td1 = d2-d1
# td2 = td1 + timedelta(days=5)
# assert td1 == timedelta(days=758)
# assert td2 == timedelta(days=763)
 