# HW1-1: Grid Map Environment & MDP Solver

這是一個基於 Flask 構建的網頁應用程式，用來視覺化與實作強化學習（Reinforcement Learning）中的**馬可夫決策過程（MDP）**。專案包含了網格地圖的建立、隨機策略評估（Policy Evaluation），以及最佳解疊代（Value Iteration）。

## 🖼️ Demo 畫面展示

<p align="center">
  <img src="assets/demo2.png" alt="Grid Map Initialization" width="600"/>
  <br>
  <em>網格地圖設定與操作介面，支援動態生成 X 軸與 Y 軸座標提示</em>
</p>

<p align="center">
  <img src="assets/demo1.png" alt="Value Iteration & Optimal Paths" width="600"/>
  <br>
  <em>Value Iteration 計算結果：視覺化展示單一最佳路徑（粉紅色高光）</em>
</p>

## 🌟 功能展示與階段實作 (Phases)

### 階段 1-1: 網格地圖開發 (Grid Map Development)
- **動態維度**：允許使用者輸入 `3` 到 `9` 之間的數字 $n$，動態生成大小為 $n \times n$ 的網格地圖。
- **互動式設計**：
  - **起點 (Start)**：點擊第一格顯示為**綠色**。
  - **終點 (End)**：點擊第二格顯示為**紅色**（目標狀態 `+10` Reward）。
  - **障礙物 (Obstacle)**：後續點擊之網格顯示為**灰色**，最多可設定 $n-2$ 個障礙物（撞牆或撞障礙物的 Step Penalty 為 `-1`）。
- **使用者體驗 (UX)**：具備錯誤防呆檢查（如超出數量限制的 Toast 提示）、微動畫與現代化的深色主題。網格外圍具有自動生成的 $X$ 與 $Y$ 座標軸。

### 階段 1-2: 策略顯示與價值評估 (Policy Evaluation)
- **隨機策略生成**：對每個非終端與非障礙物的狀態發布隨機的行動策略（$\uparrow, \rightarrow, \downarrow, \leftarrow$）。
- **價值函數評估 (Value Function)**：
  - 實作 **Iterative Policy Evaluation** 演算法，藉由 Bellman Equation 推導每個狀態的價值 $V(s)$。
  - **MDP 參數**：折扣參數 $\gamma = 0.9$，收斂閾值 $\theta = 10^{-4}$。
- **雙矩陣並排顯示**：按下 `Random Policy Eval` 按鈕後，會動態展開視窗並同時顯示「Value Matrix（價值矩陣）」與「Policy Matrix（策略矩陣）」。

### 階段 1-3: 價值疊代與最佳路徑 (Value Iteration & Optimal Path)
- **尋找最佳策略 (Optimal Policy)**：
  - 實作 **Value Iteration** 演算法，找出在當前環境設置下，能夠最大化 Expected Return 的行動指南。
- **單一最小路徑提取 (Single Optimal Path)**：
  - 遇到相同價值時，演算法會挑選並儲存第一個最佳的行動方向，確保策略單一性。
  - 運用程式邏輯找出避開障礙物、完美抵達終點的「最佳最短路徑」。
- **路徑視覺化**：
  - 在 Policy Matrix 畫面上，將最短路徑所經過的網格亮起**粉紅色高光**，一目了然。

## 🚀 技術架構 (Technology Stack)

- **後端 (Backend)**: Python, Flask, NumPy (負責強化學習之 Value Iteration 與 Policy Evaluation 核心演算法矩陣運算)。
- **前端 (Frontend)**: HTML5, CSS3, Vanilla JavaScript (負責網格 DOM 渲染、動畫效果及介面互動)，透過 AJAX fetch API 與後端溝通。

## 📂 專案結構 (Directory Structure)
```
HW1-1/
├── app.py                  # Flask 核心伺服器與強化學習 API 端點
├── requirements.txt        # Python 依賴套件 (Flask, NumPy 等)
├── templates/
│   └── index.html          # HTML UI 結構、CSS 樣式與負責串接 API 的前端 JS 邏輯
├── README.md               # 專案說明文件
└── assets/                 # 存放 Demo 圖片用資料夾
```

## 🛠️ 如何執行本專案 (How to run)

本專案是一個具互動性的 Flask 網頁應用程式，請確保您的系統已安裝 Python 3.x 環境。

1. 克隆（Clone）此專案至本地端（或直接下載 ZIP）：
   ```bash
   git clone https://github.com/Jester-99/grid-map-app.git
   cd grid-map-app
   ```
2. 安裝必要的 Python 套件：
   ```bash
   pip install -r requirements.txt
   ```
3. 執行 Flask 伺服器啟動程式：
   ```bash
   python app.py
   ```
4. 開啟您的瀏覽器，並前往 `http://localhost:5000` 即可開始體驗！

> 💡 **提示**: 本專案的 `Demo` 分支為「純前端」靜態版本，可直接掛載於 GitHub Pages 執行，若不想安裝環境可直接切換至該分支遊玩！
