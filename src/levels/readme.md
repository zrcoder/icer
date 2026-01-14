# ICER关卡

## 文件格式
使用JavaScript ES模块格式，文件名为 `{关卡序号}.js`（如 `1.js`, `2.js`）

## 动态加载系统

游戏采用动态加载系统，按需加载关卡：

### 关卡组织
```
src/levels/levels/
├── 1/              # 章节1
│   ├── 1.js        # 章节1的第1关
│   └── 2.js        # 章节1的第2关
├── 2/              # 章节2
│   ├── 1.js        # 章节2的第1关
│   └── 2.js        # 章节2的第2关
└── 3/              # 章节3
    └── 1.js        # 章节3的第1关
```

### 加载流程
1. **游戏启动** → 显示章节选择页面
2. **选择章节** → 加载该章节的关卡列表
3. **选择关卡** → 按需加载关卡数据并开始游戏

### 新增关卡
只需创建新的JS文件并在配置中添加章节信息即可，无需预编译或导入。

## 关卡字段
- `name`: 关卡名称
- `difficulty`: 难度等级 (`"tutorial"`, `"basic"`, `"medium"`, `"hard"`)
- `author`: 作者（可选）
- `description`: 关卡描述（可选）
- `optimal_moves`: 最优步数（可选）
- `optimal_time`: 最优时间（可选）
- `grid`: 关卡地图数组

## 地图符号说明
- `.` = 空地
- `P = 玩家起始位置
- `W = 墙壁
- `S = 石头（可推动）
- `F = 火焰（需要熄灭）
- `I = 冰块（可融化）
- `C = 冰块制造器
- `H = 热块制造器
- `1,2,3 = 传送门对（相同数字互相连接）

## 示例配置

```javascript
export default {
  name: "Movement Basics",
  difficulty: "tutorial",
  author: "ICER Team",
  description: "Learn basic movement controls",
  optimal_moves: 5,
  optimal_time: 10,
  grid: [
    "WWWWWWWWWW",
    "W........W",
    "W..P.....W",
    "W........W",
    "W....F...W",
    "WWWWWWWWWW"
  ]
};
```

## 关卡目录组织

关卡按章节组织，目录结构如下：
```
src/levels/levels/
├── 1/           # 章节1
│   ├── 1.js    # 章节1的第1关
│   ├── 2.js    # 章节1的第2关
│   └── ...
├── 2/           # 章节2
│   ├── 1.js
│   └── ...
└── 3/           # 章节3
    └── ...
```

关卡ID由目录结构自动生成，格式为 `{章节}-{关号}`，例如：
- `src/levels/levels/1/1.js` → 关卡ID: `1-1`
- `src/levels/levels/2/3.js` → 关卡ID: `2-3`

## 设计建议

### 关卡设计原则
1. **循序渐进** - 从简单到复杂
2. **目标明确** - 玩家清楚需要做什么
3. **测试友好** - 可以快速重试
4. **视觉清晰** - 布局美观易懂

### 难度递进
- **Tutorial**: 基础操作，1-2个机制
- **Basic**: 简单组合，2-3个机制
- **Medium**: 复杂组合，3-4个机制
- **Hard**: 高难度，所有机制组合

### 关卡元素使用建议
- **早期关卡**: 专注于单一机制
- **中期关卡**: 机制组合
- **后期关卡**: 复杂互动和解谜

## 构建和测试

创建或修改关卡后，运行以下命令更新游戏：
```bash
npm run build          # 构建游戏（动态加载，无需预编译）
npm run dev            # 启动开发服务器测试
```

## 添加新关卡

### 1. 创建关卡文件
在对应章节目录下创建 `{序号}.js` 文件：
```javascript
// src/levels/levels/1/3.js
export default {
  name: "New Level",
  difficulty: "basic",
  author: "Your Name",
  description: "Level description",
  optimal_moves: 15,
  optimal_time: 30,
  grid: [
    "WWWWWWWWWW",
    "W........W",
    "W..P.....W",
    "W........W",
    "W....F...W",
    "WWWWWWWWWW"
  ]
};
```

### 2. 更新章节配置
在 `src/levels/levelManager.ts` 的 `SECTIONS_CONFIG` 中添加关卡：
```typescript
const SECTIONS_CONFIG = {
  1: { name: 'Tutorial Section', levels: [1, 2, 3] }, // 添加关卡3
  2: { name: 'Basic Section', levels: [1, 2] },
  3: { name: 'Advanced Section', levels: [1] }
};
```

### 3. 完成！
游戏会自动识别新关卡，无需重新编译或重启开发服务器。

## API 使用

### 获取章节列表
```typescript
const sections = levelManager.getSections();
// 返回: [{ section: 1, name: 'Tutorial Section', levelCount: 2 }, ...]
```

### 获取章节下的关卡
```typescript
const levels = await levelManager.getLevelsInSection(1);
// 返回: [{ levelId: '1-1', level: 1, name: 'Movement Basics', ... }, ...]
```

### 加载关卡
```typescript
const success = await levelManager.loadLevel(1, 1); // 加载章节1的第1关
// 或
const success = await levelManager.loadLevelById('1-1'); // 通过ID加载
```