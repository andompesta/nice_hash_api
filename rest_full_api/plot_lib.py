from matplotlib import pyplot as plt

def plot_global_current_state(history_states, fild="price", color="black"):
    plt.style.use('ggplot')

    y = []
    for timestamp in history_states:
        for stat in timestamp["stats"]:
            y.append(float(stat[fild]))

    plt.plot(range(len(y)), y, c=color, alpha=0.8)
    plt.show(block=True)