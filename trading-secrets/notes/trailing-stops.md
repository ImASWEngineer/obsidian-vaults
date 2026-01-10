---
title: Trailing Stops
tags: #trading_strategy #risk_management #exit_strategy
last_updated: 2023-10-27
---

# Trailing Stops

A trailing stop is a dynamic type of [[stop-loss]] order that automatically adjusts as the price of an asset moves in the trader's favor. It is designed to protect profits by allowing a trade to continue gaining as long as the price is moving favorably, but automatically closing the position if the price reverses by a specified amount.

## How it Works

Instead of a fixed price, a trailing stop is set at a specific percentage or dollar amount below the market price (for long positions) or above the market price (for short positions). As the price moves, the stop price moves with it, maintaining the set distance. If the price reverses and falls (or rises for shorts) by the specified amount, the trailing stop is triggered, and the position is closed.

## Benefits

-   **Profit Protection**: Locks in a portion of profits while allowing for further gains.
-   **Risk Management**: Limits potential losses if the market reverses.
-   **Flexibility**: Adapts to market movements without constant manual adjustment.

## Considerations

-   **Volatility**: Setting the trailing stop too tight in a volatile market can lead to premature exits.
-   **Gap Risk**: Like fixed stop-losses, trailing stops may not execute at the exact desired price if the market gaps.

Trailing stops are a valuable tool for managing [[drawdowns]] and optimizing profit realization within a [[trading-plan]].