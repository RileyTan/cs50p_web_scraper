import pandas as pd

# load data
def main():
    df = pd.read_csv('original_countries_by_hdi.csv')
    faulty_rows = select_faulty(df)

    fix_round1(df, faulty_rows)
    fix_round2(df, faulty_rows)
    fix_round3(df, faulty_rows)

    save_to_csv(df)

def select_faulty(df):
    """
    This function returns a mask, used in Pandas, a Series of booleans.
    Rows that have an empty or negative ranking will be represented by True.
    Rows that don't have that error will be represented by False.
    """
    mask_empty_rank = df['Rank'].isnull()
    mask_negative_rank = df['Rank'].str.contains('[^0-9.]')
    mask_faulty_rows_rank = mask_empty_rank | mask_negative_rank

    return mask_faulty_rows_rank

    return df
def fix_round1(df, faulty_rows):
    """
    This function shifts the faulty rows one column to the right.
    This function then returns the corrected dataframe, corrected once.
    """
    df.loc[faulty_rows] = df.loc[faulty_rows].shift(periods=1, axis="columns")

def clean_percentage_values(df, columns):
    """
    This function removes percentage signs and converts the values to floats.
    """
    for column in columns:
        df[column] = df[column].str.rstrip('%').astype(float) / 100.0

def fix_round2(df, faulty_rows):
    """
    This function returns the corrected dataframe by shifting the rows that have cells with % inside.
    This function works with the same rows as before.
    """
    last_two_columns = df.columns[-2:]
    clean_percentage_values(df, last_two_columns)
    df.loc[faulty_rows, last_two_columns] = df.loc[faulty_rows, last_two_columns].shift(periods=1, axis="columns")

def fix_round3(df, faulty_rows):
    """
    Rewrites the Rank column sequentially.
    """
    df["Rank"] = range(1, len(df) + 1)

def save_to_csv(df, file_path='correct_countries_by_hdi.csv'):
    """
    Saves the corrected dataframe into a new file.
    """
    df.to_csv(file_path, index=False)

if __name__ == "__main__":
    main()
