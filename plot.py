import numpy as np
import matplotlib.pyplot as plt

def pm(v0, angle, g=9.81, t_max=5, dt=0.01):
    theta = np.radians(angle)
    t = np.arange(0, t_max, dt)
    x = v0 * np.cos(theta) * t
    y = v0 * np.sin(theta) * t - 0.5 * g * t**2
    return x, y

def pm_air_resistance(v0, angle, C_d, A, rho, mass, g, t_max, dt):
    theta = np.radians(angle)
    vx0 = v0 * np.cos(theta)
    vy0 = v0 * np.sin(theta)

    t = np.arange(0, t_max, dt)
    x = np.zeros_like(t)
    y = np.zeros_like(t)
    vx = np.zeros_like(t)
    vy = np.zeros_like(t)

    vx[0] = vx0
    vy[0] = vy0

    for i in range(1, len(t)):
        v = np.sqrt(vx[i-1]**2 + vy[i-1]**2)
        F_d = 0.5 * C_d * A * rho * v**2
        ax = -F_d * vx[i-1] / v / mass
        ay = -g - (F_d * vy[i-1] / v / mass)
        vx[i] = vx[i-1] + ax * dt
        vy[i] = vy[i-1] + ay * dt
        x[i] = x[i-1] + vx[i-1] * dt
        y[i] = y[i-1] + vy[i-1] * dt
        if y[i] < 0:
            break

    return x[:i], y[:i]

def pm_magnus_forces(v0, angle, omega, S, C_d, A, rho, mass, g, t_max, dt):
    theta = np.radians(angle)
    vx0 = v0 * np.cos(theta)
    vy0 = v0 * np.sin(theta)

    t = np.arange(0, t_max, dt)
    x = np.zeros_like(t)
    y = np.zeros_like(t)
    vx = np.zeros_like(t)
    vy = np.zeros_like(t)

    vx[0] = vx0
    vy[0] = vy0

    for i in range(1, len(t)):
        v = np.sqrt(vx[i-1]**2 + vy[i-1]**2)
        F_d = 0.5 * C_d * A * rho * v**2
        F_m = S * omega * v
        ax = -F_d * vx[i-1] / v / mass + F_m * vy[i-1] / v / mass
        ay = -g - (F_d * vy[i-1] / v / mass) + F_m * vx[i-1] / v / mass
        
        vx[i] = vx[i-1] + ax * dt
        vy[i] = vy[i-1] + ay * dt
        x[i] = x[i-1] + vx[i-1] * dt
        y[i] = y[i-1] + vy[i-1] * dt
        if y[i] < 0:
            break

    return x[:i], y[:i]

# variables
v0 = 50
angle = 45
C_d = 0.47
A = 0.01
rho = 1.225
mass = 0.145
g = 9.81
t_max = 5
dt = 0.01
omega = 50

# target
target_x = 7  # meters
target_y = 3  # meters
target_width = 1  # meters
target_height = 1  # meters

model = 'pm_magnus_forces'

if model == 'pm':
    x, y = pm(v0, angle, g, t_max, dt)
elif model == 'pm_air_resistance':
    x, y = pm_air_resistance(v0, angle, C_d, A, rho, mass, g, t_max, dt)
elif model == 'pm_magnus_forces':
    x, y = pm_magnus_forces(v0, angle, omega, S=1e-4, C_d=C_d, A=A, rho=rho, mass=mass, g=g, t_max=t_max, dt=dt)

plt.figure()
plt.plot(x, y, label='Projectile Path')
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.title('Projectile Motion Target')
plt.grid()

plt.gca().add_patch(plt.Rectangle((target_x, target_y), target_width, target_height, edgecolor='r', facecolor='none', lw=2, label='Target'))

plt.legend()
plt.show()
