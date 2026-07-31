# 四个特性函数的微分方程以及Maxwell关系

**★** 目前为止，我们利用热一和热二，定义了与内能U相关的辅助量焓H、自由能F、吉布斯函数G,并且得到了可逆过程的热力学基本方程：

$$
\begin{array}{l}
\left\{\begin{matrix}
H=U+pV \\
F=U-TS \\
G=H-TS
\end{matrix}\right.
\end{array}\quad + \quad dU=TdS-pdV
$$

根据以上信息，不难得到三个辅助量的全微分(实际上就是勒让德变换)：

$$
\boxed{dH}=dU+pdV+Vdp=TdS-\cancel{pdV}+\cancel{pdV}+Vdp=\boxed{TdS+Vdp}
$$

$$
\boxed{dF}=dU-TdS-SdT=\cancel{TdS}-pdV-\cancel{TdS}-SdT=\boxed{-SdT-pdV}
$$

$$
\boxed{dG}=dH-TdS-SdT=\cancel{TdS}+Vdp-\cancel{TdS}-SdT=\boxed{-SdT+Vdp}
$$

由于态函数全微分的性质，混合二阶偏导可以交换顺序，不难得到：

(1)内能U(S,V)：

$$
dU=\left(\frac{\partial U}{\partial S}\right)_VdS+\left(\frac{\partial U}{\partial V}\right)_SdV=TdS-pdV
$$

$$
\Rightarrow\begin{array}{l}
\left\{\begin{matrix}
\left(\frac{\partial U}{\partial S}\right)_V=T \\
\left(\frac{\partial U}{\partial V}\right)_S=-p
\end{matrix}\right.
\end{array}\Rightarrow \boxed{
\left(\frac{\partial T}{\partial V}\right)_S=-\left(\frac{\partial p}{\partial S}\right)_V}
$$

(2)焓H(S,p)：

$$
dH=\left(\frac{\partial H}{\partial S}\right)_pdS+\left(\frac{\partial H}{\partial p}\right)_Sdp=TdS+Vdp
$$

$$
\Rightarrow\begin{array}{l}
\left\{\begin{matrix}
\left(\frac{\partial H}{\partial S}\right)_p=T \\
\left(\frac{\partial H}{\partial p}\right)_S=V
\end{matrix}\right.
\end{array}\Rightarrow \boxed{
\left(\frac{\partial T}{\partial p}\right)_S=\left(\frac{\partial V}{\partial S}\right)_p}
$$

(3)自由能F(T,V)：

$$
dF=\left(\frac{\partial F}{\partial T}\right)_VdT+\left(\frac{\partial F}{\partial V}\right)_TdV=-SdT-pdV
$$

$$
\Rightarrow\begin{array}{l}
\left\{\begin{matrix}
\left(\frac{\partial F}{\partial T}\right)_V=-S \\
\left(\frac{\partial F}{\partial V}\right)_T=-p
\end{matrix}\right.
\end{array}\Rightarrow \boxed{
\left(\frac{\partial S}{\partial V}\right)_T=\left(\frac{\partial p}{\partial T}\right)_V}
$$

(4)吉布斯函数G(T,p)：

$$
dG=\left(\frac{\partial G}{\partial T}\right)_pdT+\left(\frac{\partial G}{\partial p}\right)_Tdp=-SdT+Vdp
$$

$$
\Rightarrow\begin{array}{l}
\left\{\begin{matrix}
\left(\frac{\partial G}{\partial T}\right)_p=-S \\
\left(\frac{\partial G}{\partial p}\right)_T=V
\end{matrix}\right.
\end{array}\Rightarrow \boxed{
\left(\frac{\partial S}{\partial p}\right)_T=-\left(\frac{\partial V}{\partial T}\right)_p}
$$

由此得到四个常用的Maxwell关系。对于这四个关系的记忆和使用，需要首先理解并记忆四个特性函数的全微分表达式，在此基础上知道麦氏关系对角分别是p、V和T、S，并且分母或分子与偏导固定的量进行交换，偏导分子分母p、T同号p、S不同号。根据以上技巧，不难记住四式。

**★** 下面初步对以上关系式进行应用，求出热容的偏导式。

首先由热力学基本方程和S(T,V)的全微分展开得到：

$$
dU=TdS-pdV\qquad dS=\left(\frac{\partial S}{\partial T}\right)_VdT+\left(\frac{\partial S}{\partial V}\right)_TdV
$$

为了使基本方程中的$dS$变为$dT$，将$dS$代入得到：

$$
dU=T\left(\frac{\partial S}{\partial T}\right)_VdT+\left[T\left(\frac{\partial S}{\partial V}\right)_T-p\right]dV
$$

根据dU的偏导得到：

$$
\left(\frac{\partial U}{\partial T}\right)_V=\boxed{T\left(\frac{\partial S}{\partial T}\right)_V=C_V}\qquad \left(\frac{\partial U}{\partial V}\right)_T=T\left(\frac{\partial S}{\partial V}\right)_T-p
$$

利用麦氏关系，消去不易测量的S，将第二式化为上一章文献中的公式：

$$
\boxed{\left(\frac{\partial U}{\partial V}\right)_T=T\left(\frac{\partial p}{\partial T}\right)_V-p}
$$

上式即可根据物态方程求出内能对体积的依赖关系，详见前一章节。

另一方面，如果展开H(T,p)和S(T,p),并利用$dH=TdS+Vdp$同理可以得到：

$$
\left(\frac{\partial H}{\partial T}\right)_p=\boxed{T\left(\frac{\partial S}{\partial T}\right)_p=C_p}\qquad \left(\frac{\partial H}{\partial p}\right)_T=T\left(\frac{\partial S}{\partial p}\right)_T+V
$$

同样利用麦氏关系消去S得到：

$$
\boxed{\left(\frac{\partial H}{\partial p}\right)_T=-T\left(\frac{\partial V}{\partial T}\right)_p+V}
$$

上式即可求出焓对压强的依赖关系，易得理想气体焓与p无关。

**上述方法也可选择S(V,p)进行，由此得到U和H关于p和V变量的偏导关系。再次利用麦氏关系可以得到绝热过程的微分方程。**

**★** 根据以上导出的热容偏导式，不难求出上一章导出的$C_p-C_V$表达式：

$$
C_p-C_V=T\left(\frac{\partial S}{\partial T}\right)_p-T\left(\frac{\partial S}{\partial T}\right)_V
$$

利用链式法则对S(T,V(T,p))进行偏导(对S(T,p(T,V))偏导效果一样)：

$$
\left(\frac{\partial S}{\partial T}\right)_p=\left(\frac{\partial S}{\partial T}\right)_V+\left(\frac{\partial S}{\partial V}\right)_T\left(\frac{\partial V}{\partial T}\right)_p
$$

代入，并利用麦氏关系得到：

$$
\boxed{C_p-C_V}=T\left(\frac{\partial S}{\partial V}\right)_T\left(\frac{\partial V}{\partial T}\right)_p=\boxed{T\left(\frac{\partial p}{\partial T}\right)_V\left(\frac{\partial V}{\partial T}\right)_p}
$$

在实际测量中，容易得到的是$\alpha$和$\kappa_T$,因而上式可改写为：

$$
\left(\frac{\partial p}{\partial V}\right)_T \left(\frac{\partial V}{\partial T}\right)_p \left(\frac{\partial T}{\partial p}\right)_V=-1\Rightarrow
\left(\frac{\partial p}{\partial T}\right)_V=\frac{\alpha}{\kappa_T}
$$

$$
\boxed{C_p-C_V=\frac{TV\alpha^2}{\kappa_T}}
$$

**★** 对于复杂偏导的拼凑，常常用到雅可比行列式的性质进行变换：

$$
\left(\frac{\partial u}{\partial x}\right)_y=\frac{\partial(u,y)}{\partial(x,y)}=-\frac{\partial(y,u)}{\partial(x,y)}=\frac{\partial(u,y)\partial(r,s)}{\partial(r,s)\partial(x,y)}=\frac{1}{\frac{\partial(x,y)}{\partial(u,y)}}
$$

练习用以上性质证明：$\frac{\kappa_S}{\kappa_T}=\frac{C_V}{C_p}$和$C_p-C_V=\frac{TV\alpha^2}{\kappa_T}$

利用雅可比行列式，也可将麦氏关系重新表达：

$$
\left(\frac{\partial T}{\partial V}\right)_S=-\left(\frac{\partial p}{\partial S}\right)_V=\frac{\partial(T,S)}{\partial(V,S)}=-\frac{\partial(p,V)}{\partial(S,V)}\Rightarrow\boxed{\frac{\partial(p,V)}{\partial(T,S)}=\frac{\partial(x,y)}{\partial(x,y)}=1}
$$

其中x，y可以在(p,V)和(T,S)中任选一个，总共有四种组合，即麦氏关系。

**★** 最后，利用麦氏关系可以导出$C_V$和$C_p$在不同体积和压强下的变化：

$$
\boxed{\left(\frac{\partial C_V}{\partial V}\right)_T}=T\left[\frac{\partial }{\partial V}\left(\frac{\partial S}{\partial T}\right)_V\right]_T=T\left[\frac{\partial }{\partial T}\left(\frac{\partial S}{\partial V}\right)_T\right]_V=\boxed{T\left(\frac{\partial^2 p}{\partial T^2}\right)_V}
$$

$$
\boxed{\left(\frac{\partial C_p}{\partial p}\right)_T}=T\left[\frac{\partial }{\partial p}\left(\frac{\partial S}{\partial T}\right)_p\right]_T=T\left[\frac{\partial }{\partial T}\left(\frac{\partial S}{\partial p}\right)_T\right]_p=\boxed{-T\left(\frac{\partial^2 V}{\partial T^2}\right)_p}
$$

从而只要知道某一体积或压强下的热容，根据物态方程就可以求得任意体积或压强下的热容。
