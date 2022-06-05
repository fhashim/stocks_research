import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt

from pandas.tseries.offsets import MonthEnd

# read s&p500 data
sp = pd.read_csv('data/SP500.csv')
sp['Date'] = pd.to_datetime(sp['Date'], format='%d/%m/%Y')
sp['Month'] = pd.PeriodIndex(sp.Date, freq='M')
sp['Year'] = pd.PeriodIndex(sp.Date, freq='Y')
sp = sp.sort_values(by='Date')
sp_monthly = pd.DataFrame(sp.groupby('Month').max()['Date'])
sp_monthly = sp_monthly.set_index('Date').join(sp.set_index('Date')[['Adj Close**']]). \
    rename(columns={'Adj Close**': 'SP500'})
sp_monthly['Month'] = pd.PeriodIndex(sp_monthly.reset_index().Date, freq='M')

sp_yearly = pd.DataFrame(sp.groupby('Year').max()['Date'])
sp_yearly = sp_yearly.set_index('Date').join(sp.set_index('Date')[['Adj Close**']]). \
    rename(columns={'Adj Close**': 'SP500'})
sp_yearly['Year'] = pd.PeriodIndex(sp_yearly.reset_index().Date, freq='Y')
sp_yearly['SP500_Yearly_Returns'] = (sp_yearly['SP500'] - sp_yearly['SP500'].shift()) / sp_yearly['SP500'].shift()

# read housing permits
housing = pd.read_csv('data/housing_permits.csv')
housing = housing.dropna().reset_index(drop=True)
housing['Date'] = pd.to_datetime(housing['Date'])
housing['Month'] = pd.PeriodIndex(housing.Date, freq='M')
housing = housing.sort_values(by='Date')

# read gdp
# yearly
gdp = pd.read_csv('data/USGDP.csv')
gdp['Date'] = pd.to_datetime(gdp['Date'], format='%d/%m/%Y')
gdp = gdp.sort_values(by='Date')
gdp['Month_End'] = gdp['Date'] - MonthEnd(1)
gdp['Month_End_Year'] = pd.PeriodIndex(gdp.Month_End, freq='Y')

# create yearly gdp
gdp_yearly = pd.DataFrame(gdp.groupby('Month_End_Year').max()['Month_End'])
gdp_yearly = gdp_yearly.set_index('Month_End').join(gdp.set_index('Month_End')[['GDP', 'Month_End_Year']])
gdp_yearly['GDP_Returns'] = (gdp_yearly['GDP'] - gdp_yearly['GDP'].shift()) / gdp_yearly['GDP'].shift()

# read gdp yearly growth
yearly_gdp_growth = pd.read_csv('data/GDP_Growth.csv')
yearly_gdp_growth['Date'] = pd.to_datetime(yearly_gdp_growth['Year'], format='%Y')
yearly_gdp_growth['Month'] = pd.PeriodIndex(yearly_gdp_growth.Date, freq='M')
yearly_gdp_growth.rename(columns={'GDP Growth': 'Yearly_GDP_Growth'}, inplace=True)

# create quarterly gdp
gdp_quarterly = gdp[['Date', 'Month_End', 'GDP']]
gdp_quarterly['GDP_Returns'] = (gdp_quarterly['GDP'] - gdp_quarterly['GDP'].shift()) / gdp_quarterly['GDP'].shift()

# analysis df
analysis_df = pd.DataFrame(data=pd.date_range(yearly_gdp_growth.Date.min(), yearly_gdp_growth.Date.max(), freq='M'),
                           columns=['Date'])
analysis_df['Month'] = pd.PeriodIndex(analysis_df.Date, freq='M')

# Join SP500
analysis_df = analysis_df.set_index('Month').join(sp_monthly[['Month', 'SP500']].set_index('Month'))

# Join housing data
analysis_df = analysis_df.join(housing[['Month', 'Authorised']].set_index('Month'))

#Join GDP Growth
analysis_df = analysis_df.join(yearly_gdp_growth.set_index('Month')['Yearly_GDP_Growth'])
analysis_df['Yearly_GDP_Growth'] = analysis_df['Yearly_GDP_Growth'] / 100

# Join GDP Quarterly
analysis_df = analysis_df.reset_index().set_index('Date').join(
    gdp_quarterly.set_index('Month_End').rename(columns={'GDP_Returns': 'Quarterly_GDP'})['Quarterly_GDP'])

# Join GDP Yearly
analysis_df = analysis_df.reset_index().set_index('Date').join(gdp_yearly.
                                                               rename(columns={'GDP_Returns': 'Yearly_GDP'})
                                                               ['Yearly_GDP'])

# SP500
analysis_df = analysis_df.join(sp_yearly['SP500_Yearly_Returns'])

# SP500 Returns
analysis_df['SP500_Returns'] = (analysis_df['SP500'] - analysis_df['SP500'].shift()) / analysis_df['SP500'].shift()

# Housing Permit Returns
analysis_df['Housing_Returns'] = (analysis_df['Authorised'] -
                                  analysis_df['Authorised'].shift()) / analysis_df['Authorised'].shift()

plot_df = analysis_df[['Month', 'SP500_Returns', 'Authorised', 'Yearly_GDP_Growth', 'Housing_Returns']]

plot_df = plot_df.iloc[1:, :]

corr = plot_df.corr()

fig = plt.figure(figsize=(8, 5), dpi=150)
ax = fig.gca()
sns.lineplot(data=plot_df.Housing_Returns, color="g", label='Housing')
ax2 = plt.twinx()
sns.lineplot(data=plot_df.Yearly_GDP_Growth, color="b", ax=ax2, label='GDP', marker='o')
plt.legend(loc='upper center')
ax.set_ylabel('Authorised Housing Permits Growth')
ax2.set_ylabel('GDP Growth')
ax.set_title('Housing Permits vs GDP Growth')
plt.grid(True)
fig.tight_layout()
plt.savefig("housing_permits_growth", dpi=150)


fig = plt.figure(figsize=(8, 5), dpi=150)
ax = fig.gca()
sns.lineplot(data=plot_df.Authorised, color="g", label='Housing')
ax2 = plt.twinx()
sns.lineplot(data=plot_df.Yearly_GDP_Growth, color="b", ax=ax2, label='GDP', marker='o')
plt.legend(loc='upper center')
ax.set_ylabel('Authorised Housing Permits')
ax2.set_ylabel('GDP Growth')
ax.set_title('Housing Permits vs GDP Growth')
plt.grid(True)
fig.tight_layout()
plt.savefig("housing_permits", dpi=150)



## PMI INDICATOR

# read manufacturing PMI

man_pmi = pd.read_csv('data/ISM-MAN_PMI.csv')
man_pmi['Date'] = pd.to_datetime(man_pmi['Date'], format='%Y-%m-%d')
man_pmi['Month'] = pd.PeriodIndex(man_pmi.Date, freq='M')
man_pmi = man_pmi.sort_values(by='Date')

# analysis df
analysis_df = pd.DataFrame(data=pd.date_range(yearly_gdp_growth.Date.min(), yearly_gdp_growth.Date.max(), freq='M'),
                           columns=['Date'])
analysis_df['Month'] = pd.PeriodIndex(analysis_df.Date, freq='M')

# join gdp growth
analysis_df = analysis_df.set_index('Month').join(yearly_gdp_growth.set_index('Month')['Yearly_GDP_Growth'])

# join pmi
analysis_df = analysis_df.join(man_pmi.set_index('Month')['PMI'])

plot_df = analysis_df[['Yearly_GDP_Growth', 'PMI', 'Date']]

plot_df = plot_df.reset_index(drop=True).set_index('Date')

corr = plot_df.corr()

fig = plt.figure(figsize=(8, 5), dpi=150)
ax = fig.gca()
sns.lineplot(data=plot_df.PMI, color="g", label='Manufacturing PMI')
ax2 = plt.twinx()
sns.lineplot(data=plot_df.Yearly_GDP_Growth, color="b", ax=ax2, label='GDP', marker='o')
plt.legend(loc='upper center')
ax.set_ylabel('Manufacturing PMI')
ax2.set_ylabel('GDP Growth')
ax.set_title('Manufacturing PMI vs GDP Growth')
plt.grid(True)
fig.tight_layout()
plt.savefig("manufacturing_pmi", dpi=150)