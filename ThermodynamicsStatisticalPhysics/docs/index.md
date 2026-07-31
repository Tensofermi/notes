# 热力学与统计物理笔记

## 背景介绍

热力学与统计物理讨论的是同一件事的两种语言：热力学从宏观状态函数出发，用少数变量描述系统的平衡、相变和能量转化；统计物理则从微观粒子的状态数出发，解释温度、熵、热容、涨落和分布函数为什么会出现。

这份笔记沿着“热力学基本规律 $\rightarrow$ 平衡判据与相变 $\rightarrow$ 分子动理学 $\rightarrow$ 统计分布 $\rightarrow$ 系综理论”的路线整理。前半部分更像宏观热力学的计算工具箱，后半部分则逐渐转向微观图像，把熵、配分函数和系综这些概念串起来。

## PDF 版本

如果想离线阅读可以下载2021年的整理版：[热统知识梳理 PDF](https://tensofermi.github.io/notes/physical_notes/%E7%83%AD%E7%BB%9F%E7%9F%A5%E8%AF%86%E6%A2%B3%E7%90%86.pdf)。

## 内容结构

| 章节 | 内容 |
| --- | --- |
| 第1章 | [热力学的基本概念](chapter_01_basic_concepts/index.md) |
| 第2章 | [均匀体系的热力学性质](chapter_02_uniform_system/index.md) |
| 第3章 | [单元体系相变](chapter_03_phase_transition/index.md) |
| 第4章 | [多元体系平衡](chapter_04_multicomponent_system/index.md) |
| 第5章 | [分子动理学](chapter_05_kinetic_theory/index.md) |
| 第6章 | [近独立子系最概然分布](chapter_06_most_probable_distribution/index.md) |
| 第7章 | [Boltzmann统计理论](chapter_07_boltzmann_statistics/index.md) |
| 第8章 | [Bose/Fermi统计理论](chapter_08_bose_fermi_statistics/index.md) |
| 第9章 | [系综理论](chapter_09_ensembles/index.md) |

## 阅读建议

建议先把第一、二章中的热力学基本方程、Maxwell 关系和特性函数读顺；它们会在相变、化学势和系综理论中反复出现。公式较密的地方可以先抓住“变量选择”和“约束条件”，再回头补推导细节。

读统计物理部分时，可以始终盯住一条线索：微观状态数 $\Omega$ 给出熵，配分函数 $Z$ 给出热力学量，而不同约束条件对应不同系综。这样看，Boltzmann、Bose、Fermi 分布就不是孤立公式，而是同一套极值思想在不同粒子统计下的结果。
