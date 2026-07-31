# 热动平衡判据

**★** 根据熵增原理，孤立系统的熵只增不减，从而系统达到平衡态时，熵必然最大。利用这一特性，当系统处于平衡态时给予系统一个虚变动，一定有：

$$
\tilde{\Delta}S=S(x_1+\delta x_1,...,x_n+\delta x_n)-S(x_1,...,x_n)<0
$$

注意上式$\tilde{\Delta}$表示熵的虚变动，并不是实际发生的过程。利用泰勒展开可以写为更详细的形式：

$$
\begin{array}{l}
\left\{\begin{matrix}
\tilde{\Delta}S&=&\delta S+ \frac{1}{2!}\delta^2 S+\frac{1}{3!}\delta^3S+...\\
\delta S&=&\sum_{i=1}^{n}\left(\frac{\partial S}{\partial x_i}\right)\delta x_i\\
\delta^2S&=&\sum_{i,j} \left(\frac{\partial^2S}{\partial x_i\partial x_j}\right)\delta x_i \delta x_j\\
...&=&...
\end{matrix}\right.
\end{array}
$$

根据熵取极值，故有$\delta S=0$,得到平衡条件。熵取极大有$\delta^2S<0$,得到稳定条件。此外根据孤立系统的性质，系统的内能、体积、粒子数都不变。从而有：

$$
\begin{array}{l}
\left\{\begin{matrix}
\delta S=0\\
\delta^2 S<0\\
\delta U=0\quad\delta V=0\quad \delta N=0
\end{matrix}\right.
\end{array}
$$

以上为孤立系统的熵判据的变分表达形式。注意这里仅得到熵取极大值的条件，并没有区分出是稳定还是亚稳平衡。此外，研究临界态时需要分析更多的$\delta^nS$，通常根据奇偶性，断定$\delta^{2n-1}S=0$和$\delta^{2n}S<0$.之后的其他判据也类似。

**★** 根据以上的思想指导，利用等温等容$F=F_{min}$和等温等压$G=G_{min}$的平衡条件,得到：

$$
\begin{array}{l}
\left\{\begin{matrix}
\delta F=0\\
\delta^2 F>0\\
\delta T=0\quad\delta V=0\quad \delta N=0
\end{matrix}\right.
\end{array}
\qquad
\begin{array}{l}
\left\{\begin{matrix}
\delta G=0\\
\delta^2 G>0\\
\delta T=0\quad\delta p=0\quad \delta N=0
\end{matrix}\right.
\end{array}
$$

当然也可导出其他热力学量的判据，通常利用$\boxed{\delta U\leqslant T\delta S-p\delta V}$,在规定某些量不变的情况下，对不等式进行构造导出虚变动趋势，从而推断出平衡条件。
