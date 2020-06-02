# %%
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt


# %%
bafta = pd.read_csv('awarddata/bafta.csv')
bafta = bafta[bafta['winner'] == True].copy()
new = bafta['category'].str.split(' in ', expand=True)
bafta['category'] = new[0]
new = bafta['category'].str.split('|', expand=True)
bafta['category'] = new[1]
bafta_rep = {' Film':'picture',
' Direction':'directing',
' Director':'directing',
' Supporting Actor':'sup actor',
' Supporting Actress':'sup actress',
' Actor':'actor',
' Actress':'actress',
' Leading Actor':'actor',
' Leading Actress':'actress',
' Cinematography':'cinematography',
' Documentary':'doc',
' Sound':'sound',
' MUSIC (Original Score)':'score',
' Original Screenplay':'screenplay',
' Screenplay':'screenplay',
' Editing':'editing',
' Original Song Written for a Film':'song'}
bafta = bafta[bafta['category'].isin(list(bafta_rep.keys()))].copy()
bafta['category'] = bafta['category'].replace(bafta_rep)
bafta['nominee'] = bafta['nominee'].str.upper()
bafta['workers'] = bafta['workers'].str.upper()
bafta = bafta.reset_index(drop=True)
bafta = bafta.drop(columns=['winner'])
bafta = bafta.rename(columns={'nominee':'b_nominee','workers':'b_winner'})


# %%
gg = pd.read_csv('awarddata/gg.csv')
gg = gg[gg['win'] == True].copy()
gg = gg.drop(['year_film', 'ceremony'], axis =1).copy()
gg_rep = {'Best Motion Picture - Drama':'picture',
'Best Motion Picture - Musical or Comedy':'picture',
'Picture':'picture',
'BEST PICTURE':'picture',
'Best Director - Motion Picture':'directing',
'Best Performance by an Actor in a Supporting Role in any Motion Picture':'sup actor',
'Best Performance by an Actress in a Supporting Role in any Motion Picture':'sup actress',
'Best Performance by an Actor in a Motion Picture - Drama':'actor',
'Best Performance by an Actor in a Motion Picture - Musical or Comedy':'actor',
'Actor In A Leading Role - Musical Or Comedy':'actor',
'Actor In A Leading Role':'actor',
'Best Performance by an Actress in a Motion Picture - Drama':'actress',
'Best Performance by an Actress in a Motion Picture - Musical or Comedy':'actress',
'Actress In A Leading Role - Musical Or Comedy':'actress',
'Actress In A Leading Role':'actress',
'Documentary':'doc',
'Foreign Film - Foreign Language':'foreign',
'Foreign Film - English':'foreign',
'Best Original Score - Motion Picture':'score',
'Best Screenplay - Motion Picture':'screenplay',
'Best Original Song - Motion Picture':'song'}
gg = gg[gg['category'].isin(list(gg_rep.keys()))].copy()
gg['category'] = gg['category'].replace(gg_rep)
gg['nominee'] = gg['nominee'].str.upper()
gg['film'] = gg['film'].str.upper()
gg = gg.reset_index(drop=True)
gg = gg.rename(columns={'year_award':'year'})
gg = gg.drop(columns=['win'])
gg = gg.rename(columns={'nominee':'g_nominee','film':'g_film'})


# %%
osc = pd.read_csv('awarddata/oscars.csv')
osc = osc[osc['win'] == True].copy()
osc = osc.drop(['year_film', 'ceremony'], axis =1).copy()
osc_rep = {'BEST PICTURE':'picture',
'DIRECTING':'directing',
'ACTOR IN A SUPPORTING ROLE':'sup actor',
'ACTRESS IN A SUPPORTING ROLE':'sup actress',
'ACTOR':'actor',
'ACTRESS':'actress',
'CINEMATOGRAPHY':'cinematography',
'DOCUMENTARY (Feature)':'doc',
'FOREIGN LANGUAGE FILM':'foreign',
'SOUND':'sound',
'MUSIC (Original Score)':'score',
'WRITING (Original Screenplay)':'screenplay',
'FILM EDITING':'editing',
'MUSIC (Original Song)':'song'}
osc = osc[osc['category'].isin(list(osc_rep.keys()))].copy()
osc['category'] = osc['category'].replace(osc_rep)
osc['name'] = osc['name'].str.upper()
osc['film'] = osc['film'].str.upper()
osc = osc.reset_index(drop=True)
osc = osc.rename(columns={'year_ceremony':'year', 'name':'o_nominee', 'film':'o_film'})
osc = osc.drop(columns=['win'])


# %%
sag = pd.read_csv('awarddata/sag.csv')
sag = sag[sag['won'] == True].copy()
sag['year'] = sag['year'].str.split(' - ', expand=True)[0]
sag_rep = {
'MALE SUPPORTING ROLE':'sup actor',
'MALE ACTOR IN A SUPPORTING ROLE':'sup actor',
' MALE ACTOR IN A SUPPORTING ROLE':'sup actor',
'MALE SUPPORT IN A MOTION PICTURE': 'sup actor',
'MALE SUPPORT IN A MOTION PICTURE ': 'sup actor',
' MALE SUPPORT IN A MOTION PICTURE': 'sup actor',
'MALE SUPPORT':'sup actor',
'FEMALE SUPPORTING ROLE':'sup actress',
'FEMALE ACTOR IN A SUPPORTING ROLE':'sup actress',
' FEMALE ACTOR IN A SUPPORTING ROLE':'sup actress',
'FEMALE ACTOR IN A SUPPORTING ROLE ':'sup actress',
'FEMALE SUPPORT IN A MOTION PICTURE':'sup actress',
'FEMALE SUPPORT':'sup actress',
' FEMALE SUPPORT':'sup actress',
'FEMALE SUPPORT ':'sup actress',
'MALE LEAD ROLE':'actor',
'MALE LEAD':'actor',
'MALE ACTOR IN A LEADING ROLE':'actor',
'MALE LEAD IN A MOTION PICTURE':'actor',
' MALE ACTOR IN A LEADING ROLE':'actor',
'FEMALE LEAD ROLE':'actress',
'FEMALE LEAD':'actress',
'FEMALE ACTOR IN A LEADING ROLE':'actress',
' FEMALE ACTOR IN A LEADING ROLE':'actress',
'FEMALE LEAD IN A MOTION PICTURE':'actress'}
sag = sag[sag['category'].isin(list(sag_rep.keys()))].copy()
sag = pd.concat([pd.DataFrame(np.reshape(['2018', '2015', 'sup actress', 'sup actress', 'ALLISON JANNEY', 'PATRICIA ARQUETTE', 'I, TONYA', 'BOYHOOD', True, True], (5,2)).T, columns=['year', 'category','full_name', 'show', 'won']), sag])
sag['category'] = sag['category'].replace(sag_rep)
sag['full_name'] = sag['full_name'].str.upper()
sag['show'] = sag['show'].str.upper()
sag = sag.reset_index(drop=True)
sag = sag.drop(20)
sag = sag.reset_index(drop=True)
sag = sag.rename(columns={'full_name':'name', 'name': 's_nominee', 'film': 's_film'})
sag = sag.drop(columns=['won'])


# %%
dga = pd.read_csv('awarddata/dga.csv')
dga['d_nominee'] = dga['d_nominee'].str.upper()
dga['d_film'] = dga['d_film'].str.upper()
dga['year'] = dga['year'] + 1


# %%
# Directors
o_dir = osc[osc['category'] == 'directing']
g_dir = gg[gg['category'] == 'directing']
b_dir = bafta[bafta['category'] == 'directing']
df = o_dir.merge(g_dir, on='year', how='outer').copy()
df = df.merge(b_dir, on='year', how='outer').copy()
df = df.merge(dga, on='year', how='outer').copy()
direct = df[df['category_y'].notnull()]
direct_all = direct[(direct['o_film'] == direct['g_film']) & ((direct['o_film'] == direct['b_nominee']) | (direct['o_film'] == direct['b_winner'])) & (direct['o_film'] == direct['d_film'])].copy()
direct_one = direct[(direct['o_nominee'] == direct['g_film']) | ((direct['o_film'] == direct['b_nominee']) | (direct['o_film'] == direct['b_winner'])) | (direct['o_film'] == direct['d_film'])].copy()
direct_none = direct[(direct['o_nominee'] != direct['g_film']) & ((direct['o_film'] != direct['b_nominee']) | (direct['o_film'] != direct['b_winner'])) & (direct['o_film'] != direct['d_film'])].copy()


# %%


