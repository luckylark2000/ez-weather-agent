# 彩云天气 API 集成指南

## 概述

ez-weather-agent 现在支持真实的彩云天气 API，可以获取详细的天气数据，包括：

- 实时天气
- 时间分辨率：72小时预报
- 每日预报：7天
- 历史天气数据
- 天气警报
- 空气质量指数（AQI）
- 生活指数（紫外线、舒适度等）

## 获取 API Token

### 步骤 1：访问彩云天气官网

访问 [彩云天气官网](https://www.caiyunapp.com/)

### 步骤 2：注册账户

- 点击"注册"创建新账户
- 填写必要的信息（邮箱、密码等）
- 验证邮箱

### 步骤 3：获取 API Token

- 登录账户
- 进入"开发者"或"API"页面
- 创建新的应用程序
- 复制你的 API Token

### 步骤 4：配置 .env 文件

将 API Token 添加到你的 `.env` 文件：

```bash
DEEPSEEK_API_KEY=your_deepseek_api_key
CAIYUN_WEATHER_API_TOKEN=your_caiyun_api_token
```

## 支持的城市位置

当前支持以下城市（可以轻松扩展）：

**中国城市：**
- Beijing（北京）
- Shanghai（上海）
- Guangzhou（广州）
- Shenzhen（深圳）
- Chengdu（成都）
- Hangzhou（杭州）
- Suzhou（苏州）
- Wuhan（武汉）
- Xi'an（西安）
- Chongqing（重庆）

**国际城市：**
- London（伦敦）
- New York（纽约）
- Tokyo（东京）
- Paris（巴黎）
- Sydney（悉尼）

## 天气代理功能

### 实时天气查询

```python
from weather_agent import run_weather_agent

response = run_weather_agent("What's the weather in Beijing?")
print(response)
```

返回信息包括：
- 当前温度
- 湿度
- 风速和风向
- 降水概率
- 空气质量（PM2.5, PM10, AQI等）
- 生活指数（UV、舒适度）

### 时间预报

```python
response = run_weather_agent("Get hourly forecast for Shanghai")
```

提供未来72小时的时间分辨率预报

### 每日预报

```python
response = run_weather_agent("7-day forecast for Suzhou")
```

提供7天的每日预报（最高/最低温、天气状况、降水概率）

## 架构

```
┌─────────────────────────────────────┐
│   User Query (Natural Language)     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   DeepSeek AI (LangGraph Agent)     │
│   - 理解自然语言                      │
│   - 选择合适的工具                    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Weather Tools                     │
│   - get_realtime_weather()          │
│   - get_hourly_forecast()           │
│   - get_daily_forecast()            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Caiyun Weather API                │
│   - /realtime (实时天气)            │
│   - /hourly (小时预报)              │
│   - /daily (每日预报)               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Formatted Response                │
└─────────────────────────────────────┘
```

## 关键特性

1. **LangGraph 代理框架** - 使用图形化的代理架构
2. **工具调用** - DeepSeek 自动选择合适的天气工具
3. **坐标映射** - 自动将城市名称转换为地理坐标
4. **详细数据** - 获取包括AQI、生活指数等详细信息
5. **错误处理** - 优雅地处理API错误和不支持的城市

## 添加新城市

要添加新城市，只需在 `weather_agent.py` 中的 `CITY_COORDINATES` 字典中添加坐标：

```python
CITY_COORDINATES = {
    ...
    "your_city": (longitude, latitude),  # 经度, 纬度
}
```

你可以在 [Google Maps](https://maps.google.com/) 或其他地图服务中找到坐标。

## 成本和限制

- 彩云天气提供免费API额度
- 查看官方文档了解请求速率限制
- 根据付费计划，提供更高的API调用限制

## 故障排除

### 提示 "CAIYUN_WEATHER_API_TOKEN is not set"

确保在 `.env` 文件中设置了 token：
```bash
CAIYUN_WEATHER_API_TOKEN=your_actual_token
```

### 提示 "Location not found"

当前支持的城市列表有限。你可以：
1. 在 `CITY_COORDINATES` 中添加新城市
2. 或使用现有支持的城市名称

### 网络错误或超时

- 检查网络连接
- 验证 API Token 有效性
- 查看彩云天气 API 状态页面

## 下一步

1. 测试集成：`python test_caiyun.py`
2. 运行交互式应用：`python main.py`
3. 扩展城市支持列表
4. 自定义响应格式
