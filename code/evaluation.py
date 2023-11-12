from classes import *
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt

k = 2
n = 125
seed = 42
num_bands = 5
num_buckets = 25

SETTINGS = {
    'n_documents': 20,   
    'file_path': 'C:/Github/ID2222/data/',
    'file_name': 'recipes.json'
}

def execution_time():
    # Test execution time vs number of documents
    times = pd.DataFrame(columns=['n_documents', 'time'])
    for i in tqdm(range(0, 400, 10)):
        SETTINGS['n_documents'] = i
        data_pipeline = DataPipeline(SETTINGS)
        df_documents = data_pipeline.df_documents

        eval = Evaluation(k, n, seed, num_bands, num_buckets, SETTINGS)
        elapsed_time = eval(df_documents=df_documents)

        times = pd.concat([times, pd.DataFrame({'n_documents': [i], 'time': [elapsed_time]})], ignore_index=True)

    # Save the results
    times.to_csv('C:/Github/ID2222/results/evaluation_times_lsh.csv', index=False)
    


def make_graph():
    # Make a graph of execution time vs number of documents
    times = pd.read_csv('C:/Github/ID2222/results/evaluation_times.csv')
    plt.plot(times['n_documents'], times['time'])
    plt.xlabel('Number of documents')
    plt.ylabel('Execution time (s)')
    plt.title('Execution time vs number of documents')
    plt.savefig('C:/Github/ID2222/results/evaluation_times.png')

def combine_graph():
    # Combine graphs
    times = pd.read_csv('C:/Github/ID2222/results/evaluation_times.csv')
    times_lsh = pd.read_csv('C:/Github/ID2222/results/evaluation_times_lsh.csv')
    plt.plot(times['n_documents'], times['time'], label='LSH')
    plt.plot(times_lsh['n_documents'], times_lsh['time'], label='LSH')
    plt.xlabel('Number of documents')
    plt.ylabel('Execution time (s)')
    plt.title('Execution time vs number of documents')
    plt.savefig('C:/Github/ID2222/results/evaluation_times2.png')

if __name__ == '__main__':
    #execution_time()
    #make_graph()
    combine_graph()