import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from collections import defaultdict
import itertools

# % matplotlib inline

# Upgrade pandas to use dataframe.explode() function. 
# !pip install --upgrade pandas==0.25.0


def overview_df(df):
    print("**********************************************")
    print("to see the datatye of df")
    print(df.dtypes)
    print()

    print("to see shape of dataset ...")
    print(df.shape)
    print()

    print("to see statistics for each column ... ")
    print(df.describe())
    print()

    print("to see the first row ...")
    print(df.head(1))
    
    print("how many duplicated rows in movie datasets...")
    print(df.duplicated().sum())
    print()

    print("to check unique values in each column ...")
    print(df.nunique())
    print()
    
    print("to see missing value by each column ... ")
    print(df.isnull().sum())
    print("\n **********************end of see overview df ************************")


def data_cleaning(df):
    """Implement drop 01 duplicated row
and some specified columns that have NaN values
    """
    print("**********************************************")
    print("starting cleaning data ... \n")
    df_clean = df.drop_duplicates()
    
    #drop some dont care columns tagline keywords overview homepage
    df_clean.drop(['tagline', 'keywords', 'overview', 'homepage'], axis=1, inplace=True)
    
    #drop some columns including NaN: cast director imdb_id
    df_clean.dropna(subset=['cast', 'director', 'imdb_id', 'genres'], inplace=True)
    
    # to replace missing value of `production_companies` by a default string
    df_clean.fillna({'production_companies':'None'}, inplace=True)
    print("\n ***********************end of cleaning data ***********************")
    
    return df_clean

def df_single_genres(df):
    print("**********************************************")

    print("to see shape of dataset ...")
    print(df.shape)
    print()

    print("to check unique values in each column ...")
    print(df.nunique())
    print()
    
    print("to see missing value by each column ... ")
    print(df.isnull().sum())
    print()
   
    #see deep-inside the genres ... 
    print("to check unique values in each column ...")
    genres_list = df['genres'].unique().tolist()
    print(type(genres_list))
    
    #to get only list of single genre in `genres` column
    gen_list_single = []
    for item in genres_list:
        if(item.__contains__('|')):
            item_child = item.split('|')
            for ch in item_child:
                if ch not in gen_list_single:
                    gen_list_single.append(ch)
        else:
            if item not in gen_list_single: 
                gen_list_single.append(item)
    
    # print(gen_list_single)
    print("\n **********************end of see df after cleaned ************************")
    
    return gen_list_single


def df_explore_bygenres(df, genres):
    """ Answer questions 1:
        1. Which genres are most popular from year to year?  
        by list of single genres
to check one by one and compute polular genres by year
    """

    # Question1:
    print("to see unique value list of genres ...\n")
    print(df.genres.unique())
    
    # How many every single genres appear
    release_count = []
    for item in genres:
        # print(f"to check this genres ...{item}   \n")
        # print(df[df['genres'].str.contains(item)].count())
        # print(df[df['genres'].str.contains(item)].shape[0])
        count = df[df['genres'].str.contains(item)].shape[0]
        release_count.append(count)
        print()
    
    # build a dict from two lists
    stt_bygenres = {genres[i]: release_count[i] for i in range(len(genres))}
    
    print(type(stt_bygenres))
    print(stt_bygenres)
    
    # build data frame for explore number released movied by genres
    # df_gen = pd.DataFrame.from_dict(stt_bygenres)
    movie_in_genere = pd.DataFrame(data=stt_bygenres, index=[0])
    print(movie_in_genere.head())
    
    s = movie_in_genere.iloc[0:,:]
     
    s.plot(kind='bar',width = 3)
    plt.title('Most Popular Movie by Genres')
    plt.xlabel('Movie genres')
    plt.ylabel('No. of released movied')
    plt.show()
    
    print("\n ***********************end of explore by genres ***********************")


def df_single_cast(df):
    """ Function to get the list actor whom is classified by apprearing at least 20 times on different movies.
    The result actor list is sorted also as decreasing from the most to 20"""

    # target result list
    actor_list_famous = []
   
    cast_list = df['cast'].unique().tolist()
    # print(cast_list)
    
    # list out a list of single actor name
    # Note: some actor-name is no meaning when display only "Jr."
    print("\nPick up to a list of single actors ... ")
    cast_list_single = []
    for item in cast_list:
        if item.__contains__('|'):
            item_child = item.split('|')
            for ch in item_child:
                if 'Jr.' == ch:
                    cast_list_single.append('')
                elif ch not in cast_list_single:
                    cast_list_single.append(ch)   
        elif 'Jr.' == item:
            cast_list_single.append('')
        else:
            if item not in cast_list_single: 
                cast_list_single.append(item)

    # Get original cast list in combined form
    print("\nGet the original casts list in combined-form starting ... \n")
    cast_list_org = []
    for item in cast_list:
        if item.__contains__('|'):
            item_child = item.split('|')
            cast_list_org.append(item_child)
    # print("to check cast list in original ... \n")
    # print(cast_list_org)
    
    # to look up most popular actor with at least 10 times appearing
    # most_actor10 = {}
    most_actor10 = defaultdict(list)
    act = 0
    
    print("\nlooking up actor ...  please wait ... \n")
    for actor in cast_list_single:
        # most_actor10[actor] = []
        for casts in cast_list_org:
            act += casts.count(actor)
        most_actor10[actor].append(act)
        # reset the count var for next actor looking up
        act = 0
    
    print("to check result dict for which cast popular ... \n")
    most_actor10_sort = dict(sorted(most_actor10.items(), key=lambda item: item[1], reverse=True))
    # print(most_actor10_sort)
    
    # slice for get a dict of actor with >= 10 appear
    most_actor10_final = dict(itertools.islice(most_actor10_sort.items(), 1077))
    # print(most_actor10_final)
    
    # to get the result list from above dict
    actor_list_famous = most_actor10_final.keys()
        
    print("\n ********end of getting the famous actor list ************************")
    
    # return actor_list_famous
    return most_actor10_final


def explore_question2(df, f_cast):
    """2. What kinds of properties are associated with movies that have high revenues?"""
    
    # select properties to investigate impact to revenue_adj are: 'popularity' `vote_average` `budget_adj` f_cast or `director`

    # tempo_close*******************************************************************
    # build mean() by each target test-feature
    # print("\ncheck mean() of revenue_adj of each revenue_adj  ... \n")
    # print(df.describe().revenue_adj)
    #
    # print("\ncheck mean() of revenue_adj of each vote_average  ... \n")
    # print(df.describe().vote_average)
    #
    # print("\ncheck mean() of revenue_adj of each budget_adj  ... \n")
    # print(df.describe().budget_adj)

    # tempo_close*******************************************************************

    # print("\nto see distribution of revenue_adj ... \n")
    # df['revenue_adj'].plot()

    # create a columns by "famous-index" = sum(index of most_actor10),
    # adding new column with index is number of apprearing on all time, each cell will hold the sum of all actor in current
    # movie, the higher the more famous

    # scan by df['cast'], check contain any famous_actors and get the famous_index to fill to `famous_actors_index`
    # To get a list of famous_index given by each cast movie by movie
    famous_index = []
    famous_accum = 0

    print("\nlook up and save the famous index by actors in every single movie ... \n")
    # scan by dict of famous_actor20, and scan row by row of df
    for index, row in df.iterrows():
        for item in f_cast.items():
            fcast_c = row['cast'].count(item[0])
            if 0 != fcast_c:
                # cast_apprearing_time in dict is an 1-element-list, that why need [1][0]
                famous_accum += item[1][0]
        # reset value of every row checking finished
        famous_index.append(famous_accum)
        famous_accum = 0

    print("\nfinished getting famous-cast index for every movie")
    print("\nadding new famous_actors_index by above result")

    df.loc[:, 'famous_actors_index'] = famous_index
    print(df.head())

    print("\nplot relationships between some feature vs revenue_adj ... \n")
    df.plot(x='vote_average', y='revenue_adj', kind='scatter', color='red')
    df.plot(x='budget_adj', y='revenue_adj', kind='scatter', color='green')
    df.plot(x='popularity', y='revenue_adj', kind='scatter', color='blue')
    df.plot(x='famous_actors_index', y='revenue_adj', kind='scatter', color='black')
    plt.show()

def main():
    """ Mainfuction for setting up the sequence for investigating datasets include some steps
    overview dataset ->  
    """


    # there's some actor name could not display properly character
    df_movie=pd.read_csv('./../../Prj2_Investigate_dataset/movie_data_sets/tmdb-movies.csv', encoding = "ISO-8859-1")
    
    # to see the overview of dframe
    overview_df(df_movie)
    
    # implement datacleaning to get a dataframe after cleaned.
    df_cleaned = data_cleaning(df_movie)
    
    # to get a list of sigle-form genres
    genres_single = df_single_genres(df_cleaned)
    print("to see genres by single ... \n")
    print(genres_single)
    
    # OK question 1
    # exploring the first question about the movies' popularity by genres
    # df_explore_bygenres(df_cleaned, genres_single)

    # this below dict contain the most-appear actor in movies, the apprearing will be used later for estimate success movie
    famous_casts = df_single_cast(df_cleaned)
    # print(famous_casts)
    
    print("to see number most famous actor and the list ... \n")
    # print(len(famous_casts))
    # print(famous_casts)
    
    # start to explore data for answer question2
    # use the above famous_casts for serving more this question2
    # drop don't care columns prior to exploring about which impacts to revenue
    df_cleaned.drop(['imdb_id', 'original_title', 'runtime', 'vote_count', 'revenue', 'budget'], axis=1, inplace=True)
    # print(df_cleaned.head(30))
    # overview again the df after more drops
    # overview_df(df_cleaned)

    explore_question2(df_cleaned, famous_casts)

if __name__ == "__main__":
    main()