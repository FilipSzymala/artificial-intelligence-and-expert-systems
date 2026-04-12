import matplotlib.pyplot as plt
import pandas as pd
import os


def load_session_data(session_path):
    results = []
    if not os.path.exists(session_path):
        print(f"Error: Catalogue {session_path} does not exist.")
        return pd.DataFrame()

    for strat_dir in os.listdir(session_path):
        dir_path = os.path.join(session_path, strat_dir)
        if not os.path.isdir(dir_path):
            continue

        parts = strat_dir.split('_')
        strategy = parts[0]
        param = parts[1]

        for file in os.listdir(dir_path):
            if file.endswith('_sol_details.txt'):
                depth = int(file.split('_')[1])

                with open(os.path.join(dir_path, file), 'r') as f:
                    lines = [line.strip() for line in f.readlines()]
                    if len(lines) >= 4:
                        results.append({
                            'Depth': depth,
                            'Strategy': strategy,
                            'Param': param,
                            'SolLen': int(lines[0]),
                            'Visited': int(lines[1]),
                            'Processed': int(lines[2]),
                            'MaxDepth': int(lines[3])
                        })
    return pd.DataFrame(results)


def plot_criterion(df, column, title, filename):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Remove no solution records for avg calculations
    plot_df = df.copy()
    if column == 'SolLen':
        plot_df = plot_df[plot_df[column] != -1]

    # Overall
    ax = axes[0, 0]
    summary = plot_df.groupby(['Depth', 'Strategy'])[column].mean().unstack()
    if not summary.empty:
        summary.rename(columns={'bfs': 'BFS', 'dfs': 'DFS', 'astr': 'A*'}, inplace=True)
        cols = [c for c in ['BFS', 'DFS', 'A*'] if c in summary.columns]
        summary[cols].plot(kind='bar', ax=ax)

    # Log scale to make data more visible (without it A* and BFS data hides cuz DFS results are too big)
    if column in ['Visited', 'Processed']:
        ax.set_yscale('log')

    ax.set_title('Ogółem')
    ax.set_ylabel('Kryterium')
    ax.set_xlabel('')
    ax.tick_params(axis='x', rotation=0)

    # Astr (A*)
    ax = axes[0, 1]
    astr = plot_df[plot_df['Strategy'] == 'astr']
    if not astr.empty:
        astr_summary = astr.groupby(['Depth', 'Param'])[column].mean().unstack()
        astr_summary.rename(columns={'hamm': 'Hamming', 'manh': 'Manhattan'}, inplace=True)
        astr_summary.plot(kind='bar', ax=ax)
    ax.set_title('A*')
    ax.set_xlabel('')
    ax.tick_params(axis='x', rotation=0)

    # BFS
    ax = axes[1, 0]
    bfs = plot_df[plot_df['Strategy'] == 'bfs']
    if not bfs.empty:
        bfs_summary = bfs.groupby(['Depth', 'Param'])[column].mean().unstack()
        bfs_summary.columns = [c.upper() for c in bfs_summary.columns]
        bfs_summary.plot(kind='bar', ax=ax)
    ax.set_title('BFS')
    ax.set_ylabel('Kryterium')
    ax.set_xlabel('Głębokość')
    ax.tick_params(axis='x', rotation=0)

    # DFS
    ax = axes[1, 1]
    dfs = plot_df[plot_df['Strategy'] == 'dfs']
    # Log scale to make data more visible
    if column in ['Visited', 'Processed']:
        ax.set_yscale('log')
    if not dfs.empty:
        dfs_summary = dfs.groupby(['Depth', 'Param'])[column].mean().unstack()
        dfs_summary.columns = [c.upper() for c in dfs_summary.columns]
        dfs_summary.plot(kind='bar', ax=ax)
    ax.set_title('DFS')
    ax.set_xlabel('Głębokość')
    ax.tick_params(axis='x', rotation=0)

    # Hide legend labels for consistency with report requirements in wikamp exercise
    for a in axes.flat:
        legend = a.get_legend()
        if legend:
            legend.set_title(None)

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()