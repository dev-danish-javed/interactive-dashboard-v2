# chart_helper.py
import io
import base64
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------
# Internal utility: convert fig → HTML <img>
# ----------------------------------------
def _fig_to_html(fig):
    """Convert Matplotlib figure to base64 HTML <img> tag."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f'<img src="data:image/png;base64,{encoded}" />'


# ----------------------------------------
# Chart Functions
# ----------------------------------------

def bar_chart(data, labels, title="Bar Chart", xlabel="", ylabel=""):
    fig, ax = plt.subplots()
    ax.bar(labels, data, color='royalblue')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return _fig_to_html(fig)


def grouped_bar_chart(data_groups, labels, group_names, title="Grouped Bar Chart", xlabel="", ylabel=""):
    fig, ax = plt.subplots()
    x = np.arange(len(labels))
    width = 0.8 / len(data_groups)
    for i, (data, group) in enumerate(zip(data_groups, group_names)):
        ax.bar(x + i * width, data, width, label=group)
    ax.set_xticks(x + width * (len(data_groups) - 1) / 2)
    ax.set_xticklabels(labels)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    return _fig_to_html(fig)


def line_chart(x, y, title="Line Chart", xlabel="", ylabel=""):
    fig, ax = plt.subplots()
    ax.plot(x, y, marker='o', color='steelblue')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return _fig_to_html(fig)


def multi_line_chart(x, y_series, labels, title="Multi-Line Chart", xlabel="", ylabel=""):
    fig, ax = plt.subplots()
    for y, label in zip(y_series, labels):
        ax.plot(x, y, marker='o', label=label)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    return _fig_to_html(fig)


def area_chart(x, y, title="Area Chart", xlabel="", ylabel=""):
    fig, ax = plt.subplots()
    ax.fill_between(x, y, color='lightcoral', alpha=0.6)
    ax.plot(x, y, color='red')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return _fig_to_html(fig)


def pie_chart(data, labels, title="Pie Chart"):
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title(title)
    ax.axis('equal')
    return _fig_to_html(fig)


def donut_chart(data, labels, title="Donut Chart"):
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        data, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4)
    )
    ax.set_title(title)
    ax.axis('equal')
    return _fig_to_html(fig)


def scatter_chart(x, y, title="Scatter Plot", xlabel="", ylabel=""):
    fig, ax = plt.subplots()
    ax.scatter(x, y, color='seagreen', alpha=0.7)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return _fig_to_html(fig)


def bubble_chart(x, y, sizes, title="Bubble Chart", xlabel="", ylabel=""):
    fig, ax = plt.subplots()
    ax.scatter(x, y, s=sizes, alpha=0.5, color='skyblue', edgecolors='gray')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return _fig_to_html(fig)


def histogram(data, bins=10, title="Histogram", xlabel="", ylabel="Frequency"):
    fig, ax = plt.subplots()
    ax.hist(data, bins=bins, color='salmon', edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return _fig_to_html(fig)


def box_plot(data, labels=None, title="Box Plot", ylabel=""):
    fig, ax = plt.subplots()
    ax.boxplot(data, labels=labels, patch_artist=True)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    return _fig_to_html(fig)


def violin_plot(data, labels=None, title="Violin Plot", ylabel=""):
    fig, ax = plt.subplots()
    ax.violinplot(data, showmeans=True)
    if labels:
        ax.set_xticks(np.arange(1, len(labels) + 1))
        ax.set_xticklabels(labels)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    return _fig_to_html(fig)


def heatmap(matrix, x_labels, y_labels, title="Heatmap"):
    fig, ax = plt.subplots()
    cax = ax.imshow(matrix, cmap='coolwarm', aspect='auto')
    fig.colorbar(cax)
    ax.set_xticks(np.arange(len(x_labels)))
    ax.set_yticks(np.arange(len(y_labels)))
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)
    ax.set_title(title)
    return _fig_to_html(fig)


def radar_chart(categories, values, title="Radar Chart"):
    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    categories += [categories[0]]
    values += [values[0]]
    angles = np.linspace(0, 2 * np.pi, len(categories))
    ax.plot(angles, values, color='dodgerblue', linewidth=2)
    ax.fill(angles, values, color='dodgerblue', alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories[:-1])
    ax.set_title(title)
    return _fig_to_html(fig)


def waterfall_chart(values, labels, title="Waterfall Chart"):
    fig, ax = plt.subplots()
    running_total = np.cumsum(values)
    starts = np.concatenate(([0], running_total[:-1]))
    colors = ['green' if v >= 0 else 'red' for v in values]
    ax.bar(labels, values, bottom=starts, color=colors)
    ax.plot(range(len(running_total)), running_total, color='black', marker='o')
    ax.set_title(title)
    ax.set_ylabel("Value")
    return _fig_to_html(fig)
