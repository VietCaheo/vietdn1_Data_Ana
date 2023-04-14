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


def df_explore_byGenres(df, genres):
    """ Answer 02 questions 1: 
        1. Which genres are most popular from year to year?  
        by list of single genres
to check one by one and compute polular genres by year
    """
    #Question1:
    print("to investigate some columns with unique value ...\n")
    print("to see unique value list of genres ...\n")
    print(df.genres.unique())
    
    df_action_exist= df[df['genres'].str.contains("Action")]
    
    #How many every single genres appear
    release_count = []
    for item in genres:
        #print(f"to check this genres ...{item}   \n")
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
    """ Function to get the list actor name with at least 20 times apprearing on different movie.
    The result actor list is sorted also as descrease from the most to 20.
    """
    
    #target resutl list
    actor_list_famous = []
   
    cast_list = df['cast'].unique().tolist()
    # print(cast_list)
    
    # list out a list of single actor name
    print("\n to handle cast list and pick up to a list of single actors ... ")
    cast_list_single = []
    for item in cast_list:
        if(item.__contains__('|')):
            item_child = item.split('|')
            for ch in item_child:
                if ('Jr.' == ch):
                    cast_list_single.append('')
                elif (ch not in cast_list_single):
                    cast_list_single.append(ch)   
        elif('Jr.' == item):
            cast_list_single.append('')
        else:
            if item not in cast_list_single: 
                cast_list_single.append(item)
    
    
    #Get orignal cast list in combined form
    print("\n to get the orinal casts list in combined-form starting ... \n")
    cast_list_org = []
    for item in cast_list:
        if(item.__contains__('|')):
            item_child = item.split('|')
            cast_list_org.append(item_child)
    # print("to check cast list in original ... \n")
    # print(cast_list_org)
    
    # to look up most popular actor with at least 20 times apprearing
    # most_actor20 = {}
    most_actor20 = defaultdict(list)
    act = 0
    
    print("\nlook up actor starting ... ... ... this take some mins \n")
    for actor in cast_list_single:
        # most_actor20[actor] = []
        for casts in cast_list_org:
            act +=  casts.count(actor)  
        most_actor20[actor].append(act)
        #reset the count var for next actor looking up
        act=0
    
    print("to check result dict for which cast popular ... \n")
    most_actor20_sort = dict(sorted(most_actor20.items(), key=lambda item: item[1], reverse=True))
    
    #to slice for get a actor list with >= 20 appear
    most_actor20_final = dict(itertools.islice(most_actor20_sort.items(), 374))
    print(most_actor20_final)
    
    #to get the result list from above dict
    actor_list_famous = most_actor20_final.keys()
        
    print("\n ********end of getting the famous actor list ************************")
    
    return actor_list_famous

def xxx():
    """2. What kinds of properties are associated with movies that have high revenues?"""
    
    #select properties to investigate impact to revenues are: `revenue_adj` popularity budget_adj vote_average director cast
    
def main():
    """ Mainfuction for setting up the sequence for investigating datasets
include some steps
    overview dataset ->  
    """
    
    #there's some actor name could not display properly character
    df_movie=pd.read_csv('./movie_data_sets/tmdb-movies.csv', encoding = "ISO-8859-1")
    
    #to see the overview of dframe
    overview_df(df_movie)
    
    #implement datacleaning to get a dataframe after cleaned.
    df_cleaned = data_cleaning(df_movie)
    
    # to get a list of sigle-form genres
    genres_single = df_single_genres(df_cleaned)
    print("to see genres by sigle ... \n")
    print(genres_single)
    
    #OK
    #exploring the first question about the movies' popularity by genres 
    # df_explore_byGenres(df_cleanedgenres_single)
    
    cast_single_list = df_single_cast(df_cleaned)
    # print(cast_single_list)
    
    print("to see number most famoust actor and the list ... \n")
    print(len(cast_single_list))
    
    print(cast_single_list)


if __name__ == "__main__":
    main()