import math
import timeit
import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import sequential_worker as sw
import parallel_worker as pw
import gpu_worker as gw


class MetricsHelper:
    def __init__(self, worker, difficulty, title):
        self.func = create_closure(worker, difficulty)
        self.props = worker.INFOS
        self.difficulty = difficulty
        self.title = title


def sequential_cases(title):
    cases = []
    cases.append(MetricsHelper(sw, 2, title))
    cases.append(MetricsHelper(sw, 3, title))
    cases.append(MetricsHelper(sw, 4, title))
    cases.append(MetricsHelper(sw, 5, title))
    return cases


def parallel_cases(title):
    cases = []
    cases.append(MetricsHelper(pw, 2, title))
    cases.append(MetricsHelper(pw, 3, title))
    cases.append(MetricsHelper(pw, 4, title))
    cases.append(MetricsHelper(pw, 5, title))
    cases.append(MetricsHelper(pw, 6, title))

    return cases


def gpu_cases(title):
    cases = []
    cases.append(MetricsHelper(gw, 1, title))
    cases.append(MetricsHelper(gw, 2, title))
    cases.append(MetricsHelper(gw, 3, title))
    return cases


def hashes_per_second_cases():
    cases = []
    cases.append(MetricsHelper(sw, 6, ""))
    cases.append(MetricsHelper(pw, 6, ""))
    cases.append(MetricsHelper(gw, 3, ""))
    return cases


def create_closure(algo, difficulty):
    hashGuessed = 0

    def closure():
        return algo.work(difficulty)
    return closure


def analyse_algorithm(metricHelper):
    times = timeit.repeat(metricHelper.func, number=1, repeat=5)
    return times


def hashesMetrics(case):
    total = []
    for i in range(1):
        total.append(case.func() // 60)
    return total


def init_plots(algorithms):
    # Configure plotting
    plt.tight_layout()
    fig_correct, plot_correct = plt.subplots()

    plot_correct.set_title(algorithms[0].title)

    handles = []
    for algorithm in algorithms:
        handles.append(patches.Patch(
            color=algorithm.props[1], label=algorithm.props[0]))

    handles.append(patches.Patch(color='white', label='x = Difficulty'))
    handles_correct = handles
    handles_correct.append(patches.Patch(
        color='white', alpha=0, label='y = Time(s) for 10 blocks'))

    plot_correct.legend(loc='upper left', title='Legend',
                        handles=handles_correct, fontsize='x-small')

    plot_correct.set_xlabel("x")
    plot_correct.set_ylabel("y")
    return fig_correct, plot_correct


if __name__ == "__main__":
    dot_size = 20.0
    seq_cases = sequential_cases("Sequential Time Analysis")
    par_cases = parallel_cases("Parallel Time Analysis")
    g_cases = gpu_cases("GPU Time Analysis")
    fig_global, plot_global = init_plots(
        [seq_cases[0], par_cases[0], g_cases[0]])
    plot_global.set_title("Average Time per Worker")
    # Sequential
    fig_seq, plot_seq = init_plots([seq_cases[0]])
    for i, c in enumerate(seq_cases):
        times = analyse_algorithm(c)
        if i % 2 == 0:
            avg_time = sum(times) // len(times)
            plot_global.scatter(c.difficulty, avg_time,
                                color=c.props[1], alpha=0.5, s=dot_size)
        plot_seq.scatter(
            [c.difficulty for i in range(len(times))], times, color=c.props[1], alpha=0.5, s=dot_size)
        plot_seq.plot()
    fig_seq.savefig(seq_cases[0].title, dpi=300, bbox_inches='tight')
    # parallel
    fig_par, plot_par = init_plots([par_cases[0]])
    for i, c in enumerate(par_cases):
        times = analyse_algorithm(c)
        if i % 2 == 0:
            avg_time = sum(times) // len(times)
            plot_global.scatter(c.difficulty, avg_time,
                                color=c.props[1], alpha=0.5, s=dot_size)

        plot_par.scatter(
            [c.difficulty for i in range(len(times))], times, color=c.props[1], alpha=0.5, s=dot_size)
        plot_par.plot()
    fig_par.savefig(par_cases[0].title, dpi=300, bbox_inches='tight')

    # GPU
    fig_gpu, plot_gpu = init_plots([g_cases[0]])
    for i, c in enumerate(g_cases):
        times = analyse_algorithm(c)
        avg_time = sum(times) // len(times)
        plot_global.scatter(c.difficulty * 2, avg_time,
                            color=c.props[1], alpha=0.5, s=dot_size)
        plot_gpu.scatter(
            [c.difficulty * 2 for i in range(len(times))], times, color=c.props[1], alpha=0.5, s=dot_size)
        plot_gpu.plot()
    fig_gpu.savefig(g_cases[0].title, dpi=300, bbox_inches='tight')

    plot_global.plot()
    fig_global.savefig("Global Time Analysis", dpi=300, bbox_inches='tight')

    """
    hash_cases = hashes_per_second_cases()

    fig_speed, plot_speed = init_plots(
        hash_cases)
    plot_speed.set_title("Hashing Speed Analysis")
    for i, c in enumerate(hash_cases):
        speed = hashesMetrics(c)

        plot_speed.scatter(
            [i for i in range(len(speed))], speed, color=c.props[1], alpha=0.85, s=dot_size)

    plot_speed.plot()
    fig_speed.savefig("Hashing Speed Analysis", dpi=300, bbox_inches='tight')
"""
