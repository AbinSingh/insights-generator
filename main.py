
from cos_quadrant_creator import cos_quadrant_creator
from hazard_quadrant_creator import hazard_quadrant_creator
from data_generator import data_gen
from trend_analysis import generate_trend

if __name__ == "__main__":
    df_claims = data_gen(num_samples=5000)

    df_claims = cos_quadrant_creator(df_claims)

    print(df_claims.head())

    df_claims = hazard_quadrant_creator(df_claims)
    print(df_claims.head())

    trend_df = generate_trend(df_claims)
    print(trend_df.head())
    print(trend_df.columns)





