---
title: Stop-Loss
tags: #risk_management #trading_fundamentals #orders
last_updated: 2023-10-27
---

# Stop-Loss

A stop-loss is an order placed with a broker to buy or sell a security once it reaches a certain price. It is designed to limit a trader's loss on a security position. Setting a stop-loss is a fundamental and non-negotiable part of [[risk-management]].

## Purpose

- **Limits Losses**: Automatically closes a losing trade at a predetermined price, preventing catastrophic losses.
- **Removes Emotion**: Takes the decision to exit a losing trade out of the trader's hands, preventing hope from turning a small loss into a large one.
- **Defines Risk**: A stop-loss is essential for calculating [[risk-per-trade]] and [[position-sizing]].

## Visual Representation (ASCII)

For a long (buy) trade, the stop-loss is placed below the entry price.

```
      /
     /
    /  <-- Price rises (Profit)
   /
  E-----------  <-- Entry Price
  |
  |
  SL----------  <-- Stop-Loss Price (Loss is limited if price falls here)
```

## Types of Stop-Loss Orders

- **Price-Based**: Set at a specific price level, often based on [[support-and-resistance]] or a recent low/high.
- **Percentage-Based**: Set a certain percentage away from the entry price.
- **Volatility-Based**: Uses indicators like Average True Range (ATR) to set a stop based on the stock's typical price movement.
- **[[trailing-stops]]**: A dynamic stop that moves with the price to lock in profits.

## Source Reference
-   **Book**: [[ross-cameron-how-to-day-trade|Ross Cameron's How to Day Trade]]
-   **Concept**: Stop-Loss Strategies (Chapter 2)