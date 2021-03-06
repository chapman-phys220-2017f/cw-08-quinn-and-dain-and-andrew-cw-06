#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML

"""Rudimentary animation library

This simple library is a simple wrapper around the matplotlib animation
feature, assuming a one dimensional domain and one dimensional range.
It automates the plotting details given just a generator for updated ranges.
"""

def plot_anim(frame_gen, xlim=(0,5), ylim=(-10,10), n=1000, delay=20, max_frames=1000,
                   title=None, xlabel=None, ylabel=None, gif=False):
    """Produce an animation from a frame-generating function. 
    Works in two modes:
      - Return a Jupyter HTML5 wrapper around a rendered mp4 video of the animation
      - Create an animated gif file of the animation
    The first mode is default and recommended for in-notebook rendering.
    
    Args:
      frame_gen : Generator that takes domain array of points and yields
                  successive range arrays of points to plot as frames.
                  The frames will continue until the generator is exhausted.
      xlim = (xmin,xmax) : Horizontal plot range [default (0,5)]
      ylim = (ymin,ymax) : Vertical plot range   [default (-10,10)]
      n : Number of domain points
      delay : number of ms between frames
      max_frames : maximum number of saved frame [default 1000]
      title : plot title (optional)
      xlabel : plot x axis label (optional)
      ylabel : plot y axis label (optional)
      gif : Boolean, if true render gif file instead of outputting HTML5 (default false)
    
    Returns:
      HTML object containing mp4 video of animation (when gif false)
    
    Effects:
      Saves a gif file containing the animation (when gif true)
    """
    # Define domain points that remain fixed
    x = np.linspace(xlim[0],xlim[1],n)
    g = frame_gen(x)
    
    # Create empty plot set to desired fixed zoom
    fig, ax = plt.subplots()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    if title:  plt.title(title)
    if xlabel: plt.xlabel(xlabel)
    if ylabel: plt.ylabel(ylabel)
    
    # Draw an empty line and save the handle to update later
    line, = ax.plot([], [], lw=2)
    
    # Define how to generate a blank frame
    def init_frame():
        line.set_data([],[])
        return (line,)
    
    # Define how to update a frame from a range input
    def animate(y):
        line.set_data(x,y)
        return (line,)
    
    # Define animation object using frame generator
    # Use blit to redraw only the changes that were made
    anim = animation.FuncAnimation(fig, animate, init_func=init_frame, save_count=max_frames,
                                   frames=g, interval=delay, blit=True)
    
    # Tidy up stray plot within the notebook itself
    plt.close()
    
    if gif:
        # Render animation as animated gif file
        anim.save(frame_gen.__name__+'.gif', writer='imagemagick')
    else:
        # Make sure that animation renders to HTML5 by default
        rc('animation', html='html5')
        # Convert animation to HTML5 and return
        return HTML(anim.to_html5_video())
