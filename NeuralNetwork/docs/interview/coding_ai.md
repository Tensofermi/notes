# AI 方向编程题思路

AI 岗笔试中的编程题通常不是让你写神经网络，而是考基础算法、数据结构和工程建模能力。准备时要把题目翻译成清晰的数据结构问题。

## 题目：Top-k 最大元素

**来源背景**：华为 / 字节编程题常见类型改写。

**考点定位**：堆、排序、复杂度。

**先给结论**：如果只需要 top-k，不必完整排序；可用大小为 $k$ 的小根堆。

**解题思路**：

遍历数组，维护小根堆：

- 堆大小小于 $k$，直接入堆。
- 否则若当前数大于堆顶，弹出堆顶并加入当前数。

复杂度：

$$
O(n\log k).
$$

**代码实现**：

```python
import heapq

def top_k(nums, k):
    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)
    return sorted(heap, reverse=True)
```

**易错点**：

- $k=0$ 要特殊处理。
- top-k 最大用小根堆，top-k 最小用大根堆或取负号。

**关联阅读**：[计算复杂度速览](../prerequisites/complexity_classes.md)。

## 题目：滑动窗口最大值

**来源背景**：数组和队列类笔试题改写。

**考点定位**：单调队列。

**先给结论**：用单调递减队列保存候选下标，队首始终是当前窗口最大值。

**解题思路**：

每个元素进入队列一次、弹出一次，所以总复杂度：

$$
O(n).
$$

**代码实现**：

```python
from collections import deque

def max_sliding_window(nums, k):
    q = deque()
    ans = []
    for i, x in enumerate(nums):
        while q and q[0] <= i - k:
            q.popleft()
        while q and nums[q[-1]] <= x:
            q.pop()
        q.append(i)
        if i >= k - 1:
            ans.append(nums[q[0]])
    return ans
```

**易错点**：

- 队列里存下标，不只存值，这样才能判断是否过期。
- 弹出尾部较小元素不影响答案，因为它们永远不会再成为最大值。

**关联阅读**：[复杂度速览](../prerequisites/complexity_classes.md)。

## 题目：最长无重复子串

**来源背景**：字符串高频题改写。

**考点定位**：双指针、哈希表。

**先给结论**：用滑动窗口维护当前没有重复字符的区间。

**解题思路**：

右指针扩展，遇到重复字符时移动左指针，直到窗口重新合法。

**代码实现**：

```python
def length_of_longest_substring(s):
    last = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

**易错点**：

- 左指针不能往回退。
- 更新 `left` 时要判断重复字符是否在当前窗口内。

**关联阅读**：[AI 方向编程题思路](coding_ai.md)。

## 题目：最短路径应该用 BFS 还是 Dijkstra？

**来源背景**：图算法笔试题改写。

**考点定位**：图搜索、边权、复杂度。

**先给结论**：

- 无权图最短路用 BFS。
- 非负权图最短路用 Dijkstra。
- 有负权边要考虑 Bellman-Ford 或 SPFA 类算法。

**解题思路**：

BFS 按层扩展，第一次到达某节点就是最短步数。Dijkstra 每次取当前距离最小的未确定节点，适用于非负权边。

**易错点**：

- 有权图不能随便用 BFS。
- Dijkstra 不适用于负权边。
- 网格题常可看成图。

**关联阅读**：[计算复杂度速览](../prerequisites/complexity_classes.md)。

## 题目：0/1 背包怎么写状态转移？

**来源背景**：动态规划基础题改写。

**考点定位**：DP、状态定义、滚动数组。

**先给结论**：`dp[c]` 表示容量为 `c` 时的最大价值，遍历物品时容量要倒序。

**解题思路**：

转移：

$$
dp[c]=\max(dp[c],dp[c-w_i]+v_i).
$$

容量倒序是为了保证每个物品只用一次。

**代码实现**：

```python
def knapsack(weights, values, cap):
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]
```

**易错点**：

- 0/1 背包倒序；完全背包正序。
- 状态定义先写清楚，再写转移。

**关联阅读**：[复杂度速览](../prerequisites/complexity_classes.md)。

## 题目：如何实现 softmax 并避免溢出？

**来源背景**：AI 工程编程题改写。

**考点定位**：数值稳定、数组操作。

**先给结论**：先减最大值，再做指数和归一化。

**代码实现**：

```python
import math

def softmax(xs):
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    s = sum(exps)
    return [v / s for v in exps]
```

**解题思路**：

因为：

$$
{e^{x_i}\over\sum_j e^{x_j}}
=
{e^{x_i-m}\over\sum_j e^{x_j-m}}.
$$

**易错点**：

- 不减最大值时，大 logit 会导致 `exp` overflow。
- 如果所有输入都是极小数，直接 exp 也可能 underflow。

**关联阅读**：[数值精度](../numerical_precision.md)。

## 题目：批量 padding 后如何构造 attention mask？

**来源背景**：NLP 工程编程题改写。

**考点定位**：padding、mask、batch。

**先给结论**：padding mask 标记哪些位置是有效 token，attention 时让 padding 位置不能被读。

**代码实现**：

```python
def make_padding_mask(lengths, max_len):
    mask = []
    for n in lengths:
        mask.append([i < n for i in range(max_len)])
    return mask
```

例如 `lengths=[3, 5]`，`max_len=5`：

```text
True True True False False
True True True True  True
```

**易错点**：

- padding mask 和 causal mask 不是同一个东西。
- 有些框架中 `True` 表示保留，有些表示屏蔽，要看 API。

**关联阅读**：[训练目标与 Mask](../Transformer/training.md)。

## 题目：在线统计均值和方差

**来源背景**：流式数据和工程统计题改写。

**考点定位**：数值稳定、单遍算法。

**先给结论**：用 Welford 算法可以单遍稳定更新均值和方差。

**代码实现**：

```python
def mean_var_stream(xs):
    n = 0
    mean = 0.0
    m2 = 0.0
    for x in xs:
        n += 1
        delta = x - mean
        mean += delta / n
        delta2 = x - mean
        m2 += delta * delta2
    var = m2 / (n - 1) if n > 1 else 0.0
    return mean, var
```

**解题思路**：

直接用：

$$
\mathbb E[x^2]-\mathbb E[x]^2
$$

在大数相减时可能有精度损失。Welford 算法更稳定。

**易错点**：

- 样本方差除以 $n-1$，总体方差除以 $n$。
- 流式场景不能假设所有数据都能放进内存。

**关联阅读**：[数值精度](../numerical_precision.md)。

