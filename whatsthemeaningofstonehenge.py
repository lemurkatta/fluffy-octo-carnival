import numpy as np
import matplotlib.pyplot as plt

# set probabilities
# probabilities = [0]*90
# probabilities[15:30] = [0.5/15]*15
# probabilities[10:15] = [0.3/15]*5
# probabilities[30:40] = [0.3/15]*10
# probabilities[5:10] = [0.15/35]*5
# probabilities[40:70] = [0.15/35]*30
# probabilities[0:5] = [0.05/25]*5
# probabilities[70:90]  = [0.05/25]*20

# check probabilities
# print(probabilities)
# print(sum(probabilities))
# plt.scatter(range(90), probabilities)
# plt.show()

#generate 100 exam samples of 50 students each
# exams = [np.random.choice(range(90), 50, p=probabilities)
#          for i in range(100)]

exams = [np.random.normal(30, 10, 50)
         for i in range(100)]

#compute cost function
def cost(students_delay, prof_waiting_time, number_of_students):
    return (students_delay + number_of_students*prof_waiting_time)/(2*number_of_students)  # multiply prof by number of students (50)

#compute delay and cost function given scheduled time
def simulate(scheduled_time, exams):
    mean_students_delay = 0
    mean_prof_waiting_time = 0
    for exam in exams:
        # compute real time
        # nie jestem przekonana czy potrzeba całej listy real_time czy tylko ostatniego
        # ale na razie ją trzymam
        # bo mogę
        real_exam_time = list()
        real_exam_time.append(0)
        for i in range(1, len(exam)): #tu jest brzydka pętla którą zamienię na wytwornik
            real_exam_time.append(max(scheduled_time[i], real_exam_time[i-1]+exam[i-1]))
            mean_students_delay += max((real_exam_time[i-1] + exam[i-1] - scheduled_time[i]), 0)
            mean_prof_waiting_time += max(scheduled_time[i] - real_exam_time[i-1] - exam[i-1], 0)
    mean_students_delay /= len(exams)
    mean_prof_waiting_time /= len(exams)
    #print("duration:", scheduled_time[1], mean_students_delay, mean_profs_delay)
    return cost(mean_students_delay, mean_prof_waiting_time, len(exams[0]))

# ze stacka rysowanie strzałki
def annot_min(x,y, ax=None):
    xmin = x[np.argmin(y)]
    ymin = y.min()
    text= "k={:.3f}, delay={:.3f}".format(xmin, ymin)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmin, ymin), xytext=(0.50,0.96), **kw)

def single_day(exams):
    #strategy number one: k minutes each
    results = [round(simulate([k*i for i in range(len(exams[0]))], exams)) for k in range(90)]

    enumerated_results = [(i, result) for i, result in enumerate (results)]
    print(enumerated_results, sep='\n')

    annot_min(np.array([tup[0] for tup in enumerated_results]), np.array([tup[1] for tup in enumerated_results]))

    plt.plot(results)
    plt.show()

# single_day(exams)


#na razie zakladamy, ze number_of_days dzieli 50
def simulate_multiple_days(scheduled_time, number_of_days, exams):
    print(scheduled_time)
    number_of_students_per_day = len(exams[0])//number_of_days

    sum_students = 0
    sum_prof = 0
    for exam in exams:
        sum_students_delay = 0
        sum_prof_waiting_time = 0
        for day in range(number_of_days):
            mean_students_delay_per_day = 0
            mean_prof_waiting_time_per_day = 0
            current_day_list_exam = exam[day*number_of_students_per_day:(day+1)*number_of_students_per_day]
            real_exam_time = list()
            real_exam_time.append(0)
            for i in range(1, len(current_day_list_exam)):  # tu jest brzydka pętla którą zamienię na wytwornik
                real_exam_time.append(max(scheduled_time[i], real_exam_time[i - 1] + current_day_list_exam[i - 1]))
                mean_students_delay_per_day += max((real_exam_time[i - 1] + current_day_list_exam[i - 1] - scheduled_time[i]), 0)
                mean_prof_waiting_time_per_day += max(scheduled_time[i] - real_exam_time[i - 1] - current_day_list_exam[i - 1], 0)

            mean_students_delay_per_day /= number_of_students_per_day
            #mean_prof_waiting_time_per_day /= len(number_of_students_per_day)
            sum_students_delay += mean_students_delay_per_day
            sum_prof_waiting_time += mean_prof_waiting_time_per_day
            print(mean_students_delay_per_day, " STUDENTS DEL")
            print(mean_prof_waiting_time_per_day, " PROF DEL")

        sum_students_delay /= number_of_days
        sum_students += sum_students_delay
        sum_prof += sum_prof_waiting_time

    sum_students /= len(exams)
    sum_prof /= len(exams)
    print((sum_students + sum_prof)/2)
    return (sum_students + sum_prof)/2


def multiple_days(exams):
    number_of_days = 5
    number_of_students_per_day = len(exams[0]) // number_of_days

    results = list()
    for k in range(90):
        scheduled_time = [k*i for i in range(number_of_students_per_day)]
        results.append(simulate_multiple_days(scheduled_time, number_of_days, exams))

    #results = [round(simulate_multiple_days([k*i for i in range(number_of_students_per_day)], number_of_days, exams)) for k in range(90)]

    enumerated_results = [(i, result) for i, result in enumerate (results)]
    print(enumerated_results, sep='\n')

    annot_min(np.array([tup[0] for tup in enumerated_results]), np.array([tup[1] for tup in enumerated_results]))

    plt.plot(results)
    plt.show()

multiple_days(exams)


