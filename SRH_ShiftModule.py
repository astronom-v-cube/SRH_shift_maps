import datetime as dt
import numpy as np
from scipy.ndimage import shift
from scipy import signal, optimize, interpolate

class srh_mapname_ANF:
    def __init__(self, filename, homepath = ''):
        #SRH0612 _ CH06  _ 8.20GHz  _    V        _ 20230712  _ 083000.fits
        observer, channel, frequency, polarization, date_string,   other     = filename.split('_')
        time_string, format_of_observation = other.split('.')
        sep_date = lambda ss :f"{ss[:4]}-{ss[4:6]}-{ss[6:8]}"
        sep_time = lambda ss :f"{ss[:2]}:{ss[2:4]}:{ss[4:6]}"

        self.name = filename
        self.observer = observer
        self.channel = channel
        self.freq = float(frequency[:-3])
        self.format = format_of_observation
        self.plr = polarization
        self.time = dt.time.fromisoformat(sep_time(time_string))
        self.date = dt.date.fromisoformat(sep_date(date_string))
        self.homepath = homepath + filename

def makecolors():
    cols = []
    for k in range(2000):
        cols.append('red')
        cols.append( 'orangered')
        cols.append( 'darkorange')
        cols.append( 'gold')
        cols.append( 'yellow')
        cols.append( 'greenyellow')
        cols.append( 'mediumspringgreen')
    return cols

def resize_data(data, nstep):
    """Классная функция, жаль не используется)))

    Args:
        data (_type_): _description_
        nstep (_type_): _description_

    Returns:
        _type_: _description_
    """
    n = len(data)
    m = len(data[0])
    rows, cols = (n*nstep, m*nstep)
    arr = np.zeros(shape=(n*nstep, m*nstep))

    for y in range(n):
        for x in range(m):
                for delta_y in range(nstep):
                    for delta_x in range(nstep):
                        arr[y*nstep+delta_y][x*nstep+delta_x] = data[y][x]
            #fill_cell(y, x, arr, data, nstep)
    return arr

standard_deviation = lambda  dat : np.sqrt(np.sqrt(np.sum(dat**4)/(len(dat)**2)))

def find_min_deviation(map_base, map_curr, delta_shift):
    minimum = 1e7
    best_delta = [0, 0]

    sum_shift = lambda arr: abs(arr[0]) + abs(arr[1])
    k = 1

    llist = []
    for i in np.arange(-delta_shift[0], delta_shift[0] + 1, k):
        for j in np.arange(-delta_shift[1], delta_shift[1] + 1, k):
            stand_dev = standard_deviation(map_base-shift(map_curr, [i, j]))
            if stand_dev < minimum:
                llist.append(stand_dev)

                minimum = stand_dev
                best_delta = [round(i, 2), round(j, 2)]

                if sum_shift(best_delta) <= 2 and sum_shift(best_delta) > 1:
                    k = 0.5
                elif sum_shift(best_delta) <= 0.5:
                    k = 0.1

    return best_delta, minimum

def find_min_deviation_with_correlation(map_base, map_curr):
    x = np.arange(0, map_base.shape[1])
    y = np.arange(0, map_base.shape[0])

    cross_corr = signal.correlate2d(map_base, map_curr, mode="same")
    cross_corr_spline = interpolate.RectBivariateSpline(y, x, -cross_corr)

    def thefunc(vals):
        y, x = vals
        return cross_corr_spline(x, y)

    max_y, max_x = optimize.fmin(thefunc, np.array([map_base.shape[0]//2,map_base.shape[1] // 2]))
    max_val = cross_corr_spline(max_x, max_y)

    shift_x = max_y - map_base.shape[1] // 2
    shift_y = max_x - map_base.shape[0] // 2

    return [np.round(shift_y, 5), np.round(shift_x, 5)], -max_val