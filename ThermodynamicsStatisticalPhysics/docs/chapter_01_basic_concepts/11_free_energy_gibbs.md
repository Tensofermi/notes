# 自由能、Gibbs函数

**★** 考虑两种过程：等温等容和等温等压。虽然利用熵的定义可以对其演化的方向进行判断，但在处理复杂问题时不太方便，因而引入两个辅助量：自由能F和Gibbs函数G。**(P.S.这里的等温、等压、等容是指系统与相应的热源、定容或定压环境相联系，初末平衡态满足这些约束；不可逆过程中间态不一定处处平衡。)**

由一般过程的热力学基本方程,对于等温过程得到：

$$
\Delta U\leqslant T\Delta S+W \Rightarrow W\geqslant \Delta U-T\Delta S
$$

从而定义$\boxed{F=U-TS}$，上式可以写作：

$$
W\geqslant\Delta F\Rightarrow -W=W_{\text{系统对外}}\leqslant-\Delta F
$$

表示系统对外做功的上限是F的减少量。

(1)在等温的同时考虑等容过程,系统对外不做功，因而有：

$$
\Delta F\leqslant0
$$

**即等温等容条件下，系统自由能永不增加。**

(2)在等温的同时考虑等压过程，且只有体积功，则：

$$
-p\Delta V\geqslant\Delta U-T\Delta S\Rightarrow \Delta U-T\Delta S+p\Delta V\leqslant0
$$

从而定义$\boxed{G=H-TS}$，到：

$$
\Delta G\leqslant0
$$

**即等温等压条件下，系统吉布斯函数永不增加。**

注意，以上推导仅考虑体积功，对于非体积功$W'$,有$\Delta F\leqslant W'$和$\Delta G\leqslant W'$作为过程可逆性的判据。
