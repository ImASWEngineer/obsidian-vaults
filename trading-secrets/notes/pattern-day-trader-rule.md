---
title: Pattern Day Trader (PDT) Rule
date: 2025-06-24
tags: #regulation #risk-management #trading-rules
---

## Summary
This note explains the [[pattern-day-trader-rule]], a key regulation from the Securities and Exchange Commission (SEC) that affects traders with smaller account balances.

## The Rule
- **Definition**: A trader is designated a "Pattern Day Trader" if they make four or more day trades (buying and selling the same security on the same day) within a five-business-day period in a margin account.
- **Requirement**: Once designated, a trader must maintain a minimum account balance of $25,000 to continue day trading.
- **Consequence**: If the account value drops below $25,000, day trading is restricted until the balance is restored.
- **Impact**: This rule was a significant hurdle in [[ross-camerons-trading-journey]] and is a primary reason traders use offshore brokers for small account challenges.

## Related Notes
- [[risk-management-MOC]]
- [[583-to-10-million-challenge]]

## Understanding the PDT Rule
```mermaid
graph TD
    A[Trader Makes 4+ Day Trades] --> B{Within 5 Business Days};
    B --> C{In a Margin Account};
    C --> D[Designated "Pattern Day Trader"];
    D --> E{Must Maintain $25,000 Equity};
    E -- "If Below $25k" --> F[Day Trading Restricted];
    E -- "If Above $25k" --> G[Can Continue Day Trading];
    style F fill:#f99,stroke:#333,stroke-width:2px
    style D fill:#add8e6,stroke:#333,stroke-width:2px
```