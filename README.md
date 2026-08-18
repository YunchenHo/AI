# Introduction to Artificial Intelligence — Homework

Spring 2026「Introduction to Artificial Intelligence」課程的四份作業。

## 資料夾說明

### HW1 — Route Finding
在 OpenStreetMap 圖資（`edges.csv`、`heuristic.csv`、`graph.pkl`）上實作 BFS / DFS / UCS / A* 路徑搜尋，並比較各演算法的搜尋結果與效率。`result/` 是產生的路線圖與程式碼截圖。

這個資料夾用 [uv](https://docs.astral.sh/uv/) 管理環境，已有自己的 `pyproject.toml`、`uv.lock`、`README.md`（作業原文）與 `REPORT.md`（作業報告），細節請直接看該資料夾內的文件。

**執行方式：**
```bash
cd HW1
uv sync
uv run astar.py   # 或 bfs.py / dfs.py / ucs.py
```
沒裝 `uv` 的話，也可以用 `pip install matplotlib numpy pillow` 手動安裝後直接執行。

### HW2_pacman — Multi-Agent Pacman
經典 Berkeley CS188 Pacman 專案，實作 Minimax / Alpha-Beta / Expectimax 等 multi-agent 搜尋演算法（見 `multiAgents.py`）。

**不需要額外安裝套件**，只用 Python 標準函式庫（含 `tkinter` 做圖形介面，Windows/Mac 官方安裝包通常已內建；Linux 需另外 `sudo apt install python3-tk`）。

**執行方式：**
```bash
cd HW2_pacman
python pacman.py
python autograder.py   # 跑自動評分
```

### HW3 — Text Classification
文字分類作業：NLTK 前處理 → TF-IDF 特徵 → SMOTE 平衡樣本 → SVM / XGBoost 分類，並用 Stratified K-Fold 驗證。Part 1 為理論題（見 `part1_spec.pdf`，答案在報告 PDF 中），Part 2 為程式作業（`part2_code_template.ipynb`）。

**執行方式：**
```bash
cd HW3
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
再打開 `part2_code_template.ipynb` 執行。

### HW4 — RAG Parameter Exploration
Project 2：比較不同 RAG（Retrieval-Augmented Generation）設定對回答品質的影響，設計上是在 **Google Colab** 上執行（`515512_Group17_HW4_code.ipynb` 會用到 Colab 環境與掛載的資源，不建議在本機跑）。

> 這份目前是本機的舊版本，之後會換成 Colab 上的最新版。

## 注意事項

- 上傳前已檢查過所有 `.py` / `.ipynb`，沒有硬編碼的 API key 或 token
- 各資料夾的虛擬環境（`.venv/`、`venv/`）、`__pycache__/`、Jupyter checkpoint 都已列在根目錄 `.gitignore`，不會被提交
- 目前所有檔案大小都在 GitHub 100MB 單檔限制內；如果 HW4 之後從 Colab 加入大型資料檔，記得先確認檔案大小
