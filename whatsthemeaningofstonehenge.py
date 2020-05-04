import numpy as np
import matplotlib.pyplot as plt

# set probabilities
probabilities = [0]*90
probabilities[15:30] = [0.5/15]*15
probabilities[10:15] = [0.3/15]*5
probabilities[30:40] = [0.3/15]*10
probabilities[5:10] = [0.15/35]*5
probabilities[40:70] = [0.15/35]*30
probabilities[0:5] = [0.05/25]*5
probabilities[70:90]  = [0.05/25]*20

# check probabilities
# print(probabilities)
# print(sum(probabilities))
# plt.scatter(range(90), probabilities)
# plt.show()

#generate 100 exam samples of 50 students each
exams = [np.random.choice(range(90), 50, p=probabilities)
         for i in range(100)]

#compute cost function
def cost(students_delay, profs_delay):
    return (students_delay + 50*profs_delay)/100

#compute delay and cost function given scheduled time
def simulate(scheduled_time):
    mean_students_delay = 0
    mean_profs_delay = 0
    for exam in exams:
        # compute real time
        # nie jestem przekonana czy potrzeba całej listy real_time czy tylko ostatniego
        # ale na razie ją trzymam
        # bo mogę
        real_exam_time = list()
        real_exam_time.append(0)
        for i in range(1, 50): #tu jest brzydka pętla którą zamienię na wytwornik
            real_exam_time.append(max(scheduled_time[i], real_exam_time[i-1]+exam[i-1]))
            mean_students_delay += max((real_exam_time[i-1] + exam[i-1] - scheduled_time[i]), 0)
            mean_profs_delay += max(scheduled_time[i] - real_exam_time[i-1] - exam[i-1], 0)
    mean_students_delay /= len(exams)
    mean_profs_delay /= len(exams)
    #print("duration:", scheduled_time[1], mean_students_delay, mean_profs_delay)
    return cost(mean_students_delay, mean_profs_delay)

#strategy number one: k minutes each
results = [round(simulate([k*i for i in range(50)])) for k in range(90)]
print(*[(i,result) for i, result in enumerate (results)], sep='\n')
plt.plot(results)
plt.show()

