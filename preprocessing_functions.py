from init import *

def overlap_taxi(date,date_1,date_2):
    ''' Checks if taxi time "date" occurs between "date_1" and "date_2"'''

    if date >= date_1 and date <= date_2:
      return 1
    else:
      return 0

def N_Q(index, AOBT_list, ATOT_list, airplanes_taxi):
    '''For each taxi, returns respective counts of N (other aircrafts already taxiing)
      and Q (other aircrafts that cease to taxi) during the particular time frame.'''

    # Assign Intermediate Variables
    AOBT = AOBT_list[index]
    ATOT = ATOT_list[index]

    # Minimum number of iterations for a given index
    index_min = max(0, index - airplanes_taxi)

    # Maximum number of iterations for a given index
    index_max = min(index + airplanes_taxi, len(AOBT_list))

    AOBT_range = AOBT_list[index_min : index_max]
    ATOT_range = ATOT_list[index_min : index_max]

    # Check if other airplanes are taxiing when the given airplane taxis
    N_overlap = map(lambda x, y: overlap_taxi(AOBT, x, y), AOBT_range, ATOT_range)

    # Count the total number of airplanes that are taxiing when the given airplane leaves its stand (including the given airplane)
    N_count = max(0,sum(list(N_overlap))-1) + 1

    # Check if other airplanes stop taxiing when the given airplane taxis
    Q_overlap = map(lambda x: overlap_taxi(x, AOBT, ATOT), ATOT_range)
    
    # Count the total number of airplanes that stop taxiing
    Q_count = max(0, sum(list(Q_overlap))-1)

    return N_count, Q_count

def coordinate_dist(df):
    '''Gets distance between two points, considering the spherical shape of the Earth'''

    diff_lat = (df.Lat_stand - df.Lat_runway) * np.pi / 180
    diff_lng = (df.Lng_stand - df.Lng_runway) * np.pi / 180
    
    Lat_stand = df.Lat_stand * np.pi / 180
    Lat_runway = df.Lat_runway * np.pi / 180
    
    a = np.sin(diff_lat/2) * np.sin(diff_lat/2) + np.cos(Lat_stand) * np.cos(Lat_runway) * np.sin(diff_lng/2) * np.sin(diff_lng/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = 6371 * c * 1000
    
    return distance

def hour_rounder(t):
    '''Rounds time to the nearest hour'''
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +timedelta(hours=t.minute//30))

def preprocess(geo_path, airport_path, weather_path):
    '''Pre-processes data using the formats provided for geographical, airport, and weather data.'''

    # Load and process Geographical data
    geo = pd.read_csv(geo_path)\
            .assign(stand = lambda df: df.stand.apply(lambda t: t.upper()), # Uppercase
                    runway = lambda df: df.runway.apply(lambda t: t.upper()))\
            .rename(columns = {'runway':'Runway', 'stand':'Stand'}) # Rename columns

    geo_stand = geo[['Stand', 'Lat_stand', 'Lng_stand']].drop_duplicates() # Make dataframe of Stand data only
    geo_runway = geo[['Runway', 'Lat_runway', 'Lng_runway']].drop_duplicates() # Make dataframe of Runway data only

    # Load and process Airport data
    airport_df = pd.read_csv(airport_path)\
                .merge(geo_runway, on = 'Runway', how = 'left')\
                .merge(geo_stand, on = 'Stand', how = 'left')\
                .rename(columns = {'Aircraft Model': 'aircraft_model'})\
                .assign(AOBT = lambda df: pd.to_datetime(df.AOBT), # Convert AOBT to datetime type
                        ATOT = lambda df: pd.to_datetime(df.ATOT), # Convert ATOT to datetime type
                        target = lambda df: (df.ATOT - df.AOBT).apply(lambda x: x.total_seconds()), # Compute target variable in seconds
                        hour = lambda df: df.AOBT.apply(hour_rounder), # Round to nearest hour
                        distance = lambda df: df.apply(coordinate_dist, axis = 1), # Compute distance between coordinates
                        dist_log = lambda df: np.log(df.distance), # Compute logarithm of distances
                        AOBT_year = lambda df: df.AOBT.apply(lambda x: x.year), # Extract year from AOBT
                        AOBT_month = lambda df: df.AOBT.apply(lambda x: x.month), # Extract month from AOBT
                        AOBT_day = lambda df: df.AOBT.apply(lambda x: x.day), # Extract day from AOBT
                        AOBT_hour = lambda df: df.AOBT.apply(lambda x: x.hour), # Extract hour from AOBT
                        AOBT_min = lambda df: df.AOBT.apply(lambda x: x.minute), # Extract minute from AOBT
                        Runway = lambda df: df.Runway.astype('category').cat.codes, # Convert Runway to categorical type
                        Stand = lambda df: df.Stand.astype('category').cat.codes, # Convert Stand to categorical type
                        aircraft_model = lambda df: df.aircraft_model.astype('category').cat.codes) # Convert aircraft model to categorical type

    # Compute N and Q data
    AOBT_list = list(airport_df.AOBT) # Get list of AOBT's
    ATOT_list = list(airport_df.ATOT) # Get list of ATOT's
    airport_taxi = airport_df.Stand.nunique() # Get number of unique stands
    N_Q_tuples = list(map(lambda i: N_Q(i, 
                                        AOBT_list, 
                                        ATOT_list, 
                                        airport_taxi), 
                          tqdm(range(len(airport_df))))) # Compute N and Q values per row
    airport_df = airport_df.assign(N = [t[0] for t in N_Q_tuples], # Include N and Q columns in DataFrame
                                   Q = [t[1] for t in N_Q_tuples])

    # Load and process Weather data 
    weather_df = pd.read_csv(weather_path)\
                   .drop_duplicates(keep = 'first')\
                   .drop(columns = ['summary', 'icon', 'precipIntensity', 'precipProbability', 'pressure'])\
                   .assign(hour = lambda df: pd.to_datetime(df.time_hourly))

    # Consolidate Final data
    df = airport_df.merge(weather_df, how='left', on='hour')\
                   .fillna(method = 'ffill')\
                   .query('(target > 0) & (target < 20000)')\
                   .assign(precipType = lambda df: df.precipType.astype('category').cat.codes) # Convert precipType to categorical type
    
    return df