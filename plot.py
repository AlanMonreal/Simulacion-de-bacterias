import pandas as pd
import matplotlib.pyplot as plt


def timeseries():
    df = pd.read_csv('simulador.csv')

    plt.plot('seconds', 'count', data=df, color='tab:red')

    plt.yticks(fontsize=12, alpha=.7)
    plt.title("Transcurso de tiempo ", fontsize=22)
    plt.grid(axis='both', alpha=.3)

    plt.xlabel('Segundos')
    plt.ylabel('N Bacterias')
    
    plt.gca().spines["top"].set_alpha(0.0)    
    plt.gca().spines["bottom"].set_alpha(0.3)
    plt.gca().spines["right"].set_alpha(0.0)    
    plt.gca().spines["left"].set_alpha(0.3)   

    plt.savefig('transcurso.png')
    plt.close()
