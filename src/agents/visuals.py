import os
from src.utils.io import ensure_dir
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import imageio

def render_static_chart(save_path):
    ensure_dir(os.path.dirname(save_path))
    x = np.linspace(0,10,200)
    y = np.sin(x)
    plt.figure(figsize=(8,4))
    plt.plot(x,y)
    plt.title("Sample Sensor Output")
    plt.savefig(save_path, dpi=150)
    plt.close()
    return save_path

def render_animation(mp4_path, gif_path):
    ensure_dir(os.path.dirname(mp4_path))
    x = np.linspace(0,2*np.pi,200)
    fig, ax = plt.subplots(figsize=(6,3))
    line, = ax.plot([], [], lw=2)
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1.2, 1.2)
    def init():
        line.set_data([], [])
        return (line,)
    def update(i):
        line.set_data(x, np.sin(x + i/10.0))
        return (line,)
    anim = FuncAnimation(fig, update, frames=80, init_func=init, blit=True)
    # Try to save as MP4 if ffmpeg is available
    try:
        # Check if we can write mp4
        if imageio.plugins.ffmpeg.get_exe():
            anim.save(mp4_path, fps=20, dpi=120)
        else:
            print("FFmpeg not found via imageio, skipping MP4.")
            mp4_path = None
    except Exception as e:
        print(f"Warning: Could not save MP4 (likely missing ffmpeg): {e}")
        mp4_path = None
    # Convert to GIF
    # If MP4 exists, we can convert it. If not, we must save directly as GIF using Pillow.
    if mp4_path and os.path.exists(mp4_path):
        try:
            reader = imageio.get_reader(mp4_path)
            frames = [frame for frame in reader]
            imageio.mimsave(gif_path, frames, fps=12)
        except Exception as e:
            print(f"Failed to convert MP4 to GIF: {e}")
    else:
        # Fallback: Save directly as GIF using Matplotlib (Pillow writer)
        print("Saving directly to GIF...")
        anim.save(gif_path, writer='pillow', fps=12)

    return mp4_path, gif_path