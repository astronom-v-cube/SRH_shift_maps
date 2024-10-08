import datetime as dt
import numpy as np
from scipy.ndimage import shift



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

def resize_data(data, nstep):
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
    llist = []
    for i in np.arange(-delta_shift[0], delta_shift[0]+1, 0.1):
        for j in np.arange(-delta_shift[1], delta_shift[1]+1, 0.1):
            stand_dev = standard_deviation(map_base-shift(map_curr, [i, j]))
            if stand_dev < minimum:
                llist.append(stand_dev)

                minimum = stand_dev
                best_delta = [i, j]
    #print(best_delta)
    return best_delta, minimum


def spline(data, xstep=10):
    ''' Увеличение разрешения карты с помощью бикубической интерполяции.
    data: входная карта
    xstep: во сколько раз увеличить число узлов сетки (стандартно в 10 раз)'''
    n = len(data)
    m = len(data[0])

    wide_data = 0 # ?


    return wide_data

def shift_map(data, shift=[0, 0]):
    ''' Сдвиг массива по горизонтали и вертикали'''



    return 0


def find_minimum(map_base, map_curr, delta_shift):
    ''' Hахождение минимума'''    #    вынести область, по которой сдвигаем, отдельно!!!



    return 0