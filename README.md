# QQ-Bridge-SL

Snowluma平替，桥接 QQ 与 DSH。

## 当前实现

提供最小可用的桥接核心 `qq_dsh_bridge.py`：

- QQ 事件 -> 统一消息对象 -> DSH 载荷
- DSH 事件 -> 统一消息对象 -> QQ 发送载荷

适用于后续接入 OneBot/QQ 机器人和 DSH 的具体网络层。

## 运行测试

```bash
python -m unittest discover -s tests -p 'test_*.py'
```
