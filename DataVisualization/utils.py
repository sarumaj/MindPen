import matplotlib.pyplot as plt
import base64
from io import BytesIO


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode("utf-8")
    buffer.close()
    return graph


def get_plot(x, y):
    plt.style.use('_mpl-gallery')
    plt.switch_backend("AGG")
    plt.figure(figsize=(10, 5))
    plt.title("Mood Plot")
    plt.plot(x, y, "b", linewidth=2.0, marker="o", ms=10)
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Mood")
    plt.tight_layout()
    plt.legend(["Line"])
    graph = get_graph()
    return graph
