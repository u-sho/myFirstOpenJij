# 004 Evaluation

<https://openjij.github.io/OpenJij/tutorial/ja/004-Evaluation.html>

> TTS (Time To Solution) is the computation time it takes to obtain an optimal solution with a certain probability, and this is often used in various evaluations. Success probability is the probability that the optimal solution was obtained. Residual energy is an average value that indicates how close the obtained solution was to the optimal solution.

## Time to solution (TTS)

> 例えば短い計算時間$τ_{\textit{short}}$で最適解を出す確率が低くても、その計算時間$τ_\textit{short}$で複数回アニーリングをした方が、より長い計算時間$τ_\textit{long}$を1回行うよりも計算時間が短くて済むかもしれません。なので計算時間を考慮するには単純にアニーリング時間を比較するだけでは不十分なことがあります。

1回のアニーリングで最適解が算出される確率を$p_s(τ)$とすると、$R$回のアニーリングで最適解を得る確率$p_R$は以下のように求まります。
$$
  p_R = 1-\left\{1-p_s(τ)\right\}^R
$$
この式を$R$について解くと、
$$
  R = \frac{\ln(1-p_R)}{\ln(1-p_s(τ))}
$$
となります。したがって、1回のアニーリングで$τ$の計算時間をかけて確率$p_s(τ)$で最適解となるアルゴリズムが、確率$p_R$で最適解を得るのにかかる総計算時間$\textrm{TTS}$は
$$
  \textrm{TTS}(τ,p_R) = τR = τ \frac{\ln(1-p_R)}{\ln(1-p_s(τ))}
$$
と表せます。

## 成功確率

$p_s$には経験確率を用います。（たぶん）

## 残留エネルギー

時間ではなく、最適解$E_\textrm{min}$と得られた値の平均$E$との「比」を評価指標とすることもできます。
これを**近似比**といい、以下のように計算できます。
$$
  r = \langle E \rangle / E_\textrm{min}
$$
また、物理では**残留エネルギー**という平均エネルギーとの「差」を評価指標として用いることもあります。
$$
  E_\textrm{res} = \langle E \rangle - E_\textrm{min}
$$

アニーリングアルゴリズムは最適解へ漸近収束するため、（ほとんどの場合は）アニーリング時間を長くすれば残留エネルギーは減少します。


