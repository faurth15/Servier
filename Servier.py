
import numpy as np
import pandas as pd
import re 
import json
import warnings




class Servier():
    
    def __init__(self,
                 drugs_filepath,
                clinical_filepath,
                pubmed_filepath):
        
        
        self.drugs_df = pd.read_csv(drugs_filepath)
        self.clinical_df = pd.read_csv(clinical_filepath)
        self.pubmed_df = pd.read_csv(pubmed_filepath)
        
        self.drugs = self.drugs_df['drug'].map(lambda x : x.lower()).to_list()
        
        
        
    def create_graph(self):
    
            #'''
            #drugs: list, drugs that we want to find in our corpus

            #Returns the Dataframe we use to modelise the graph.

            #create a pd.Dataframe to represent the Graph. We choose to use a pd.Dataframe
            #because of the function to_json() that can transform the dataframe to json dict object.

            #'''

        df = pd.DataFrame()
        df['drugs'] = self.drugs
        df['(PubMed,Date)'] = pd.Series([[] for i in range(len(self.drugs))])
        df['(Science,Date)'] = pd.Series([[] for i in range(len(self.drugs))])
        df['(Journal,Date)'] = pd.Series([[] for i in range(len(self.drugs))])
        df.set_index('drugs', drop = True, inplace=True)
        
        return df



    def preprocessing(self, var:str) -> pd.DataFrame:
    
        '''
        var: str,  The name of the Dataset we want to preprocess. Must be 'Science' or 'PubMed'
    
        Returns the preprocessed the dataset.
        '''
        
        if var == 'Science':
            Dataset = self.clinical_df
            Title_Column_Name = 'scientific_title'
        
        elif var == 'PubMed':
            Dataset = self.pubmed_df
            Title_Column_Name = 'title'
            
        else:
            warnings.warn("Sorry the var input must be 'Science' or 'PubMed'.")
            
            
        # Drop duplicates
        Dataset.drop_duplicates(subset=[Title_Column_Name], inplace=True)
        
        # Convert 'date' column to datetime and put all the date in the same format.
        Dataset['date'] = pd.to_datetime(Dataset['date']).dt.strftime('%d/%m/%Y')
        
        #Drop NaN in titles, convert other NaN in 'Unknown' to let the user now that 
        #we do not know the information.
        Dataset.dropna(subset=[Title_Column_Name], inplace=True)
        Dataset.replace(float("NaN"), 'Unknown', inplace=True)
        
        
        # Transform UNICODE charactere
        Dataset[Title_Column_Name] = Dataset[Title_Column_Name].apply(lambda x: x.encode("ascii", "ignore").decode())
        Dataset['journal'] = Dataset['journal'].apply(lambda x: x.encode("ascii", "ignore").decode())
        
            
        
        # Because we want to have the same Newspapers independently of the punctuation
        # we use regex to just keep the letters
        Dataset['journal'] = Dataset['journal'].apply(lambda x : re.sub(r'[^\w\s]','',x))
    
        if var == 'Science':
            self.clinical_df = Dataset
        else:
            self.pubmed_df = Dataset
            



    def Extraction(self, df:pd.DataFrame, var: str, preprop: bool = True) -> pd.DataFrame:
    
    
        '''
        df: pd.Dataframe, The Dataframe we want to fill, it represents our graph.
        var: str, If we want to look at the Scientific publication or Medical publication must be 'Science or 'PubMed'.
        preprop: bool, True if we want to preprocess our data before the extraction
    
        The Extraction function linked the drugs to the articles and newspapers that quote them in a form of a list of tuple of the form [(article or newspaper,date)].
        '''
    
        
        if preprop == True:
            self.preprocessing(var)
        
        if var == 'Science':
            Dataset = self.clinical_df
            Title_Column_Name = 'scientific_title'
        
        elif var == 'PubMed':
            Dataset = self.pubmed_df
            Title_Column_Name = 'title'
        
        else:
            warnings.warn("Sorry the var input must be 'Science' or 'PubMed'.")
            
            
        for j in range(len(self.drugs)):
            
            print(f'{self.drugs[j]} is being processed')
            
            condition = Dataset[Title_Column_Name].apply(lambda x : x.lower().find(self.drugs[j])) != -1
            IS_CITED = Dataset[condition].index.tolist()
            
            for element in zip(
                Dataset[Title_Column_Name][IS_CITED].tolist(),
                Dataset['date'][IS_CITED].tolist()
            ):
                df[f'({var},Date)'].loc[self.drugs[j]].append(element)
                 
            for element in zip(
                Dataset['journal'][IS_CITED].tolist(),
                Dataset['date'][IS_CITED].tolist()
            ):
                df['(Journal,Date)'].loc[self.drugs[j]].append(element)
            
        return df
        



