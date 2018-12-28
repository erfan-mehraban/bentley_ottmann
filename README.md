# Bentley-Ottmann implementation

This is a implementation in bentley-ottmannalgorithm implementation in general position by python and simple visualization of its export.

For more information about this algorithm check [wikipedia page](https://en.wikipedia.org/wiki/Bentley%E2%80%93Ottmann_algorithm).

## Install Dependencies

```bash
pip3 install -r requirements
```

## Run

```bash
python3 composer.py
```

## Design

* `bst.py` contains balanced binary search tree implementation which edited duo to algorithm needs.
* `models.py` contains `Segment` and `Point` models.
* `visualizer.py` have some functions to draw easily with `matplotlib`
* `bentley_ottmann.py` contains implementation of algorithm
* `composer.py` has main function and generate data and run algorithm then visualize it.

## Note

dont forget theese 3 assumprions:

* No two line segment endpoints or crossings have the same x-coordinate
* No line segment endpoint lies upon another line segment
* No three line segments intersect at a single point.

Any crash may occure if one of obove doesnt sattisfied.

## Built With

* Python3
* [Shapely](https://pypi.org/project/Shapely/)
* [matplotlib](https://matplotlib.org/)
* [bst from pgrafov](https://github.com/pgrafov/python-avl-tree/blob/master/pyavltree.py)
