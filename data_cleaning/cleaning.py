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
    looking at original_country_by_hdi.csv, we isolate the rows with issues by looking at the Rank column
    all rows with issue either have an empty rank or a rank containing non-numeric characters
    """
    mask_empty_rank = df['Rank'].isnull()
    mask_negative_rank = df['Rank'].str.contains('[^0-9.]')
    mask_faulty_rows_rank = mask_empty_rank | mask_negative_rank

    return mask_faulty_rows_rank

    return df
def fix_round1(df, faulty_rows):
    """
    this function shifts the faulty rows one column to the right.
    """
    
    df.loc[faulty_rows] = df.loc[faulty_rows].shift(periods=1, axis="columns")

def clean_percentage_values(df, columns):
    """
    this function removes percentage signs and converts the values to floats.
    """
    
    for column in columns:
        df[column] = df[column].str.rstrip('%').astype(float) / 100.0

def fix_round2(df, faulty_rows):
    """
    this is the final shift of columns for annual growth values into its corresponding column
    all percentage values are removed and converted to floats for easier future use 
    """
    
    last_two_columns = df.columns[-2:]
    clean_percentage_values(df, last_two_columns)
    df.loc[faulty_rows, last_two_columns] = df.loc[faulty_rows, last_two_columns].shift(periods=1, axis="columns")

def fix_round3(df, faulty_rows):
    """
    rewrites the Rank column sequentially.
    """
    
    df["Rank"] = range(1, len(df) + 1)

def save_to_csv(df, file_path='correct_countries_by_hdi.csv'):
    """
    saves the corrected dataframe into a new csv file.
    """
    
    df.to_csv(file_path, index=False)

if __name__ == "__main__":
    main()
