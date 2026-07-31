# 量子力学简述？笔记！

> 原发布于 B 站专栏：[量子力学简述？笔记！](https://www.bilibili.com/read/cv15432274/)
> 发布日期：2022-02-26

**推荐路径：格里菲斯《量子力学》->科恩《量子力学》-> AQM -> QFT...**

此外，up推荐陈童老师**深入浅出**的《量子力学新讲》：https://newquanta.com/

以及知乎樹🌳哥**贴心**的专栏：https://zhuanlan.zhihu.com/c_1015631028714504192

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_001.png)

大致框架如下：（可放大查看）

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_002.png)

*框架梳理*

限于作者水平，难免存在错误，恳请读者指出，感激不尽！

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_003.png)

量子力学算是一门比较出圈的学科了，很多概念广泛流传于各大媒体当中，也是许多人津津乐道的话题。然而，真正触碰这诡异的理论之后，似乎量子力学的趣味就没那么多了TωT

## 历史背景

作为本文背景的烘托，从历史的角度来看，如果不具体到人，常常被提到的事件有：

（1）从**黑体辐射**的理论与实验的矛盾出发，提出**能量量子化**概念；借此概念解释了**光电效应**；而**光量子**作为光的能量量子化，到了**康普顿散射实验**之后才得到完全的认同.

$\boxed{E=\hbar\omega}$

（2）类比相对论的四矢量形式，并结合能量量子化的概念，可以提出**德布罗意波**的概念；并由**电子衍射实验**证实实物粒子的确具有波动性.

$\boxed{\vec{p}=\hbar \vec{k}}$

（3）为了解释**氢原子光谱**，Bohr提出**角动量量子化、定态和跃迁**的概念，并最后由**薛定谔方程**从库仑势出发得到合理解释.

$\boxed{\oint pdq=nh\quad n\in \mathbb{N}}$

（4）由**Stern-Gerlach实验**的结果，不得不假设电子具有额外的**自旋角动量**，由此可以研究**自旋-轨道耦合、化学键中电子**等效应，并最后由**狄拉克方程**从相对论量子力学的角度出发，推导出了自旋的效应.

$\boxed{S_z=\pm\frac{\hbar}{2}}$

这一系列的历史虽然老生常谈，但几乎是量子力学课开篇必讲的氛围烘托。但事实上，要想品味原汁原味的历史发展过程，不妨读一读这两篇分别由爱因斯坦和薛定谔写的原始论文：

《On a Heuristic Point of View Concerning the Production and Transformation of Light》

《Quantisation As A problem of proper Value》

注：历史上，相对论性量子力学以及场的量子理论是和量子力学在同一时间点上发展起来的，例如薛定谔方程最初是由克莱因-戈登方程的经典极限得到的等等。但是由于教学安排和知识螺旋上升的设计规范，我们学习的顺序并不能将其“并行”，而是QM->AQM->QFT.

## 狄拉克符号

一套理论的首要目标是如何描述客观实在，因而我们在正式学习量子力学之前，有必要先把量子力学是如何描述具体物理系统的方法搞清楚，即狄拉克符号. 推荐参考Cohen量子力学第二章的内容，这里仅做一个极其简要的概述.

......

对于单粒子的自旋系统，我们能够测量到的状态叫**本征态**：$\{\lvert 0\rangle,\lvert 1\rangle\}$，相当于Hilbert空间当中的正交基矢量，所有的态都由这些基矢量的线性叠加表示：

$$
\lvert \psi\rangle=C_1\lvert 0\rangle+C_2\lvert 1\rangle
$$

叫作**叠加态**。但要注意，叠加态并不是指物理客体有概率$|C_1|^2$处于态$\lvert 0\rangle$，也有概率$|C_2|^2$处于态$\lvert 1\rangle$，而是真正意义上的处于一种人类之前未发现的新的状态！这一状态是事物本身的性质，而不是由于缺失信息导致的，这一点可以从Bloch球来形象理解，且任意的态$\lvert \psi\rangle$对应于Bloch球的球面，称为**纯态**。

而真正由于缺少信息导致的概率型描述，称为**混合态**，这涉及量子统计的内容，简单来说，混合态对应于Bloch球的球体内部而非球面。

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_004.jpg)

*Bloch球*

......

必要时会用到的数学公式：

$\int_{-\infty}^{\infty}e^{ikx}dx=2\pi\delta(k)$

$\int_0^\infty r^ne^{-br^m}=\frac{1}{m}\frac{\Gamma(\frac{1+n}{m})}{b^{\frac{1+n}{m}}}\quad Re(b)>0$

（此处省略2万字......）

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_005.png)

原本up确实打算这样写下去，但由于种种原因，只能把之前读陈童老师的《量子力学新讲》的笔记拿出来“滥竽充数”，笔记的内容大家看个乐呵就行，没必要细看_(:з」∠)_

陈童老师这本书涵盖了量子力学和高等量子力学的主要内容，而且有些地方处理的简洁且深刻，例如不含时微扰论，直接利用子空间、有效哈密顿量的概念来处理微扰，给出展开到任意阶的微扰方程，避免了大部分教材设变量 $\lambda$ 的繁杂，并为格林函数等方法埋下伏笔；此外，将一些有趣的前沿理论也融入其中，例如量子霍尔效应QHE，分数量子霍尔效应FQHE，任意子Anyon等；总之，如果大家有时间的话，建议去看看，一定会有所收获滴！！

笔记分了两部分，下面这部分主要是些**基本概念**，不涉及微扰论等复杂的东西，虽然简单但也十分重要，**尤其要充分掌握狄拉克符号态矢的写法**，熟练运用。这一点似乎在国内的教学中都强调的很少，也得益于曾书独钟坐标表象，暴力求解PDE的误导，被网友调侃为“国服玩家”。但如果掌握狄拉克符号的写法之后，表象变换将变得易如反掌，什么坐标表象？什么$-i\hbar\nabla$ ? 什么算符的表象变换？不就是投个影，完事！

对于三大绘景(薛定谔、海森堡、相互作用)，以及三种量子力学表述当中的路径积分，可以放到进阶的部分再详细学习。

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_006.png)

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_007.png)

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_008.png)

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_009.png)

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_010.png)

哦对了，矩阵之间的张量积（Kronecker积）十分重要，对于角动量耦合的哈密顿量矩阵的构造十分便捷，这从第四章第一个例子就可以看出，此外，对于构造量子多体的哈密顿量，甚至前沿的信息论当中都有其用武之地！

下面的笔记主要包含：微扰论、对称变换、角动量、全同原理、散射、量子统计简介以及狄拉克方程简介，属于**进阶**的内容。

微扰论与散射联系紧密，尤其是含时微扰论，QED的费曼图本质也是微扰论的发展，此后统计物理当中也广泛地使用“图”来表达微扰。

对称变换主要和诺特定理联系，这套对称与守恒的思想也是量子场论当中最基本的操作，运用群来研究量子力学的潮流也因此而起。例如，角动量主要就是处理$SO(3)$群和$SU(2)$群，全同原理当中也有辫群和置换群。

量子统计主要介绍了一些基本而重要的概念，如纯态、混合态、密度矩阵等，狄拉克方程部分主要展现了对自旋和SOC的准确预言。

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_011.png)

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_012.png)

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_013.png)

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_014.png)

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_015.png)

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_016.png)

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_017.png)

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_018.png)

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_019.png)

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_020.png)

![](../assets/images/advanced_physics/quantum_mechanics/quantum_mechanics_021.png)
