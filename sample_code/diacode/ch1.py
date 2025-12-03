################chapter 1 sample_code

def ball_trajectory(x):
    location = 10 * x - 5 * (x ** 2)
    return (location)


import matplotlib.pyplot as plt

xs = [x / 100 for x in list(range(201))]
ys = [ball_trajectory(x) for x in xs]
plt.plot(xs, ys)
plt.title('The Trajectory of a Thrown Ball')
plt.xlabel('Horizontal Position of Ball')
plt.ylabel('Vertical Position of Ball')
plt.axhline(y=0)
plt.show()

xs2 = [0.1, 2]
ys2 = [ball_trajectory(0.1), 0]

xs3 = [0.2, 2]
ys3 = [ball_trajectory(0.2), 0]
xs4 = [0.3, 2]
ys4 = [ball_trajectory(0.3), 0]
plt.title('The Trajectory of a Thrown Ball - with Lines of Sight')
plt.xlabel('Horizontal Position of Ball')
plt.ylabel('Vertical Position of Ball')
plt.plot(xs, ys, xs2, ys2, xs3, ys3, xs4, ys4)
plt.show()

xs5 = [0.3, 0.3]
ys5 = [0, ball_trajectory(0.3)]
xs6 = [0.3, 2]
ys6 = [0, 0]
plt.title('The Trajectory of a Thrown Ball - Tangent Calculation')
plt.xlabel('Horizontal Position of Ball')
plt.ylabel('Vertical Position of Ball')
plt.plot(xs, ys, xs4, ys4, xs5, ys5, xs6, ys6)
plt.text(0.31, ball_trajectory(0.3) / 2, 'A', fontsize=16)
plt.text((0.3 + 2) / 2, 0.05, 'B', fontsize=16)
plt.show()
