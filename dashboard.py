import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import numpy as np

st.set_page_config(layout='centered', page_title='Dashboard by Kamentsev Artem', page_icon="🧊")
st.set_option('deprecation.showPyplotGlobalUse', False)

#Download data
@st.cache_data
def load_data(filename):
    return pd.read_csv(filename, sep = ",")

data_file = st.file_uploader("Upload CSV", type="csv")
if data_file:
    with st.sidebar:
        st.header("Ввод параметров")
        work_days = st.text_input("Количество рабочих дней", "2")
        age = st.text_input("Возраст", "35")

    work_days = int(work_days)
    age = int(age)

    st.subheader("Выбранные значения:")
    st.write("Количество рабочих дней:", work_days)
    st.write("Возраст:", age)

    data = load_data(data_file)
    data.rename(columns={'Количество больничных дней': 'work_days', 'Возраст': 'age', 'Пол': 'gender'}, inplace=True)

    st.write("* Загруженные данные:")
    st.table(data.head())
    st.write("* Описание данных:")
    st.dataframe(data.describe())
    st.write(f"Дисперсия по рабочим дням: {round(data.var()[0], 2)}")
    st.write(f"Дисперсия по возрасту: {round(data.var()[1], 2)}")
    st.write(f"Корреляция величин: {round(data.corr().iloc[0,1], 2)}")
    st.write("Уровень значимости: 0.05")

    st.header(f"Проверка 1 гипотезы: Мужчины пропускают в течение года более {work_days} рабочих дней по болезни значимо чаще женщин.")

    N1, N2 = data.gender.value_counts()
    st.write(f"* Количество мужчин: {N1}")
    st.write(f"* Количество женщин: {N2}")

    bins = np.arange(0, 10, 1)
    plt.figure(figsize=(8, 6))
    sns.histplot(data=data, x='work_days', hue='gender', kde=True, bins=bins)
    plt.title('Распределение пропущенных дней по полу')
    st.pyplot()

    sns.histplot(
        data[data.gender == 'М'].work_days, bins=bins,
        color='blue', alpha=0.5, label='M', stat='probability', kde=True)
    sns.histplot(
        data[data.gender == 'Ж'].work_days, bins=bins,
        color='orange', alpha=0.5, label='Ж', stat='probability', kde=True)
    plt.legend(loc=1)
    plt.title('Распределение вероятностей по полу')
    st.pyplot()

    t_statistic, p_value = ttest_ind(
        data[(data.gender == 'М') & (data.work_days > work_days)].work_days,
        data[(data.gender == 'Ж') & (data.work_days > work_days)].work_days,
        equal_var=False,
        alternative='less'
    )

    st.write(f'* Гипотеза 1: Мужчины пропускают в течение года более {work_days} рабочих дней по болезни значимо чаще женщин.')
    st.write('p-value:', p_value)
    st.write('  statistic:', t_statistic)

    st.write("Отвергаем гипотезу, так как p_value меньше уровня значимости 0.05" if p_value >= 0.05 else "Принимаем гипотезу, так как p_value больше уровня значимости 0.05")

    st.header(f"Проверка 2 гипотезы: Работники старше {age} лет пропускают в течение года более {work_days} рабочих дней (work_days) по болезни значимо чаще своих более молодых коллег.")

    data["age_type"] = ['old' if x > age else 'young' for x in data['age']]

    N3, N4 = data.age_type.value_counts()
    st.write(f"* Количество сотрудников старше {age} лет: {N3}")
    st.write(f"* количество сотрудников младше {age} лет: {N4}")

    sns.boxplot(x='age', y='work_days', data=data)
    plt.title('Распределение пропущенных дней по возрасту')
    st.pyplot()

    plt.figure(figsize=(8, 6))
    sns.histplot(data=data, hue='age_type', x='work_days', kde=True)
    plt.title('Распределение пропущенных дней по возрасту категориально')
    st.pyplot()

    sns.histplot(
        data[data.age_type == 'old'].work_days, bins=bins,
        color='blue', alpha=0.5, label='Old', stat='probability', kde=True)
    sns.histplot(
        data[data.age_type == 'young'].work_days, bins=bins,
        color='orange', alpha=0.5, label='Young', stat='probability', kde=True)
    plt.legend(loc=1)
    plt.title('Распределение вероятностей по возрасту категориально')
    st.pyplot()

    t_statistic, p_value = ttest_ind(
        data[(data.age_type == 'old') & (data.work_days > work_days)].work_days,
        data[(data.age_type == 'young') & (data.work_days > work_days)].work_days,
        equal_var=False,
        alternative='less'
    )

    st.write(f'Гипотеза 2: Работники старше {age} лет пропускают в течение года более {work_days} рабочих дней по болезни значимо чаще своих более молодых коллег.')
    st.write('p-value:', p_value)
    st.write('statistic:', t_statistic)

    st.write("Отвергаем гипотезу, так как p_value меньше уровня значимости 0.05" if p_value >= 0.05 else "Принимаем гипотезу, так как p_value больше уровня значимости 0.05")



