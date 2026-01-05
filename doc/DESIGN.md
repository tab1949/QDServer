# Designing of QuantDirect Data Server
This file describes the details about the designing of QuantDirect Data Server

## Framework
```
+--------+                 +-------+
| Client | <--- HTTPS ---> | Nginx |
+--------+                 +-------+
                               ^
                              HTTP
                               |
                        +------------+
                        | API Server |
                        +------------+

+------------+            +------------+
| API Server | <---+----> | Clickhouse |
+------------+     |      | (Core DB)  |
                   |      +------------+
                   |           
                   |      +------------+
                   +----> | Redis      |
                          | (Cache DB) |
                          +------------+

```