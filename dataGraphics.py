import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import SQLConnection
import Type_Check

dailyGoal = 10
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


def performanceMeasurement(xlab, labels):


    ypos = np.arange(len(labels))
    plt.bar(x=range(0,len(xlab)), height=xlab)
    plt.xticks(ypos, labels, fontsize=7)
    for index, value in enumerate(xlab):
        plt.text(index, value, str(value))
    plt.show()


def individualGroupByDate(userID):
    SQL = SQLConnection.SQLConnection()
    data = SQL.getIndWorkEfficiency(userID)

    # print(data.OutreachDetailsDate)
    SQL.closeConnection()
    performanceMeasurement(data['OutreachDate'], data['name'].values.tolist())

def overAll():
    SQL = SQLConnection.SQLConnection()
    data = SQL.getWorkEfficiency()

    # print(data.OutreachDetailsDate)
    SQL.closeConnection()
    performanceMeasurement(data['Count_OutreachDetailsPatientId'],data['name'].values.tolist())

# individualGroupByDate('2')






