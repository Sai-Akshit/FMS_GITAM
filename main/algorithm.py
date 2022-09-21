# algorithm for data extraction
import pandas as pd
from .models import faculty_details

# default path where files are stored: media/{file_name}
def dataExtraction(file):
    df = pd.read_excel(file, sheet_name = 'Master data', skiprows=1)
    df.drop('Unnamed: 0', axis=1, inplace = True)
    df.columns = ['Name', 'ID', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 'w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9']
    df.astype({'ID':int})
    df.fillna(value= '0', axis= 1, inplace = True)


    df['Monday'] = df.m1 +" ,"+ df.m2 +" ,"+ df.m3 +" ,"+ df.m4 +" ,"+ df.m5 +" ,"+ df.m6 +" ,"+ df.m7 +" ,"+ df.m8 +" ,"+ df.m9
    df['Tuesday'] = df.t1 +" ,"+ df.t2 +" ,"+ df.t3 +" ,"+ df.t4 +" ,"+ df.t5 +" ,"+ df.t6 +" ,"+ df.t7 +" ,"+ df.t8 +" ,"+ df.t9
    df['Wednesday'] = df.w1 +" ,"+ df.w2 +" ,"+ df.w3 +" ,"+ df.w4 +" ,"+ df.w5 +" ,"+ df.w6 +" ,"+ df.w7 +" ,"+ df.w8 +" ,"+ df.w9
    df['Thursday'] = df.h1 +" ,"+ df.h2 +" ,"+ df.h3 +" ,"+ df.h4 +" ,"+ df.h5 +" ,"+ df.h6 +" ,"+ df.h7 +" ,"+ df.h8 +" ,"+ df.h9
    df['Friday'] = df.f1 +" ,"+ df.f2 +" ,"+ df.f3 +" ,"+ df.f4 +" ,"+ df.f5 +" ,"+ df.f6 +" ,"+ df.f7 +" ,"+ df.f8 +" ,"+ df.f9
    
    faculty_details.objects.all().delete()
    
    rows = df.shape
    try:
        for row in range(rows[0]):
            name_in, i_d, tt = 0, 0, []
            for i in range(len(df.iloc[row][['Name', 'ID', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']])):
                if i == 0:
                    name_in = df.iloc[row][['Name', 'ID', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']][i]
                elif i == 1:
                    i_d = int(df.iloc[row][['Name', 'ID', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']][i])
                else:
                    tt.append(df.iloc[row][['Name', 'ID', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']][i].split(" ,"))
            det = faculty_details(name= name_in, idno= i_d, timetable= tt)
            det.save()
    except:
        raise Exception("Error in data extraction")


def defineTime(post_request):
    """Genrates time indices and appends to a list"""
    indices = []
    for key in post_request:
        if post_request[key] == 'clicked':
            temp = key.replace('c', '')
            try:
                indices.append(int(temp))
            except ValueError:
                indices.append(temp)
    
    return indices


def timeIndex(timeList):
    """Subtracts 8 from every value at the index"""
    res = []
    for time in timeList:
        timeInd = time - 8
        res.append(timeInd)

    return res

def funFree(timeindex, dayList):
    res = None
    for i in timeindex:
        if dayList[i] == '0':
            res = True
        else:
            res = False
            break
    return res

def searchingFree(query_set, dayIndex, timeIndexList):
    eligibleEmps = []
    count = 1
    for emp in query_set:
        if funFree(timeIndexList, emp.timetable[dayIndex]):
            eligibleEmps.append([count, emp.name, emp.idno])
            count += 1

    return eligibleEmps


def funBusy(timeindex, daylist):
    res = None
    for i in timeindex:
        if daylist[i] != '0':
            res = True
        else:
            res = False
            break
    
    return res


def searchingBusy(query_set, dayIndex, timeIndexList):
    eligibleEmps = []
    count = 1
    for emp in query_set:
        if funBusy(timeIndexList, emp.timetable[dayIndex]):
            eligibleEmps.append([count, emp.name, emp.idno])
            count += 1

    return eligibleEmps
