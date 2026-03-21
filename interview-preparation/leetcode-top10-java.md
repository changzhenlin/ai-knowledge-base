# LeetCode Java面试最常见10道算法题

## 🏆 **Top 1: 两数之和 (Two Sum)**

### 📋 **题目描述**
给定一个整数数组 `nums` 和一个目标值 `target`，请你在该数组中找出和为目标值的那两个整数，并返回他们的数组下标。

### 💡 **解题思路**
```java
// 哈希表法 - O(n) 时间复杂度
public class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            map.put(nums[i], i);
        }
        throw new IllegalArgumentException("No two sum solution");
    }
}
```

### 🎯 **面试要点**
- ✅ **时间复杂度：** O(n)
- ✅ **空间复杂度：** O(n)
- ✅ **关键点：** 哈希表快速查找
- ✅ **变体：** 三数之和、四数之和

---

## 🏆 **Top 2: 反转链表 (Reverse Linked List)**

### 📋 **题目描述**
反转一个单链表。

### 💡 **解题思路**
```java
// 迭代法 - O(n) 时间复杂度
public class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode nextTemp = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nextTemp;
        }
        return prev;
    }
}

// 递归法
public class Solution {
    public ListNode reverseList(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode p = reverseList(head.next);
        head.next.next = head;
        head.next = null;
        return p;
    }
}
```

### 🎯 **面试要点**
- ✅ **时间复杂度：** O(n)
- ✅ **空间复杂度：** O(1) 迭代 / O(n) 递归
- ✅ **关键点：** 指针操作，递归思维
- ✅ **变体：** K个一组反转链表

---

## 🏆 **Top 3: 有效的括号 (Valid Parentheses)**

### 📋 **题目描述**
给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串，判断字符串是否有效。

### 💡 **解题思路**
```java
// 栈 - O(n) 时间复杂度
public class Solution {
    public boolean isValid(String s) {
        Stack<Character> stack = new Stack<>();
        for (char c : s.toCharArray()) {
            if (c == '(') stack.push(')');
            else if (c == '[') stack.push(']');
            else if (c == '{') stack.push('}');
            else if (stack.isEmpty() || stack.pop() != c) return false;
        }
        return stack.isEmpty();
    }
}
```

### 🎯 **面试要点**
- ✅ **时间复杂度：** O(n)
- ✅ **空间复杂度：** O(n)
- ✅ **关键点：** 栈的LIFO特性
- ✅ **变体：** 最长有效括号

---

## 🏆 **Top 4: 合并两个有序数组 (Merge Sorted Array)**

### 📋 **题目描述**
给你两个有序整数数组 `nums1` 和 `nums2`，请你将 `nums2` 合并到 `nums1` 中，使 `nums1` 成为一个有序数组。

### 💡 **解题思路**
```java
// 双指针法 - O(m+n) 时间复杂度
public class Solution {
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        int p1 = m - 1;
        int p2 = n - 1;
        int p = m + n - 1;
        
        while (p1 >= 0 && p2 >= 0) {
            if (nums1[p1] > nums2[p2]) {
                nums1[p--] = nums1[p1--];
            } else {
                nums1[p--] = nums2[p2--];
            }
        }
        
        while (p2 >= 0) {
            nums1[p--] = nums2[p2--];
        }
    }
}
```

### 🎯 **面试要点**
- ✅ **时间复杂度：** O(m+n)
- ✅ **空间复杂度：** O(1)
- ✅ **关键点：** 双指针，从后往前填充
- ✅ **变体：** 合并K个有序数组

---

## 🏆 **Top 5: 二叉树的最大深度 (Maximum Depth of Binary Tree)**

### 📋 **题目描述**
给定一个二叉树，找出其最大深度。

### 💡 **解题思路**
```java
// 递归法 - O(n) 时间复杂度
public class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) return 0;
        return Math.max(maxDepth(root.left), maxDepth(root.right)) + 1;
    }
}

// 迭代法 - BFS
public class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) return 0;
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        int depth = 0;
        while (!queue.isEmpty()) {
            int size = queue.size();
            depth++;
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                if (node.left != null) queue.offer(node.left);
                if (node.right != null) queue.offer(node.right);
            }
        }
        return depth;
    }
}
```

### 🎯 **面试要点**
- ✅ **时间复杂度：** O(n)
- ✅ **空间复杂度：** O(h) 递归 / O(n) 迭代
- ✅ **关键点：** 递归分治，BFS层序遍历
- ✅ **变体：** 最小深度、平衡二叉树

---

## 🏆 **Top 6: 买卖股票的最佳时机 (Best Time to Buy and Sell Stock)**

### 📋 **题目描述**
给定一个数组 `prices`，它的第 `i` 个元素是一支给定股票第 `i` 天的价格。如果你最多只允许完成一笔交易，设计一个算法来计算你所能获取的最大利润。

### 💡 **解题思路**
```java
// 一次遍历法 - O(n) 时间复杂度
public class Solution {
    public int maxProfit(int[] prices) {
        int minPrice = Integer.MAX_VALUE;
        int maxProfit = 0;
        for (int price : prices) {
            if (price < minPrice) {
                minPrice = price;
            } else if (price - minPrice > maxProfit) {
                maxProfit = price - minPrice;
            }
        }
        return maxProfit;
    }
}
```

### 🎯 **面试要点**
- ✅ **时间复杂度：** O(n)
- ✅ **空间复杂度：** O(1)
- ✅ **关键点：** 维护最小值和最大利润
- ✅ **变体：** 多次交易、含手续费、冷冻期

---

## 🏆 **Top 7: 爬楼梯 (Climbing Stairs)**

### 📋 **题目描述**
假设你正在爬楼梯。需要 n 阶你才能到达楼顶。每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？

### 💡 **解题思路**
```java
// 动态规划 - O(n) 时间复杂度
public class Solution {
    public int climbStairs(int n) {
        if (n <= 2) return n;
        int[] dp = new int[n + 1];
        dp[1] = 1;
        dp[2] = 2;
        for (int i = 3; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        return dp[n];
    }
}

// 优化空间 - O(1) 空间复杂度
public class Solution {
    public int climbStairs(int n) {
        if (n <= 2) return n;
        int prev2 = 1;
        int prev1 = 2;
        for (int i = 3; i <= n; i++) {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        return prev1;
    }
}
```

### 🎯 **面试要点**
- ✅ **时间复杂度：** O(n)
- ✅ **空间复杂度：** O(n) 或 O(1)
- ✅ **关键点：** 斐波那契数列，动态规划
- ✅ **变体：** 每次可爬K个台阶

---

## 🏆 **Top 8: 合并两个有序链表 (Merge Two Sorted Lists)**

### 📋 **题目描述**
将两个升序链表合并为一个新的升序链表并返回。

### 💡 **解题思路**
```java
// 递归法 - O(m+n) 时间复杂度
public class Solution {
    public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        if (l1 == null) return l2;
        if (l2 == null) return l1;
        if (l1.val < l2.val) {
            l1.next = mergeTwoLists(l1.next, l2);
            return l1;
        } else {
            l2.next = mergeTwoLists(l1, l2.next);
            return l2;
        }
    }
}

// 迭代法
public class Solution {
    public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode curr = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val < l2.val) {
                curr.next = l1;
                l1 = l1.next;
            } else {
                curr.next = l2;
                l2 = l2.next;
            }
            curr = curr.next;
        }
        curr.next = l1 != null ? l1 : l2;
        return dummy.next;
    }
}
```

### 🎯 **面试要点**
- ✅ **时间复杂度：** O(m+n)
- ✅ **空间复杂度：** O(1)
- ✅ **关键点：** 递归分治，迭代指针
- ✅ **变体：** 合并K个有序链表

---

## 🏆 **Top 9: 盛最多水的容器 (Container With Most Water)**

### 📋 **题目描述**
给你 n 个非负整数 a1, a2, ..., an，每个数代表坐标中的一个点 (i, ai)。在坐标内画 n 条垂直线，垂直线 i 的两个端点分别为 (i, ai) 和 (i, 0)。找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。

### 💡 **解题思路**
```java
// 双指针法 - O(n) 时间复杂度
public class Solution {
    public int maxArea(int[] height) {
        int maxArea = 0;
        int left = 0;
        int right = height.length - 1;
        while (left < right) {
            int width = right - left;
            int minHeight = Math.min(height[left], height[right]);
            maxArea = Math.max(maxArea, width * minHeight);
            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }
        return maxArea;
    }
}
```

### 🎯 **面试要点**
- ✅ **时间复杂度：** O(n)
- ✅ **空间复杂度：** O(1)
- ✅ **关键点：** 双指针，贪心策略
- ✅ **变体：** 接雨水问题

---

## 🏆 **Top 10: 最长公共子序列 (Longest Common Subsequence)**

### 📋 **题目描述**
给定两个字符串 text1 和 text2，返回这两个字符串的最长公共子序列的长度。

### 💡 **解题思路**
```java
// 动态规划 - O(m*n) 时间复杂度
public class Solution {
    public int longestCommonSubsequence(String text1, String text2) {
        int m = text1.length();
        int n = text2.length();
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        return dp[m][n];
    }
}
```

### 🎯 **面试要点**
- ✅ **时间复杂度：** O(m*n)
- ✅ **空间复杂度：** O(m*n)
- ✅ **关键点：** 动态规划，子问题分解
- ✅ **变体：** 最长公共子串、编辑距离

---

## 📊 **算法分类总结**

### 🔧 **必备技能**
| 类别 | 题数 | 重点算法 |
|------|------|----------|
| **数组** | 3道 | 双指针、哈希表 |
| **链表** | 3道 | 递归、迭代 |
| **动态规划** | 2道 | 状态转移、空间优化 |
| **树** | 1道 | 递归、BFS |
| **栈/队列** | 1道 | 单调栈、层序遍历 |

### ⏰ **时间复杂度要求**
- **O(n)**: 6道 (必须掌握)
- **O(n²)**: 2道 (需要优化)
- **O(m+n)**: 2道 (双序列问题)

### 🎯 **面试准备建议**

**📚 基础阶段 (1-2周)**
1. 熟练掌握每种数据结构的特性
2. 理解常见算法思想（贪心、分治、动态规划）
3. 背诵模板代码，能快速写出

**🚀 进阶阶段 (2-3周)**
1. 大量刷题，总结规律
2. 学习优化技巧（空间换时间、剪枝等）
3. 练习手写代码，注意边界条件

**💡 高级阶段 (1-2周)**
1. 研究变体题目
2. 总结面试技巧和答题套路
3. 模拟面试，练习表达

---

## 🎯 **面试回答技巧**

### 📋 **标准答题流程**
1. **理解题意**：确认输入输出，边界条件
2. **思路分析**：说明解题思路和算法选择
3. **代码实现**：写出清晰、健壮的代码
4. **复杂度分析**：时间和空间复杂度
5. **优化讨论**：可能的优化方向

### 💡 **加分项**
- ✅ **多种解法**：展示不同思路
- ✅ **边界处理**：考虑特殊情况
- ✅ **代码规范**：命名清晰，结构良好
- ✅ **沟通表达**：思路清晰，表达流畅

---

## 📝 **刷题计划建议**

**📅 每日安排**
- **周一**：数组 + 字符串
- **周二**：链表 + 栈/队列
- **周三**：树 + 二叉搜索树
- **周四**：动态规划
- **周五**：图论 + 搜索
- **周末**：综合练习 + 总结

**🎯 优先级**
1. **必会题**：前5道，必须熟练掌握
2. **高频题**：6-8道，重点练习
3. **进阶题**：9-10道，理解思路

---

**更新时间：** 2026-03-16
**适用岗位：** Java工程师、算法工程师
**准备建议：** 每道题都要能独立写出代码，理解多种解法