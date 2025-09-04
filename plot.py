import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import glob

# Must match Rust constants
N = 10000
frame_size = N*8 + (N-1)*8  # bytes per file

# Get all bin files, sort by timestep number
files = sorted(glob.glob("data/frame_*.bin"))

fig, ax = plt.subplots(figsize=(10, 5))
line_e, = ax.plot([], [], color='blue', label='Electric Field (E)')
line_h, = ax.plot([], [], color='red', label='Magnetic Field (H)')

ax.set_xlim(0, N)
ax.set_ylim(-1, 1)
ax.set_xlabel('Cell index')
ax.set_ylabel('Field amplitude')
ax.legend()
ax.grid(True)

def init():
    line_e.set_data([], [])
    line_h.set_data([], [])
    return line_e, line_h

def read_bin_file(filename):
    """Read a single frame bin file (ex, hy)."""
    with open(filename, "rb") as f:
        buf = f.read()
        if len(buf) < frame_size:
            raise ValueError(f"Incomplete frame in {filename}")
        offset = 0
        ex = np.frombuffer(buf, dtype="<f8", count=N, offset=offset).copy()
        offset += N * 8
        hy = np.frombuffer(buf, dtype="<f8", count=N-1, offset=offset).copy()
    return ex, hy

def animate(file):
    ex, hy = read_bin_file(file)

    x_e = np.arange(len(ex))
    x_h = np.arange(len(hy))

    line_e.set_data(x_e, ex)
    line_h.set_data(x_h, hy * 100)  # keep scaling factor
    return line_e, line_h

ani = animation.FuncAnimation(
    fig, animate, frames=files,
    init_func=init, blit=False, interval=50, repeat=False
)

# Save as MP4
ani.save("wave_animation.mp4", fps=20, extra_args=['-vcodec', 'libx264'])

plt.show()
