import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# housing permits
housing = pd.read_csv('data/housing_permits.csv')
housing = housing.dropna().reset_index(drop=True)
housing['Date'] = pd.to_datetime(housing['Date'])

housing_melt = pd.melt(housing, id_vars=['Date'], value_vars=['Authorised', 'Started', 'Completed'])
sns.set(rc={'figure.figsize': (18, 8)})
ax = sns.lineplot(data=housing_melt[housing_melt.variable != 'Completed'], x="Date", y="value",
                  hue="variable", style='variable')
ax.set_title('Authorized vs Started Housing Permits')
ax.set(xlabel='Date', ylabel='Housing')
ax.legend(title='Housing Permits')
plt.savefig("graphs/housing_permits_started.png", dpi=150)

sns.set(rc={'figure.figsize': (18, 8)})
ax = sns.lineplot(data=housing_melt[housing_melt.variable != 'Started'], x="Date", y="value",
                  hue="variable", style='variable')
ax.set_title('Authorized vs Completed Housing Permits')
ax.set(xlabel='Date', ylabel='Housing')
ax.legend(title='Housing Permits')
plt.savefig("graphs/housing_permits_completed.png", dpi=150)

# ism index
man_pmi = pd.read_csv('data/ISM-MAN_PMI.csv')
man_pmi['Date'] = pd.to_datetime(man_pmi['Date'], format='%Y-%m-%d')
man_pmi = man_pmi.sort_values(by='Date')

sns.set(rc={'figure.figsize': (15, 8)})
ax = sns.lineplot(data=man_pmi, x="Date", y="PMI", color='b')
ax.axhline(50, ls='--', c='k')
ax.axhline(60, ls='--', c='m')
ax.axhline(40, ls='--', c='r')
ax.set_title('Manufacturing PMI')
ax.set(xlabel='Date', ylabel='PMI')
plt.savefig("graphs/manufacturing_index.png", dpi=150)

# consumer sentiment index
consumer_index = pd.read_csv('data/consumer_index.csv')
consumer_index['Date'] = pd.to_datetime(consumer_index['Year'].astype(str) + '-' + consumer_index['Month'].astype(str),
                                        format='%Y-%m')
consumer_index = consumer_index[['Date', 'Index']]
consumer_index = consumer_index.sort_values(by='Date').reset_index(drop=True)
consumer_index['Moving Average'] = consumer_index.Index.expanding(2).mean()
consumer_index['6 Months Rolling Average'] = consumer_index.Index.rolling(6).mean()
consumer_index['12 Months Rolling Average'] = consumer_index.Index.rolling(12).mean()
consumer_index_melt = pd.melt(consumer_index, id_vars=['Date'], value_vars=['Index', 'Moving Average',
                                                                            '6 Months Rolling Average',
                                                                            '12 Months Rolling Average'])

sns.set(rc={'figure.figsize': (18, 8)})
ax = sns.lineplot(data=consumer_index_melt.dropna(), x="Date", y="value",
                  hue="variable", style='variable')
ax.set_title('University of Michigan Consumer Sentiment Index')
ax.set(xlabel='Date', ylabel='')
plt.savefig("graphs/consumer_index.png", dpi=150)
