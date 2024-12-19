import streamlit as st
import pandas as pd
import numpy as np

import altair as alt

import matplotlib.pyplot as plt
import seaborn as sns

import os


st.set_page_config(page_title="Tips", page_icon="📈")

st.title('Чаевые')

st.write("""
        ## Страница создана для визуализации данных датасета tips.csv \n
        ### Загрузите файл **tips.csv** \n
        #### [Скачать файл](https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv)     
        """)

#Функция кэширования

@st.cache_data
def cached_file():
    PATH = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv'
    tips_cached = pd.read_csv(PATH)
    return tips_cached

#Функция загрузки файла

@st.cache_data
def upload(cached, uploaded):
    if uploaded is not None:
        tips = pd.read_csv(uploaded)
        
        if cached.shape == tips.shape:
            st.sidebar.write('Загружено')
            st.write('### Файл успешно загружен \n Вот его первые **8** строчек')
            st.write(tips.head(8))
            return tips
        else:
            st.sidebar.write('Загружен не тот файл')
            st.stop()
    
    else:
        st.stop()

#Скачивание данных со страницы

def download(file, num):
    os.makedirs('saves', exist_ok=True)
    file_path = os.path.join('saves', file)
    plt.savefig(file_path)
    download_label = f"Скачать график {num}"
    
    with open(file_path, 'rb') as png:
        st.sidebar.download_button(
            label=download_label,
            data=png,
            file_name=file
        )

#Основные переменные
cached_tips = cached_file()
file = st.sidebar.file_uploader('Загрузи в меня CSV файл', type='csv')
tips = upload(cached_tips, file)

#Подготовка датасета

dstart = '2023-01-01'
dstop = '2023-01-31'

drange = pd.date_range(start=dstart, end=dstop)

tips['time_order'] = np.random.choice(drange, size=len(tips))
tips['time_order'] = pd.to_datetime(tips['time_order'])

#Вывод первого графика
#Динамика чаевых во времени

group = tips.groupby('time_order')['tip'].sum().reset_index()

st.write('## 1. График, отражающий динамику чаевых во времени')
st.line_chart(group, x='time_order', y='tip', x_label='Дата', y_label='Чаевые')
st.write('\n')
#Хитрый метод сохранения графика сделанного через line_chart
fig, ax_1 = plt.subplots(figsize=(16, 5))
ax_1.plot(group['time_order'], group['tip'], marker='.')
ax_1.set_xlabel('Дата')
ax_1.set_ylabel('Всего донатов')
ax_1.set_title('Динамика донатов от даты')
chart1 = fig
download('tips_in-time.png', 1)

#Вывод графика 2
#То же самое, только используя replot

chart2 = sns.relplot(data=group, y='time_order', x='tip', size=group.index, color='g')
chart2.set_axis_labels('Чаевые', 'Дата')

st.write('## 2. График динамики чаевых во времени с помощью **relplot**')
st.pyplot(chart2)
st.write('\n')
download('tips_in-time_relplot.png', 2)

#Вывод графика 3

st.write('## 3. Гистограмма по колонке **total_bill**')
fig3, ax_3 = plt.subplots()
sns.histplot(data=tips, x='total_bill')
ax_3.set_xlabel('Общий счёт')
ax_3.set_ylabel('Частота')
st.pyplot(fig3)
download('total_bill.png', 3)
st.write('\n')

#Вывод графика 4

st.write('## 4. График, аналогичный предыдущему, построенный с использованием метода **displot**')

chart4 = sns.displot(data=tips, x='total_bill', col='time', kde=True, kind='hist')
chart4.set_axis_labels('Чаевые', 'Количество')
st.pyplot(chart4)
download('total_bill_same-same_but_different.png', 4)
st.write('\n')

#Вывод графика 5

st.write('## 5. **scatterplot**, показывающий связь между общим счётом и чаевыми')

fig5, ax5 = plt.subplots()
sns.scatterplot(data=tips, x='tip', y='total_bill', hue='smoker', legend=False, ax=ax5)
ax5.set_xlabel('Чаевые')
ax5.set_ylabel('Общий счёт')
ax5.legend(title='Курильщик', labels=['Да', 'Нет'])
st.pyplot(fig5)
download('scatterplot_totalbill_tip.png', 5)
st.write('\n')

#Вывод графика 6

st.write('## 6. Аналогичный график, только через **replot**')
chart6 = sns.relplot(data=tips, y='total_bill', x='tip', kind='scatter', hue='smoker')
chart6.set_axis_labels('Чаевые', 'Общий счёт') 
st.pyplot(chart6)
download('same-same_but_different_relplot.png', 6)
st.write('\n')

#Вывод графика 7

st.write('## 7. График, связывающий параметры **total_bill**, **tip** и **size**')
chart7 = sns.relplot(data=tips, x='total_bill', y='tip', size='size', marker='o', hue='size')
chart7.set_axis_labels('Чаевые', 'Общий счёт') 
st.pyplot(chart7)
download('chart_totalbill_tip_and_size.png', 7)
st.write('\n')

#Вывод графика 8

st.write('## 8. Наглядная демонстрация связи между днём недели и размером счёта')
chart8 = sns.catplot(data=tips, y='total_bill', x='day', kind='violin')
chart8.set_axis_labels('День', 'Общий счёт')
st.pyplot(chart8)
download('demonstration_by_day_titalbill.png', 8)
st.write('\n')

#Вывод графика 9

st.write('## 9. _scatterplot_ с днём недели по оси **Y**, чаевыми по оси **X**, и цветом по полу')
fig9, ax9 = plt.subplots()
sns.scatterplot(data=tips, x='tip', y='day', hue='sex', ax=ax9)
ax9.set_xlabel('Чаевые')
ax9.set_ylabel('День недели')
ax9.legend(title='Пол', labels=['Мужчина', 'Женщина'])
st.pyplot(fig9)
download('scatterplot_dayY_tipsX_colorsex.png', 9)
st.write('\n')

#Вывод графика 10

st.write('## 10. _boxplot_ с суммой всех счетов за каждый день, разбивая по времени на ужин (Dinner) и обед (Lunch)')
df = tips.copy()
df['total_bill'].sum()
fig10, ax10 = plt.subplots()
sns.boxplot(data=df, x='time', y='total_bill', hue='time')
ax10.set_xlabel('Время дня')
ax10.set_ylabel('Общий чек')
st.pyplot(fig10)
download('boxplot_forewer.png', 10)
st.write('\n')

#Вывод графика 11

st.write('## 11. Аналогичный график, только используя метод _catplot_')
chart11 = sns.catplot(kind='bar', data=tips, y='total_bill', x='time', hue='day')
chart11.set_axis_labels('Время дня', 'Общий чек')
st.pyplot(chart11)
download('same-same_boxplot_forewer.png', 11)
st.write('\n')

#Вывод графика 12

lunch_tip = tips[tips['time'] == 'Lunch']
dinner_tip = tips[tips['time'] == 'Dinner']

st.write('## 12. Гистограммы чаевых на ужин и обед')
fig12, ax12 = plt.subplots(1, 2, figsize=(12, 8))
sns.histplot(data=lunch_tip['tip'],
             bins=10,
             kde=False,
             color='b', ax=ax12[0])
ax12[0].set_xlabel('Cуммаа чаевых')
ax12[0].set_ylabel('Количество')
ax12[0].set_label('Чаевые на обед')

sns.histplot(dinner_tip['tip'], 
             bins=10, 
             kde=False, 
             color='salmon', ax=ax12[1])
ax12[1].set_title("Чаевые на ужин")
ax12[1].set_xlabel("Сумма чаевых")
ax12[1].set_ylabel('Количество')
st.pyplot(fig12)
download('histogramms_of_happyness.png', 12)
st.write('\n')

#Вывод графика 13

st.write("""### 13. 2 графика _разброса_ для мужчин и для женщин. \n
         тут представлена связь размера счёта и чаевых, с дополнительным
         разбиением на курящих и не курящих \n""")
st.write('Реализован данный график с помощью _Altair_')

male = tips[tips['sex'] == 'Male']
female = tips[tips['sex'] == 'Female']

cmale = alt.Chart(male).mark_point().encode(
    x=alt.X('total_bill', title='Общий чек'),
    y=alt.Y('tip', title='Чаевые'),
    color='smoker',
    shape='smoker',
    tooltip=['total_bill', 'tip', 'smoker']
).properties(
    title='Чаевые - мужчины'
)

cfemale = alt.Chart(female).mark_point().encode(
    x=alt.X('total_bill', title='Общий чек'),
    y=alt.Y('tip', title='Чаевые'),
    color='smoker',
    shape='smoker',
    tooltip=['total_bill', 'tip', 'smoker']
).properties(
    title='Чаевые - женщины'
)

st.altair_chart(cmale | cfemale, use_container_width=True)
st.write('\n')
#Хитрость для скачивания графиков)) 
fig13, ax13 = plt.subplots(1, 2, figsize=(12, 8))
sns.scatterplot(data=tips[tips['sex'] == 'Male'], 
            x='total_bill', 
            y='tip', 
            hue='smoker', ax=ax13[0])
ax13[0].set_title('Чаевые - мужчины')
ax13[0].set_xlabel('Счёт')
ax13[0].set_ylabel('Чаевые')

sns.scatterplot(data=tips[tips['sex'] == 'Female'], 
            x='total_bill', 
            y='tip', 
            hue='smoker', ax=ax13[1])
ax13[1].set_title('Чаевые - женщины')
ax13[1].set_xlabel('Счёт')
ax13[1].set_ylabel('Чаевые')
download('13_grafic.png', 13)

#Вывод графика 14

st.write('### 14. Тепловая карта зависимостей численных переменных')

hm = tips.copy()
hm = hm[['total_bill', 'tip', 'size', 'time_order']]

hm = hm.corr(method='spearman', min_periods=10, numeric_only=True)

fig14, ax14 = plt.subplots()
sns.heatmap(hm, annot=True, ax=ax14)
st.pyplot(fig14)
download('HeatMap.png', 14)

st.write('## А на сегодня всё!')
st.write('### Cпасибо за использование нашего сервиса!')
