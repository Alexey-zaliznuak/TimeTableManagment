from datetime import datetime

def datetimes_intersect(
        dt:datetime,
        to_intersect: list[
            tuple[datetime, datetime],
        ],
        *,
        max_intrsects_count = 1, # break if found this count intersects
    ) -> bool:

    max_dt = max(dt)
    min_dt = min(dt)
    intersects = 0

    for el in to_intersect:
        if not (min(el) > max_dt or max(el) < min_dt):
            print('\n'+str(el[0])+str(el[1])+'\n')
            intersects += 1
        if intersects == max_intrsects_count:
            return True

    return False
