# See https://stackoverflow.com/a/19521297/3187068
import matplotlib
matplotlib.use('pdf')

import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import textwrap


def wrapped(s: str, width: int = 60) -> str:
    return '\n'.join(textwrap.wrap(s, width))


def plot(df: pd.DataFrame,
         ax: plt.Axes,
         algorithm: str,
         column: str,
         pretty_column: str) -> None:
    grouped = df.groupby('leader.thrifty_system')
    for (name, group) in grouped:
        stats = group.groupby('num_clients')[column].agg([np.mean, np.std])
        mean = stats['mean']
        std = stats['std'].fillna(0)
        line = ax.plot(mean, '.-', label=name)[0]
        color = line.get_color()
        ax.fill_between(stats.index, mean - std, mean + std,
                        color=color, alpha=0.25)

    ax.set_title(pretty_column)
    ax.set_xlabel('Number of clients')
    ax.set_ylabel(pretty_column)
    ax.grid()
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


def main(args) -> None:
    df = pd.read_csv(args.results)
    df['num_clients'] = df['num_client_procs'] * df['num_clients_per_proc']

    # See [1] for figure size defaults. We add an extra plot at the bottom for
    # a textual note.
    #
    # [1]: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.figure.html
    num_plots = 4
    fig, ax = plt.subplots(num_plots, 1, figsize=(1.5 * 6.4, num_plots * 4.8))

    plot(df[df['round_system_type'] == 'CLASSIC_ROUND_ROBIN'], ax[0],
         'MultiPaxos', 'median_latency_ms', 'Median latency')
    plot(df[df['round_system_type'] == 'CLASSIC_ROUND_ROBIN'], ax[1],
         'MultiPaxos', 'p95_1_second_throughput',
         'P95 throughput (1 second windows)')
    plot(df[df['round_system_type'] == 'MIXED_ROUND_ROBIN'], ax[2],
         'Fast MultiPaxos', 'median_latency_ms', 'Median latency')
    plot(df[df['round_system_type'] == 'MIXED_ROUND_ROBIN'], ax[3],
         'Fast MultiPaxos', 'p95_1_second_throughput',
         'P95 throughput (1 second windows)')

    fig.set_tight_layout(True)
    fig.savefig(args.output)
    print(f'Wrote plot to {args.output}.')


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'results',
        type=str,
        help='results.csv file'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='fastmultipaxos_thrifty.pdf',
        help='Output filename'
    )
    return parser


if __name__ == '__main__':
    main(get_parser().parse_args())
