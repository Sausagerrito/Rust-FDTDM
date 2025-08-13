import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import glob
import os

# Get all CSV frames, sort by timestep number
files = sorted(glob.glob("data/frame_*.csv"))

fig, ax = plt.subplots(figsize=(10, 5))
line_e, = ax.plot([], [], color='blue', label='Electric Field (E)')
line_h, = ax.plot([], [], color='red', label='Magnetic Field (H)')

ax.set_xlim(0, 10000)  # will auto-adjust later
ax.set_ylim(-1, 1)
ax.set_xlabel('Cell index')
ax.set_ylabel('Field amplitude')
ax.legend()
ax.grid(True)

def init():
    line_e.set_data([], [])
    line_h.set_data([], [])
    return line_e, line_h

def animate(file):
    data = np.loadtxt(file, delimiter=",", skiprows=1, dtype=str)
    values_e = data[data[:,0] == "E", 1].astype(float)
    values_h = data[data[:,0] == "H", 1].astype(float)

    x_e = np.arange(len(values_e))
    x_h = np.arange(len(values_h))

    line_e.set_data(x_e, values_e)
    line_h.set_data(x_h, values_h * 100)
    return line_e, line_h

ani = animation.FuncAnimation(
    fig, animate, frames=files,
    init_func=init, blit=False, interval=50, repeat=False
)

# Save as MP4
ani.save("wave_animation.mp4", fps=20, extra_args=['-vcodec', 'libx264'])

plt.show()
