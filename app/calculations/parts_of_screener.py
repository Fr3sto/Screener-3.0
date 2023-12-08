import time
from datetime import datetime
from shared_memory_dict import SharedMemoryDict

from calculations.exchange import get_currencies
from calculations.candles import get_start_candles

from calculations.database import get_candles_by_symbol_tf, delete_all_impulses, delete_all_levels, insert_currency
from calculations.other_func import get_df_from_candles
from calculations.impulses import calculate_impulses
from calculations.levels import calculate_levels_after_impulse
from calculations.candles import get_last_candles_and_impulse

def get_start_data(currency_dict):
    t1 = time.time()
    get_start_candles(currency_dict)
    t2 = time.time()

    print('Time left Candles ',t2 - t1)

    list_tf = [5,15,30,60]

    t1 = time.time()
    delete_all_impulses()
    calculate_impulses(currency_dict, list_tf)
    t2 = time.time()

    print('Time left Impulse ',t2 - t1)

    t1 = time.time()
    delete_all_levels()
    calculate_levels_after_impulse(list_tf)
    t2 = time.time()

    print('Time left Levels ',t2 - t1)

def main_func(exchange):

    currency_dict = get_currencies(100)
    insert_currency(currency_dict)
    get_start_data(currency_dict)
    
    last_minute = datetime.now().minute
    while True:
        if datetime.now().minute != last_minute:
            last_minute = datetime.now().minute
            last_hour = datetime.now().hour
            get_last_candles_and_impulse(currency_dict, last_minute, last_hour)
        

        time.sleep(1)


if __name__ == '__main__':
    main_func('S')
