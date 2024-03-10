import pandas as pd

def read_hn_hsqc_peak_sparky(NH_HSQC_sparky):
    df = pd.read_csv(NH_HSQC_sparky, delim_whitespace=True, skip_blank_lines=True, header=None) \
        .dropna(axis=1)

    column_names = ['Assignment', 'N', 'HN']
    if df.shape[1] == 4:  # If there's a 4th column, it's the Data Height
        column_names.append('Data_Height')
    df.columns = column_names

    df['N'] = pd.to_numeric(df['N'], errors='coerce').round(3)
    df['HN'] = pd.to_numeric(df['HN'], errors='coerce').round(3)
    df = df.dropna(subset=['N', 'HN'])

    return df
