import copy
import sys

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
    return (students_delay + number_of_students*prof_waiting_time)/(2*number_of_students) # multiply prof by number of students (50)

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

    return xmin, ymin # zwroc k, dla ktorego jest najmniejszy delay

def based_on_results_permutation(min_k, min_delay, exams, scheduled_time, is_multiple = False, number_of_days = 1):

    most_optimal_all = list()

    for exam in exams:
        min_variation = abs(exam[0] - min_k)
        index = 0
        most_optimal = list()
        while True:
            min_variation = sys.maxsize
            for i in range(len(exam)):
                if abs(exam[i] - min_k) < min_variation:
                    min_variation = abs(exam[i] - min_k)
                    index = i
            if exam[index] == sys.maxsize:
                break
            most_optimal.append(exam[index])
            exam[index] = sys.maxsize

        most_optimal_all.append(most_optimal)

    if is_multiple:
        current_result = simulate_multiple_days(scheduled_time, number_of_days, most_optimal_all)
    else:
        current_result = simulate(scheduled_time, most_optimal_all)

    print("K: ", min_k)
    print("OPTIMAL ", current_result, " OUR SIMULATED RESULT ", min_delay)

def single_day(exams):
    #strategy number one: k minutes each
    results = [round(simulate([k*i for i in range(len(exams[0]))], exams)) for k in range(90)]

    enumerated_results = [(i, result) for i, result in enumerate (results)]
    print(enumerated_results, sep='\n')

    min_k, min_delay = annot_min(np.array([tup[0] for tup in enumerated_results]), np.array([tup[1] for tup in enumerated_results]))

    plt.plot(results)
    plt.show()

    based_on_results_permutation(min_k, min_delay, copy.deepcopy(exams), [min_k*i for i in range(len(exams[0]))])

    return min_k, min_delay

print("SINGLE DAY")
single_day(exams)
print()


#strategy: n students every k minutes
def single_day_few_students_one_time(number_of_students_per_time, exams):
    #results = [round(simulate([k*i for i in range(len(exams[0]))], exams)) for k in range(90)]

    results = list()
    for k in range(200):
        scheduled_time = list()
        for i in range(len(exams[0])//number_of_students_per_time + 3):
            for j in range(number_of_students_per_time):
                scheduled_time.append(k*i)

        # scheduled_time = [k*i for i in range(len(exams[0]))]
        results.append(simulate(scheduled_time, exams))

    enumerated_results = [(i, result) for i, result in enumerate (results)]
    print(enumerated_results, sep='\n')

    min_k, min_delay = annot_min(np.array([tup[0] for tup in enumerated_results]), np.array([tup[1] for tup in enumerated_results]))

    plt.plot(results)
    plt.show()

    best_scheduled = list()
    for i in range(len(exams[0]) // number_of_students_per_time + 3):
        for j in range(number_of_students_per_time):
            best_scheduled.append(min_k * i)

    based_on_results_permutation(min_k//number_of_students_per_time, min_delay, copy.deepcopy(exams), best_scheduled)

    return min_k, min_delay

print("SINGLE DAY, FEW ONE TIME")
single_day_few_students_one_time(3, exams)
print()



#na razie zakladamy, ze number_of_days dzieli 50
def simulate_multiple_days(scheduled_time, number_of_days, exams):
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


        sum_students_delay /= number_of_days
        sum_students += sum_students_delay
        sum_prof += sum_prof_waiting_time

    sum_students /= len(exams)
    sum_prof /= len(exams)
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

    min_k, min_delay = annot_min(np.array([tup[0] for tup in enumerated_results]), np.array([tup[1] for tup in enumerated_results]))

    plt.plot(results)
    plt.show()

    based_on_results_permutation(min_k, min_delay, exams[:], [min_k*i for i in range(number_of_students_per_day)], True, number_of_days)

    return min_k, min_delay

print("MULTIPLE DAYS")
multiple_days(exams)
