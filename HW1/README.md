# **Spring 2026 Introduction to Artificial Intelligence**

## **Homework 1: Route Finding**

- Assigned: 2026/3/13 (Fri.)  
- Due date: 2026/3/27 (Fri.) 23:59  
- Oral test sign-up form open period: 2026/3/24 (Tue.) 14:20 \~ 2026/3/27 (Fri.) 23:59  
- Oral test: 3/30 (Mon.) 16:30\~18:30 @ EC022

## **Introduction**

When you are invited to a new restaurant located somewhere you’re not familiar with, what would you do? Map applications have the feature that helps you plan a path from home to the restaurant. For example, Google Maps automatically figures out feasible routes and provides the corresponding instructions to reach the destination given your current position.

The application mentioned above is a **navigation system**. A navigation system involves three steps. First, you have to construct a map (also called **mapping**). Do you know how to build one (e.g., Hsinchu City)? Second, given a map, you have to know your current position. This step is called **localization.** Do you know how Google Maps locates your position? Third, a **route finding algorithm** that takes as input a current position and destination set by you is utilized to identify feasible routes. In this homework, we focus on the third part. Before reading the following description, how would you tackle the route finding problem?

The goal of this programming assignment is to implement a variety of **search algorithms**. You are given real map data of Hsinchu City exported from OpenStreetMap ([https://www.openstreetmap.org/](https://www.openstreetmap.org/)). Given a starting point and destination, different search algorithms find you different routes. You will see the difference shown on an actual map.

## **Notes:**

* Please read the **Appendix** carefully.  
* Only the [standard Python library](https://docs.python.org/3/library/) is allowed in **algorithm files** (`bfs.py`, `dfs.py`, `ucs.py`, `astar.py`, `astar_time.py`).  
* Visualization helpers for report screenshots (e.g., `route_map.py` and `generate_report_maps.py`) are **not** part of algorithm grading and may use extra packages listed in Appendix.  
* You will implement each search algorithm in the corresponding Python script (e.g., bfs.py).
* You may add your own local helper module(s) if needed, but they must use only the standard Python library and must be included in your submission zip.
* If your **submitted code** imports packages outside the standard Python library, the homework will receive **0 points** according to the grading policy. The provided visualization scripts in this repository are TA-supplied utilities and are not part of algorithm grading.

## **Environment**

- We recommend using `uv` to manage the Python environment for this homework.
- Recommended Python version: `3.11.x`
- The project is pinned with `.python-version` so that you can use a consistent Python minor version locally.

## **Evaluation and Final Score**

This homework has three grading components:

1. **Implementation** (50%)  
2. **Report** (30%)  
3. **Oral test** (20%)

Final score is computed as:

`final score = Implementation + Report + Oral test`

## **Implementation (50%)**

All search functions share the same input pattern:

- Parameters:  
  - `start`: integer, the starting node ID  
  - `end`: integer, the destination node ID  
- Common returns:  
  - `path`: list of integer, the path found from `start` to `end`  
  - `num_visited`: integer, the number of visited nodes during search

The required function names and algorithm-specific outputs are:

| Part | Function | Goal | Main output |
| :---- | :---- | :---- | :---- |
| Part 1 | `bfs` | Find a path with breadth-first search | `dist`: float, total path distance in meters |
| Part 2 | `dfs` | Find a path with depth-first search | `dist`: float, total path distance in meters |
| Part 3 | `ucs` | Find the shortest path with uniform cost search | `dist`: float, total path distance in meters |
| Part 4 | `astar` | Find the shortest path with A\* search | `dist`: float, total path distance in meters |
| Part 5 | `astar_time` | Find the fastest path with A\* and a time-based heuristic | `time`: float, total travel time in seconds |

### Exact interface requirements

All five functions must return a tuple in the form:

```python
(path, cost_or_time, num_visited)
```

with the following requirements:

- `path` must be a `list[int]`.
- `path` must include both endpoints, so the first element must be `start` and the last element must be `end`.
- `cost_or_time` must be a number (`int` or `float`).
- `num_visited` must be an `int`.
- For consistency in your report, we recommend counting `num_visited` as the number of nodes **popped from the frontier for expansion**, including the start node.
- If `start == end`, return `([start], 0.0, 1)`.
- The released and hidden grading cases always have at least one legal path, so you do not need special error handling for unreachable grading cases. If you want to handle unreachable inputs in your own testing, returning `([], float("inf"), num_visited)` is acceptable.

### Graph and cost model

- Treat each row in `edges.csv` as a **directed edge** from `start` to `end`.
- Do **not** add a reverse edge unless the reverse row also appears in `edges.csv`.
- For Parts 1 to 4, edge cost is `distance` in meters.
- For Part 5, edge cost is travel time computed from:

```python
time_seconds = distance_meters / (speed_limit_kmh * 1000 / 3600)
```

- In Parts 1 and 2, the returned `dist` is still the sum of physical edge distances along the returned path, even though BFS/DFS do not optimize distance.
- If multiple legal answers exist, any answer produced by a correct implementation is accepted. For reproducibility, we recommend expanding neighbors in the order they appear in `edges.csv`.

The released public test cases use the following start and end nodes:

| Case | Starting node | End node |
| :---- | :---- | :---- |
| 1 | near National Yang Ming Chiao Tung University (ID: `2773409914`) | near Big City Shopping Mall (ID: `1079387396`) |
| 2 | near Hsinchu Zoo (ID: `426882161`) | near COSTCO Hsinchu Store (ID: `1737223506`) |
| 3 | near National Experimental High School At Hsinchu Science Park (ID: `1718165260`) | near Nanliao Fishing Port (ID: `8513026827`) |

### Part 1: Breadth-first Search (10%)

* Implement a breadth-first search function to find a path from a starting node to an end node.  
* Implement the function `bfs(start, end)`.  
* Treat every edge as unit cost for the search order, and report the physical path distance in meters.
* Return `(path, dist, num_visited)`.

### Part 2: Depth-first Search (10%)

* Implement a depth-first search function to find a path from a starting node to an end node. You can implement depth-first search in a recursive method or a non-recursive method.  
* Implement the function `dfs(start, end)`.  
* Report the physical path distance in meters for the path your DFS returns.
* Return `(path, dist, num_visited)`.

### Part 3: Uniform Cost Search (10%)

* Implement a uniform cost search function to find the shortest path from a starting node to an end node.  
* Implement the function `ucs(start, end)`.  
* Return `(path, dist, num_visited)`.

### Part 4: A\* Search (10%)

* Implement a A\* search function to find the shortest path from a starting node to an end node.  
* Use the straight-line distance from `heuristic.csv` as the heuristic value `h(n)`.
* Implement the function `astar(start, end)`.  
* Return `(path, dist, num_visited)`.

### Part 5: Search with a different heuristic (10%)

* Implement an A\* search function to find the **fastest** path from a starting node to an end node, where edge cost is travel time rather than distance.  
* For this part, assume that the actual driving speed on each road segment is exactly the speed limit in `edges.csv`.  
* You must use an **admissible** heuristic for travel time. The reference heuristic used in the TA testing code is:

```python
h_time(n) = straight_line_distance_to_goal(n) / max_adjacent_speed_of_node_n
```

  where the speed term is measured in `m/s`.
* Based on current TA observations, the following designs are considered workable:
  * `straight_line_distance_to_goal / very_high_speed_limit`
  * `straight_line_distance_to_goal / global_max_speed_limit`
* The following designs may be workable, but are not guaranteed:
  * `straight_line_distance_to_goal / speed_limit_of_previous_edge`
  * `straight_line_distance_to_goal / average_speed_limit_of_adjacent_edges`
* The following designs are **not** admissible for grading:
  * `straight_line_distance_to_goal / average_speed_from_start_to_current_node`
  * `straight_line_distance_to_goal / global_average_speed_limit`
* Implement the function `astar_time(start, end)`.  
* Return `(path, time, num_visited)`.  
* Test your implementation with the three cases listed above.  
* Compare the results with the results obtained in Part 4 for the same start/end pairs.  
* In the grading environment, your implementation for this part must finish the required test cases within **30 seconds**. Otherwise, this part will receive 0 points.

## **Grading Policy (Part 1 \~ Part 5\)**

* Total implementation score is **50 points**.  
* For each part, **50% comes from public tests** (the 3 published test cases), and **50% comes from private tests**.  
* Private tests are selected and run by TAs.  
* All test cases (public/private) are chosen to ensure there is at least one legal road/path between the start and end nodes.  
* If your submitted code uses packages outside the standard Python library, the homework will receive **0 points**.
* Scoring is **block-level all-or-nothing** for each part:  
  * Public block: full public points only if all public checks pass, otherwise 0\.  
  * Private block: full private points only if all private checks pass, otherwise 0\.

| Part | Public | Private | Total |
| :---- | :---- | :---- | :---- |
| Part 1 (BFS) | 5 | 5 | 10 |
| Part 2 (DFS) | 5 | 5 | 10 |
| Part 3 (UCS) | 5 | 5 | 10 |
| Part 4 (A\*) | 5 | 5 | 10 |
| Part 5 (A\* Time) | 5 | 5 | 10 |

How to run the released local grader:

```shell
uv run grader/grade.py
```

Notes:

- This command runs the released public checks in your local environment.
- Private tests are not included in the release, and they will be run by TAs in the grading environment after submission.
- The released local grader is intentionally a **public-only grader**. You should treat its score as a public subtotal rather than your final implementation score.
- The released local grader is a convenience tool, not the full specification. Your implementation must still follow the interface and behavior rules described in this README.

## **Report (30%)**

* A report is required.  
* The report should be written in **English**.  
* Please save the report as a `REPORT.md`.  
* Answer the questions in the `REPORT.md` template.
* Put all images referenced by `REPORT.md` in the `result/` folder.
* In Part I, provide **code screenshots** and explain the logic of each algorithm.
* In Part II, upload the final map results for BFS/DFS/UCS/A\*/A\* Time in Question 1, fill in a comparison table for BFS/DFS/UCS/A\* in Question 2, and write a text comparison between A\* and A\* Time in Question 3.

## **Academic Integrity and AI Policy**

This course has a strict policy on AI-generated work for **all graded material**.

- Discussion with classmates is allowed, but you must cite your discussion partners and write your own code.
- Do **not** use ChatGPT, Copilot, or any other automatic code-generation tool to produce material that you submit for grading.
- Any code, report text, explanation, or other graded content you hand in must be solved and typed by **you**, the student.
- We will treat AI-generated submission content as **cheating**.
- Do **not** post solutions online or share them publicly. If you use GitHub while collaborating with an approved partner, keep the repository **private**.
- Assignments may be checked with plagiarism detection, including cross-class comparisons.
- Violations of the course policy may lead to **zero points, negative points, or an F in the course**.

## **Oral Test (20%)**

The oral test is used to verify that you implemented the homework yourself and understand your submission. Each student must sign up for a 4-minute oral test slot as part of completing this assignment.

The purpose of the oral test is to help prepare you for future technical interviews. During the oral test, you will be asked several questions related to your homework. If you completed the work yourself, you should be able to answer questions about your own implementation.

We take academic integrity very seriously. Submissions will undergo plagiarism checks both within and across classes taught by Prof. Yen and Prof. Wei. Our checking process also includes multiple variants of AI-generated code. These measures are intended to ensure fairness for students who complete their work without copying from peers or AI.

Oral test rules:

- Questions will be selected from a prepared question set that will not be announced in advance.  
- TAs will ask several questions during the 4-minute oral test.
- If a student cannot adequately explain their submission during the oral test, the course staff may initiate an authorship review, including possible misuse of AI tools, plagiarism, or other academic integrity violations.
- If a student receives 0 points on the oral test and the plagiarism review flags the submission, the course staff will conduct a closer review of the submitted work and may follow up with additional investigation regarding the authenticity of the submission.
- If the instructor and TAs conclude that the submission violates the course policy, the assignment may receive **0 or negative points**.

Oral test sign-up form:  
[https://docs.google.com/spreadsheets/d/1DmCvFY3pKuad9fpqTI-4PiseoscXmCdUof7B1VIrxKk/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1DmCvFY3pKuad9fpqTI-4PiseoscXmCdUof7B1VIrxKk/edit?usp=sharing)

If a student cannot attend the oral test:

- Unexcused absence: the oral-test component score is **0**.  
- Excused absence (with prior notice and valid proof): one make-up oral test may be arranged with prior notice email.  
- Emergency cases must contact TAs within 48 hours with supporting documents.  
- Missing the approved make-up oral test is treated as an unexcused absence and receives **0** for the oral-test component.

## **QA Page**

If you have any questions about this homework, please ask them on the following Notion page. We will answer them as soon as possible. Additionally, we encourage you to answer other students' questions if you can.

[https://www.notion.so/HW1-QA-space-314bb214a6aa8053911bec6bc8662cb0](https://www.notion.so/HW1-QA-space-314bb214a6aa8053911bec6bc8662cb0)

Reminder: We will **not** announce any updates to the E3 Platform on this Notion page, so please check it regularly.

You may email the TAs only if you have any questions that are not suitable for public discussion. Please send to `spring-intro-ai@googlegroups.com` with the subject line `[ClassID]_{StudentID}_HW1_{ShortDescriptionOfQuestion}`.

## **Submission**

Please compress your submission into `{STUDENT ID}_hw1.zip` (for example, `109123456_hw1.zip`) and **submit it to the E3 System.**

Your zip file should contain:

- `bfs.py`
- `dfs.py`
- `ucs.py`
- `astar.py`
- `astar_time.py`
- any optional helper module(s) that your five algorithm files import
- `REPORT.md`
- `result/` containing the images referenced by `REPORT.md`

Do **not** include the provided dataset files, grader files, virtual environment folders, or cache folders in your submission zip.

The file structure should look like:

```
{student_id}_hw1.zip
  ┣ bfs.py
  ┣ dfs.py
  ┣ ucs.py
  ┣ astar.py
  ┣ astar_time.py
  ┣ optional_helper.py
  ┣ REPORT.md
  ┗ result
    ┣ bfs_code.png
    ┣ dfs_code.png
    ┣ ucs_code.png
    ┣ astar_code.png
    ┣ astar_time_code.png
    ┣ bfs_map.png
    ┣ dfs_map.png
    ┣ ucs_map.png
    ┣ astar_map.png
    ┣ astar_time_map.png
    ┗ other-screenshots.png
```

Please make sure the image files referenced in `REPORT.md` are included in the zip file.

- Do **not** include folders such as `grader/`, `.venv/`, or `__pycache__/` in your submission zip.
- Wrong submission format leads to 0 point.
- Late submission leads to 0 point.

## **Appendix**

### **Released Files**

This release provides the following files and folders:

| File / Folder | Purpose |
| :---- | :---- |
| `README.md` | Homework specification, grading rules, submission format, and appendix notes. |
| `REPORT.md` | Report template that you should fill in and submit. |
| `bfs.py` | Starter code for Part 1. Implement `bfs(start, end)` here. |
| `dfs.py` | Starter code for Part 2. Implement `dfs(start, end)` here. |
| `ucs.py` | Starter code for Part 3. Implement `ucs(start, end)` here. |
| `astar.py` | Starter code for Part 4. Implement distance-based `astar(start, end)` here using `heuristic.csv`. |
| `astar_time.py` | Starter code for Part 5. Implement time-based `astar_time(start, end)` here. |
| `edges.csv` | Directed road-network data used by all search algorithms. Each row stores `start`, `end`, `distance`, and `speed limit`. |
| `heuristic.csv` | Straight-line-distance lookup table for A\* and A\* Time test destinations. |
| `graph.pkl` | Road geometry data used only for drawing route maps. It is not required for your search logic. |
| `route_map.py` | Visualization helper that turns a node path into a PNG route map. |
| `generate_report_maps.py` | Command-line helper that runs your algorithm(s) and generates report figures in `result/`. |
| `pyproject.toml` | Project metadata and dependency list for local development with `uv`. |
| `uv.lock` | Lock file for reproducible package installation with `uv`. |
| `.python-version` | Recommended local Python version for this homework. |
| `grader/` | Released local grader package. It includes only the public checks. |

Files inside `grader/`:

| File | Purpose |
| :---- | :---- |
| `grader/grade.py` | Entry point for the released local grader (`uv run grader/grade.py`). |
| `grader/spec.py` | Public grading specification, including released cases, scoring setup, and runtime limit. |
| `grader/scoring.py` | Shared grading logic that loads your functions and evaluates each part. |
| `grader/path_metrics.py` | Helper utilities for validating path legality, distance, and travel time from `edges.csv`. |
| `grader/README.md` | Short usage notes for the released grader. |
| `grader/__init__.py` | Makes `grader/` importable as a Python package. |

### **Setup**

Additional packages are required only for visualization/screenshot generation in the report. They are not required for algorithm grading.

**For local development:**  
We recommend using `uv` for dependency management in this project.  
This homework targets Python `3.11.x`. To use the recommended version with `uv`, run:

```shell
uv python pin 3.11
```

Check your Python version:

```shell
python3 --version
uv run python --version
```

Generate report maps from the command line:

```shell
uv run python generate_report_maps.py --help
uv run python generate_report_maps.py --start 2773409914 --end 1079387396
uv run python generate_report_maps.py --start 2773409914 --end 1079387396 --algorithm astar_time
```

This command generates the report figures in `result/`:
- `result/bfs_map.png`
- `result/dfs_map.png`
- `result/ucs_map.png`
- `result/astar_map.png`
- `result/astar_time_map.png`

**Check your submission locally:**

```shell
uv run grader/grade.py
```

This command runs the provided local grader so you can verify that your code can be imported and tested successfully before submission.

### **Data**

To formulate the route finding problem as a search problem, we leverage the state-based model and represent a map with intersections. In OpenStreetMap, each intersection is labeled with a unique ID. A road connects two nodes. All roads in North and East District, Hsinchu City are in edges.csv.

The CSV file stores the following information:

| column | detail |
| :---- | :---- |
| start | The ID of the starting node of a road. |
| end | The ID of the end node of a road. |
| distance | The length of a road. (Unit: meter) |
| speed limit | The speed limit of a road. (Unit: km/h) |

For A\*, we use straight-line distance as the heuristic function. Therefore, we provide the information in heuristic.csv.  
The CSV file stores one row per node and one heuristic column for each destination node that may appear in the released public tests or private tests. Each heuristic value is the straight-line distance from the row node to that destination node. The detail about columns is as follows:

| column | detail |
| :---- | :---- |
| node | A node ID appearing in `edges.csv`. |
| destination node ID | The column header is a destination node ID. The value is the straight-line distance from `node` to that destination node. (Unit: meter) |

Notes:

- `heuristic.csv` is a lookup table for all destinations used by the test cases. Students do not need to generate this file themselves.
- Test cases will only use destination nodes that already exist as columns in `heuristic.csv`.

The file `graph.pkl` stores geometry information for drawing your path. You do not have to process it in your algorithms. Please keep `graph.pkl` in the project root when you generate report maps.

The visualization helper downloads map tiles from public tile servers. If your network blocks tile downloads, you may still use the generated route image as long as the route itself is visible.
