from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    n = data.get('n', 5)
    start = data.get('start', -1)
    end = data.get('end', -1)
    obstacles = data.get('obstacles', [])
    
    # Generate random policy
    # === 強化學習 (RL) MDP 參數設定 ===
    # 0: 上 (Up), 1: 右 (Right), 2: 下 (Down), 3: 左 (Left)
    arrows = {0: '↑', 1: '→', 2: '↓', 3: '←'}
    
    # 隨機產生一個確定性策略 (Deterministic Random Policy)
    policy = np.random.randint(0, 4, size=n * n)
    
    # 初始化價值矩陣 V(s) 為 0
    V = np.zeros(n * n)
    
    # gamma: 折扣因子 (Discount factor)，0.9 代表重視未來獎勵
    gamma = 0.9
    # theta: 收斂判定閾值 (當所有 V(s) 的變化小於此值即視為收斂)
    theta = 1e-4
    
    terminals = [end] if end != -1 else []
    obs_set = set(obstacles)
    
    # 定義狀態轉移動態與獎勵函數 (Environment Dynamic -> p(s', r | s, a))
    def get_next_state_reward(s, a):
        # 終點與障礙物是吸收狀態 (Absorbing states)，無法移動
        if s in terminals or s in obs_set:
            return s, 0
            
        r, c = s // n, s % n
        nr, nc = r, c
        if a == 0: nr -= 1    # 上
        elif a == 1: nc += 1  # 右
        elif a == 2: nr += 1  # 下
        elif a == 3: nc -= 1  # 左
        
        # 邊界判定：撞牆停留在原地，獲得步數懲罰 -1
        if nr < 0 or nr >= n or nc < 0 or nc >= n:
            return s, -1 
            
        ns = nr * n + nc
        
        # 障礙物判定：撞到障礙物停留在原地，獲得步數懲罰 -1
        if ns in obs_set:
            return s, -1 
            
        # 終點判定：成功走到終點，獲得目標獎勵 +10 (進入終端狀態)
        if ns in terminals:
            return ns, 10 
        
        # 正常移動：進入下一個狀態，並獲得一般步數懲罰 -1 (促使 Agent 尋找最短路徑)
        return ns, -1 
        
    # === 策略評估 (Policy Evaluation) ===
    # 根據講義公式： V(s) = \sum_a \pi(a|s) \sum_{s', r} p(s', r|s, a) [r + \gamma V(s')]
    # 因為我們是評估「確定性策略」(Deterministic Policy)，且環境轉移沒有隨機性，
    # 公式可簡化成： V(s) = r + \gamma V(s')
    while True:
        delta = 0
        V_new = np.copy(V)
        for s in range(n * n):
            # 終點與障礙物的 Value 固定為 0，不須評估
            if s in terminals or s in obs_set:
                continue
                
            # 取得當前策略中，該 state 所指示的動作 a
            a = policy[s]
            
            # 從環境取得 next state (s') 與 reward (r)
            ns, reward = get_next_state_reward(s, a)
            
            v = V[s]
            # 進行 Bellman Backup 價值更新
            V_new[s] = reward + gamma * V[ns]
            
            # 計算該回合中，價值變化最大的幅度 (用來判斷收斂)
            delta = max(delta, abs(v - V_new[s]))
            
        V = V_new # 更新 Value 矩陣
        
        # 若所有狀態價值的變動都小於 theta，則完成 Policy Evaluation
        if delta < theta:
            break
            
    # 將 policy 格式化為前端顯示用的箭頭與符號
    policy_display = []
    for s in range(n * n):
        if s in obs_set:
            policy_display.append('')
        elif s in terminals:
            policy_display.append('★')
        else:
            policy_display.append(arrows[policy[s]])
            
    return jsonify({
        'values': np.round(V, 2).tolist(),
        'policy': policy_display
    })

@app.route('/value_iteration', methods=['POST'])
def value_iteration():
    data = request.json
    n = data.get('n', 5)
    start = data.get('start', -1)
    end = data.get('end', -1)
    obstacles = data.get('obstacles', [])
    
    # === 強化學習 (RL) MDP 參數設定 ===
    arrows = {0: '↑', 1: '→', 2: '↓', 3: '←'}
    V = np.zeros(n * n)
    gamma = 0.9
    theta = 1e-4
    
    terminals = [end] if end != -1 else []
    obs_set = set(obstacles)
    
    def get_next_state_reward(s, a):
        if s in terminals or s in obs_set:
            return s, 0
            
        r, c = s // n, s % n
        nr, nc = r, c
        if a == 0: nr -= 1    # 上
        elif a == 1: nc += 1  # 右
        elif a == 2: nr += 1  # 下
        elif a == 3: nc -= 1  # 左
        
        if nr < 0 or nr >= n or nc < 0 or nc >= n:
            return s, -1 
            
        ns = nr * n + nc
        
        if ns in obs_set:
            return s, -1 
            
        if ns in terminals:
            return ns, 10 
        
        return ns, -1 

    # === Value Iteration (價值疊代) ===
    # 講義公式 V(s) <- max_a \sum_{s', r} p(s', r|s, a)[r + \gamma V(s')]
    while True:
        delta = 0
        V_new = np.copy(V)
        for s in range(n * n):
            if s in terminals or s in obs_set:
                continue
                
            # 尋找能夠最大化 Expected Return 的動作
            max_val = -float('inf')
            for a in range(4):
                ns, reward = get_next_state_reward(s, a)
                val = reward + gamma * V[ns]
                if val > max_val:
                    max_val = val
                    
            V_new[s] = max_val
            delta = max(delta, abs(V[s] - V_new[s]))
            
        V = V_new
        if delta < theta:
            break
            
    # === 提取最佳策略 (Extract Optimal Policy) ===
    # 講義公式: \pi(s) = argmax_a \sum p(s', r|s, a)[r + \gamma V(s')]
    policy = [0 for _ in range(n * n)]
    for s in range(n * n):
        if s in terminals or s in obs_set:
            continue
            
        max_val = -float('inf')
        best_a = 0
        for a in range(4):
            ns, reward = get_next_state_reward(s, a)
            val = reward + gamma * V[ns]
            if val > max_val:
                max_val = val
                best_a = a
        policy[s] = best_a
        
    policy_display = []
    for s in range(n * n):
        if s in obs_set:
            policy_display.append('')
        elif s in terminals:
            policy_display.append('★')
        else:
            policy_display.append(arrows[policy[s]])
            
    # === 找出所有最佳/最小路徑 (Trace All Optimal Paths) ===
    path_nodes = set()
    if start != -1 and end != -1:
        curr = start
        curr_path = []
        visited = set()
        while curr != end and curr not in visited:
            curr_path.append(curr)
            visited.add(curr)
            a = policy[curr]
            ns, _ = get_next_state_reward(curr, a)
            if ns == curr:
                break
            curr = ns
        if curr == end:
            curr_path.append(end)
            
        path_nodes.update(curr_path)
                    
    path = list(path_nodes)

    return jsonify({
        'values': np.round(V, 2).tolist(),
        'policy': policy_display,
        'path': path
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
