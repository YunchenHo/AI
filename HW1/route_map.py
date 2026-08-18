import io
import math
import os
import urllib.request
from typing import Iterable, List, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pickle


def load_path_graph(path: Sequence[int], graph_file: str = 'graph.pkl') -> List[list]:
    with open(graph_file, 'rb') as f:
        graph = pickle.load(f)

    node_pairs = set(zip(path[:-1], path[1:]))
    reverse_pairs = set((v, u) for u, v in node_pairs)
    match_pairs = node_pairs | reverse_pairs

    lines = []
    for edge in graph:
        if (edge['u'], edge['v']) in match_pairs:
            lines.append(edge['geometry'])
    return lines


def save_route_map_png(
    path: Sequence[int],
    output_file: str,
    route_color: str = 'blue',
    graph_file: str = 'graph.pkl',
    zoom: int = 15,
) -> int:
    lines = load_path_graph(path, graph_file=graph_file)
    all_points = [point for line in lines for point in line]

    if not all_points:
        raise ValueError('No route geometry found from the given path.')

    lats = [point[0] for point in all_points]
    lons = [point[1] for point in all_points]

    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)

    lat_margin = max((max_lat - min_lat) * 0.15, 0.001)
    lon_margin = max((max_lon - min_lon) * 0.15, 0.001)
    min_lat -= lat_margin
    max_lat += lat_margin
    min_lon -= lon_margin
    max_lon += lon_margin

    n = 2 ** zoom

    def lon_to_xtile(lon: float) -> float:
        return (lon + 180.0) / 360.0 * n

    def lat_to_ytile(lat: float) -> float:
        lat_rad = math.radians(lat)
        return (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n

    def xtile_to_lon(x: float) -> float:
        return x / n * 360.0 - 180.0

    def ytile_to_lat(y: float) -> float:
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
        return math.degrees(lat_rad)

    x_min = int(math.floor(lon_to_xtile(min_lon)))
    x_max = int(math.floor(lon_to_xtile(max_lon)))
    y_min = int(math.floor(lat_to_ytile(max_lat)))
    y_max = int(math.floor(lat_to_ytile(min_lat)))

    tile_size = 256
    canvas = Image.new('RGB', ((x_max - x_min + 1) * tile_size, (y_max - y_min + 1) * tile_size))

    tile_templates = [
        'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        'https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
        'https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
    ]
    headers = {'User-Agent': 'HW1-Route-Renderer/1.0 (Report Map Generator)'}

    def fetch_tile(x: int, y: int) -> Image.Image:
        last_error = None
        for template in tile_templates:
            url = template.format(z=zoom, x=x, y=y)
            req = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    return Image.open(io.BytesIO(resp.read())).convert('RGB')
            except Exception as err:
                last_error = err
        raise last_error

    failed_tiles = 0
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            try:
                tile_img = fetch_tile(x, y)
                canvas.paste(tile_img, ((x - x_min) * tile_size, (y - y_min) * tile_size))
            except Exception:
                failed_tiles += 1

    lon_left = xtile_to_lon(x_min)
    lon_right = xtile_to_lon(x_max + 1)
    lat_top = ytile_to_lat(y_min)
    lat_bottom = ytile_to_lat(y_max + 1)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(np.asarray(canvas), extent=[lon_left, lon_right, lat_bottom, lat_top], origin='upper')

    for line in lines:
        route_lats = [point[0] for point in line]
        route_lons = [point[1] for point in line]
        ax.plot(route_lons, route_lats, color=route_color, linewidth=3)

    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)
    ax.axis('off')

    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    fig.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    return failed_tiles
