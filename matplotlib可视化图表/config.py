import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings; warnings.filterwarnings(action='once')

large = 22; middle = 16; small = 12

params = {'axes.titlesize': large,
          'legend.fontsize': large,
          'figure.figsize': (16, 10),
          'axes.labelsize': middle,
          'axes.titlesize': middle,
          'xtick.labelsize': middle,
          'ytick.labelsize': middle,
          'figure.titlesize': large}

plt.rcParams.update(params)
plt.style.use('seaborn-whitegrid')
sns.set_style('white')

print(mpl.__version__)
print(sns.__version__)

