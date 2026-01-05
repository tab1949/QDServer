# QuantDirect Data Server TODO List
Here listed pending tasks. For detailed interface description, see [API.md](./API.md).

## 1. Database System
- [ ] Build Database System
  - [x] Table Structure Design
- [ ] Data Cleaning / Importing / Exporting Tools
  - [ ] Import Scripts
  - [ ] Export Scripts
- [ ] Containerization

## 1-1. Database Building & Importing Scripts
The database building script describes the database structure;  
The data importing scripts should be able to import initial data and incremental data.

### 1-1-1. Futures
- [ ] Trading Calendar
  - [x] Import
  - [ ] Export 
- [ ] Contract Information
- [ ] History Tick
- [ ] History Minute
- [ ] History Day
- [ ] Daily Rank

### 1-1-2. Options
- [ ] Options List
  - [ ] Im  
- [x] History Tick
  - [x] Import
  - [x] Export (CSV, By Contracts)
- [ ] History Minute
- [ ] History Day

### 1-1-3. Stocks
- Pending
  
## 1-2. RESTful API

### 1-2-1. Futures Query:
- [ ] Contract Information (**Single** / **Combination**)
- [ ] Trading Calendar (**Period**)
- [ ] History Market Data (**Period**: 0.5s / 1s / 1min / 1h / 1d) (**Duration**)
- [ ] History Broker Position (**Duration** / **Single Day**)
- [ ] History Warehouse Data (**Duration** / **Single Day**)
- [ ] History Spot Commodity (**All** / **Region**) (**Duration** / **Single Day**)

### 1-2-2. Options (Futures Options)
- [ ] Option Information (**Single** / **Combination**)
- [ ] History Market Data (**Period**: 1min / 1h / 1d) (**Duration**)

### 1-2-3. Stocks (Chinese A-Share / Hong Kong / American)
- [ ] Basic Information
- [ ] History Market Data (**Period**: 1min / 1day) (**Duration**)
- [ ] Financial Statement

## 1-3. Containerization