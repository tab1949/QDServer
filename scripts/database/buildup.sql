-- Attention: This SQL script is designed for ClickHouse.

CREATE DATABASE IF NOT EXISTS Futures;

USE Futures;

-- This table stores metadata information about futures contracts.
CREATE TABLE IF NOT EXISTS Contracts (
    `code`        LowCardinality(String),
    `exchange`    LowCardinality(String),
    `name`        LowCardinality(String),
    `unit`        LowCardinality(String),
    `quotation_unit`      LowCardinality(String),
    `minimum_variation`   Decimal32(3),
    `minimum_margin_rate` UInt8,
    `limit_band_rate`     UInt8,
    `last_trading_day`    Date,
    `delivery_day`        Date,
    `list_date`           Date,
    `object`      LowCardinality(String) MATERIALIZED substring(`code`, 1, 2),
)
ENGINE = ReplacingMergeTree
PARTITION BY `object`
ORDER BY `code`;

-- This table stores trading calendar information for different exchanges.
CREATE TABLE IF NOT EXISTS TradingCalendar (
    `exchange`    LowCardinality(String),
    `date`        Date,
    `is_open`     UInt8,
    `pre_trading_day` Date
) 
ENGINE = ReplacingMergeTree
PARTITION BY `exchange`
ORDER BY (`date`, `exchange`);

-- This table stores original tick (0.5s snapshot) data (cleaned by ETL process).
CREATE TABLE IF NOT EXISTS HistoryTick (
    `datetime`    DateTime,
    `millisecond` UInt16,
    `symbol`      LowCardinality(String),
    `last_price`  Decimal64(3),
    `volume`      UInt64,
    `turnover`    Decimal64(3),
    `open_interest`   UInt64,
    `average`     Decimal64(3),
    `bid1_price`  Decimal64(3),
    `bid1_volume` UInt64,
    `ask1_price`  Decimal64(3),
    `ask1_volume` UInt64,
    `upper_limit` Decimal64(3),
    `lower_limit` Decimal64(3),
    `object`      LowCardinality(String) MATERIALIZED substring(`symbol`, 1, 2)
)
ENGINE = ReplacingMergeTree
PARTITION BY toYYYYMM(`datetime`)
ORDER BY (`datetime`, `millisecond`, `symbol`);

-- This table stores aggregated 1-minute-level data derived from tick data.
-- Note: Considering complexity of aggregation logic, 
--       we use a TABLE but not a MATERIALIZED VIEW.
-- Note: This table should be populated by an external ETL process.
CREATE TABLE IF NOT EXISTS HistoryMinute (
    `datetime`     DateTime,
    `symbol`       LowCardinality(String),
    `volume`       UInt64,
    `turnover`     Decimal64(3),
    `open_interest` UInt64,
    `open`         Decimal64(3),
    `close`        Decimal64(3),
    `high`         Decimal64(3),
    `low`          Decimal64(3),
    `upper_limit`  Decimal64(3),
    `lower_limit`  Decimal64(3)
)
ENGINE = ReplacingMergeTree
PARTITION BY toYYYYMM(`datetime`)
ORDER BY (`datetime`, `symbol`);

-- This table stores daily ranking data of brokers for each futures contract.
CREATE TABLE IF NOT EXISTS DailyRank (
    `trading_day`       Date,
    `symbol`            String,
    `broker_name`       String,
    `volume`            UInt64,
    `volume_variation`  Int64,
    `long_position`     UInt64,
    `long_variation`    Int64,
    `short_position`    UInt64,
    `short_variation`   Int64,
    `code` String MATERIALIZED replaceRegexpAll(`symbol`, '[0-9]', '')
)
ENGINE = ReplacingMergeTree
PARTITION BY (`code`)
ORDER BY (`trading_day`, `symbol`, `broker_name`);

-- This table stores metadata information about options contracts.
CREATE TABLE IF NOT EXISTS OptionsList (
    `code`        LowCardinality(String),
    `exchange`    LowCardinality(String),
    `name`        LowCardinality(String),
    `asset`       LowCardinality(String),
    `quotation_unit`      LowCardinality(String),
    `minimum_variation`   Decimal64(3),
    `option_type` FixedString(1), -- 'C' for Call, 'P' for Put
    `exercise_price`   Decimal64(3),
    `last_trading_day` Date,
    `list_date`   Date
)
ENGINE = ReplacingMergeTree
PARTITION BY `exchange`
ORDER BY (`exchange`, `code`);

-- This table stores history tick data (0.5s snapshot) for options contracts.
CREATE TABLE IF NOT EXISTS OptionsTick (
    `datetime`    DateTime,
    `millisecond` UInt16,
    `symbol`      LowCardinality(String),
    `last_price`  Decimal64(3),
    `volume`      UInt64,
    `turnover`    Decimal64(3),
    `open_interest`   UInt64,
    `bid1_price`  Decimal64(3),
    `bid1_volume` UInt64,
    `ask1_price`  Decimal64(3),
    `ask1_volume` UInt64,
    `contract`    LowCardinality(String) MATERIALIZED upper(replaceRegexpAll(replaceAll(`symbol`, '-', ''), '([cCpP][0-9]+)$', '')),
    `direction`   FixedString(1) MATERIALIZED upper(substring(replaceAll(`symbol`, '-', ''), length(`contract`) + 1, 1)),
    `act_price`   Decimal64(3) MATERIALIZED toDecimal64(substring(replaceAll(`symbol`, '-', ''), length(`contract`) + 2, length(`symbol`) - length(`contract`) - 1), 3)
)
ENGINE = ReplacingMergeTree
PARTITION BY toYYYYMM(`datetime`)
ORDER BY (`datetime`, `millisecond`, `symbol`);