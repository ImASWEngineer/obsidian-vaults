---
title: Position Sizing
tags: #risk_management #trading_fundamentals
last_updated: 2023-10-27
---

# Position Sizing

Position sizing is the process of determining the appropriate number of shares or contracts to trade for a particular setup. It is a critical component of [[risk-management]] that directly controls how much capital is exposed to loss on any single trade.

## Importance

- **Controls Risk**: Ensures that a single losing trade does not significantly impact the overall account balance.
- **Enables Consistency**: By using a consistent method for sizing positions, a trader can better analyze their performance over time.
- **Prevents Over-Leveraging**: Stops a trader from taking on too much risk, especially in volatile markets.

## Calculation Flow

The core idea is to size your position based on your predefined [[risk-per-trade]] and the distance to your [[stop-loss]].

```mermaid
graph TD
    A[Account Size] --> C{Risk per Trade ($)};
    B[Risk per Trade (%)] --> C;
    C -- "Max $ to Risk" --> E(Calculate # of Shares);
    D[Distance to Stop-Loss ($)] -- "Risk per Share" --> E;

    subgraph "Inputs"
        A
        B
        D
    end

    subgraph "Calculation"
        C
        E
    end

    C(Risk $) = A * B;
    E(Shares) = C / D;

    style A fill:#lightblue
    style B fill:#lightblue
    style D fill:#lightblue
```

### Example
- **Account Size**: $25,000
- **Risk per Trade (%)**: 1%
- **Max $ to Risk**: $25,000 * 0.01 = $250
- **Entry Price**: $50.00
- **Stop-Loss Price**: $49.50
- **Distance to Stop-Loss ($)**: $50.00 - $49.50 = $0.50
- **Number of Shares**: $250 / $0.50 = 500 shares

## Source Reference
-   **Book**: [[ross-cameron-how-to-day-trade|Ross Cameron's How to Day Trade]]
-   **Concept**: Position Sizing (Chapter 2)