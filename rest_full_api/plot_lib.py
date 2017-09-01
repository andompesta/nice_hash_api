from matplotlib import pyplot as plt

def plot_global_current_state(history_states, fild="price", color="black"):
    plt.style.use('ggplot')
    history_states[fild].plot()
