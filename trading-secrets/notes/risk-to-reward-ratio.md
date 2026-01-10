---
title: Risk-to-Reward Ratio
tags: #risk_management #trading_plan #metrics
last_updated: 2023-10-27
---

# Risk-to-Reward Ratio

The Risk-to-Reward Ratio (R:R) is a crucial metric in [[risk-management]] that compares the potential profit of a trade to its potential loss. It helps traders assess the attractiveness of a trade setup and ensures that potential gains outweigh potential risks.

## Calculation

The ratio is calculated by dividing the potential profit (distance from entry to [[profit-targets]]) by the potential loss (distance from entry to [[stop-loss]]).

$$ \text{Risk-to-Reward Ratio} = \frac{\text{Potential Gain}}{\text{Potential Loss}} $$

For example, if a trader risks $100 to potentially make $300, the R:R is 3:1 (or simply 3).

## Visual Representation (Mermaid)

```mermaid
graph LR
    SL[Stop Loss] --- Entry[Entry Price]
    Entry --- TP[Take Profit]

    subgraph Potential Loss (Risk)
        Entry -- "Distance" --> R_Calc(Entry - SL)
    end

    subgraph Potential Gain (Reward)
        TP -- "Distance" --> G_Calc(TP - Entry)
    end

    R_Calc --> RR_Ratio{Risk-to-Reward Ratio};
    G_Calc --> RR_Ratio;

    style R_Calc fill:#FFDDDD,stroke:#FF0000,stroke-width:2px
    style G_Calc fill:#DDFFDD,stroke:#00FF00,stroke-width:2px
```

## Importance

-   **Capital Preservation**: Encourages traders to take trades where the potential reward significantly outweighs the risk, protecting capital over the long run.
-   **Consistency**: A favorable R:R allows a trader to be profitable even with a win rate below 50%. For instance, with a 1:2 R:R, a 35% win rate can still lead to profitability.
-   **Discipline**: Forces traders to define their [[stop-loss]] and [[profit-targets]] before entering a trade, which is a key aspect of a disciplined [[trading-plan]].

## Source Reference
-   **Book**: [[ross-cameron-secrets|Ross Cameron's Trading Secrets]]
-   **Concept**: Risk Management (Chapter 2)