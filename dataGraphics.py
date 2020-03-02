import pandas as pd
import SQL_Engine
import matplotlib.pyplot as plt
import numpy as np

genderFrame = (SQL_Engine.select("PatientGender", "Patient"))
num_male = genderFrame[genderFrame.PatientGender == 'M']


def pieChart(data, labels, color):
    plt.pie(data, labels=labels, colors=color, autopct='%1.1f%%')
    plt.show()


def performanceMeasurement(date, performance1, performance2):
    df = pd.DataFrame({'x': range(1, 11), 'RANDOM1': np.random.randn(10),
                   'RANDOM2': np.random.randn(10) + range(1, 11),
                   'RANDOM3': np.random.randn(10) + range(11, 21)})

    # multiple line plot
    plt.plot('x', 'RANDOM1', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4,
             label='male')
    plt.plot('x', 'RANDOM2', data=df, marker='', color='olive', linewidth=2, label='female')
    plt.plot('x', 'RANDOM3', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
    plt.legend()
    plt.show()

pieChart([len(num_male),len(genderFrame)-len(num_male)], ['male', 'female'], ['#6e93cd', '#fbb7e0'])
performanceMeasurement(0,0,0)
