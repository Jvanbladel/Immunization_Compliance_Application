from tkinter import BOTH, LEFT, TOP

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import tkinter as tk
import ICA_super
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import SQLConnection
import Type_Check

dailyGoal = 10
def ind(user):

    root = tk.Tk()

    figure1 = plt.Figure(figsize=(6, 5), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, root)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    SQL = SQLConnection.SQLConnection()
    numbers = SQL.getIndWorkEfficiency(user)
        # print(data.OutreachDetailsDate)
    SQL.closeConnection()
        # performanceMeasurement(data['OutreachDetailsDate'], data['name'].values.tolist())
    df1 = numbers[['OutreachDetailsDate', 'Count_OutreachDetailsPatientId']]
    df1.plot.bar(x='OutreachDetailsDate', y='Count_OutreachDetailsPatientId', ylim=(0,dailyGoal), rot=0, fontsize= 8,colormap="Paired", ax=ax1)

    ax1.set_title(str(numbers['name'].values[0]) + 'Work Progress')
    toolbar = NavigationToolbar2Tk(bar1, root)
    toolbar.update()
    bar1._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
    root.mainloop()

def pieChart(data, labels, color):
    plt.pie(data, labels=labels, colors=color, autopct='%1.1f%%')
    plt.show()

def multipleBar(dataMale, dataFemale, labels):
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, dataMale, width, label='Men')
    rects2 = ax.bar(x + width / 2, dataFemale, width, label='Women')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('')
    ax.set_title('')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()

    plt.show()


'''
    displaying three lines on line graph
    using matplotlib'''


def performanceMeasurement():

    root = tk.Tk()

    figure1 = plt.Figure(figsize=(6, 5), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, root)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    SQL = SQLConnection.SQLConnection()
    numbers = SQL.getWorkEfficiency()
        # print(data.OutreachDetailsDate)
    SQL.closeConnection()
        # performanceMeasurement(data['OutreachDetailsDate'], data['name'].values.tolist())
    df1 = numbers[['name', 'Count_OutreachDetailsPatientId']]
    df1.plot.bar(x='name', y='Count_OutreachDetailsPatientId', rot=0, fontsize= 8,color=(0.2, 0.4, 0.6, 0.6), ax=ax1)

    # ax1.set_title(str(numbers['name'].values[0]) + ' work progress')
    toolbar = NavigationToolbar2Tk(bar1, root)
    toolbar.update()
    bar1._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
    root.mainloop()

    '''ypos = np.arange(len(labels))
    plt.bar(x=range(0,len(xlab)), height=xlab)
    plt.xticks(ypos, labels, fontsize=7)
    for index, value in enumerate(xlab):
        plt.text(index, value, str(value))
    plt.show()'''


def individualGroupByDate(userID):
    SQL = SQLConnection.SQLConnection()
    data = SQL.getIndWorkEfficiency(userID)

    # print(data.OutreachDetailsDate)
    SQL.closeConnection()
    # performanceMeasurement(data['OutreachDetailsDate'], data['name'].values.tolist())
    plt.bar(x=range(0, len(data['OutreachDetailsDate'])), height=data['Count_OutreachDetailsPatientId'])
    # print(data['name'].values[0])
    plt.title(str(data['name'].values[0])+' work progress')
    dateTime = data['OutreachDetailsDate'].values.tolist()
    date = []
    for d in dateTime:
        date.append(d[:10])
    # print(date)
    plt.xticks(range(0,len(date)), date,rotation = 20, fontsize=7)
    plt.ylim(0, dailyGoal)
    for index, value in enumerate(data['Count_OutreachDetailsPatientId']):
        plt.text(index, value, str(value))
    plt.show()

def overAll():
    SQL = SQLConnection.SQLConnection()
    data = SQL.getWorkEfficiency()
    # print(data.OutreachDetailsDate)
    SQL.closeConnection()

    performanceMeasurement(data['Count_OutreachDetailsPatientId'],data['name'].values.tolist())

#individualGroupByDate('2')






