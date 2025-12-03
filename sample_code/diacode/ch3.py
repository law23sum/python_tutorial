###################chapter 3


def revenue(tax):
    return (100 * (math.log(tax + 1) - (tax - 0.2) ** 2 + 0.04))


import matplotlib.pyplot as plt

xs = [x / 1000 for x in range(1001)]
ys = [revenue(x) for x in xs]
plt.plot(xs, ys)
plt.title('Tax Rates and Revenue')
plt.xlabel('Tax Rate')
plt.ylabel('Revenue')
plt.show()

import matplotlib.pyplot as plt

xs = [x / 1000 for x in range(1001)]
ys = [revenue(x) for x in xs]
plt.plot(xs, ys)
current_rate = 0.7
plt.plot(current_rate, revenue(current_rate), 'ro')
plt.title('Tax Rates and Revenue')
plt.xlabel('Tax Rate')
plt.ylabel('Revenue')
plt.show()


def revenue_derivative(tax):
    return (100 * (1 / (tax + 1) - 2 * (tax - 0.2)))


print(revenue_derivative(0.7))

step_size = 0.001

current_rate = current_rate + step_size * revenue_derivative(current_rate)

current_rate = current_rate + step_size * revenue_derivative(current_rate)

threshold = 0.0001

threshold = 0.0001
maximum_iterations = 100000
keep_going = True
iterations = 0
while (keep_going):
    rate_change = step_size * revenue_derivative(current_rate)
    current_rate = current_rate + rate_change
    if (abs(rate_change) < threshold):
        keep_going = False
    if (iterations >= maximum_iterations):
        keep_going = False
        iterations = iterations + 1

import math


def income(edu_yrs):
    return (math.sin((edu_yrs - 10.6) * (2 * math.pi / 4)) + (edu_yrs - 11) / 2)


import matplotlib.pyplot as plt

xs = [11 + x / 100 for x in list(range(901))]
ys = [income(x) for x in xs]
plt.plot(xs, ys)
current_edu = 12.5
plt.plot(current_edu, income(current_edu), 'ro')
plt.title('Education and Income')
plt.xlabel('Years of Education')
plt.ylabel('Lifetime Income')
plt.show()


def income_derivative(edu_yrs):
    return (math.cos((edu_yrs - 10.6) * (2 * math.pi / 4)) + 1 / 2)


threshold = 0.0001
maximum_iterations = 100000
current_education = 12.5
step_size = 0.001
keep_going = True
iterations = 0
while (keep_going):
    education_change = step_size * income_derivative(current_education)
    current_education = current_education + education_change
    if (abs(education_change) < threshold):
        keep_going = False
    if (iterations >= maximum_iterations):
        keep_going = False
    iterations = iterations + 1


def revenue_flipped(tax):
    return (0 - revenue(tax))


import matplotlib.pyplot as plt

xs = [x / 1000 for x in range(1001)]
ys = [revenue_flipped(x) for x in xs]
plt.plot(xs, ys)
plt.title('The Tax/Revenue Curve - Flipped')
plt.xlabel('Current Tax Rate')
plt.ylabel('Revenue - Flipped')
plt.show()

threshold = 0.0001
maximum_iterations = 10000


def revenue_derivative_flipped(tax):
    return (0 - revenue_derivative(tax))


current_rate = 0.7
keep_going = True
iterations = 0
while (keep_going):
    rate_change = step_size * revenue_derivative_flipped(current_rate)
    current_rate = current_rate - rate_change
    if (abs(rate_change) < threshold):
        keep_going = False
    if (iterations >= maximum_iterations):
        keep_going = False
    iterations = iterations + 1
