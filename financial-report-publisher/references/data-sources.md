# 数据源集成指南

本文档介绍如何为金融行情简报集成实时数据源。

## 数据获取方案

### 方案1：公开API（推荐）

#### 东方财富API

**优点：**
- 数据全面（A股、港股、美股、期货）
- 更新及时
- 免费使用

**示例代码：**

```python
import requests

def get_stock_data():
    """获取A股实时数据"""
    url = "http://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "secid": "1.000001",  # 上证指数
        "fields": "f43,f44,f45,f46,f47,f48,f49,f50,f51,f52"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['data']

def get_sector_ranking():
    """获取板块涨跌幅排名"""
    url = "http://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "10",
        "po": "1",
        "np": "1",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:90+t:2",
        "fields": "f12,f14,f2,f3,f62"
    }
    response = requests.get(url, params=params)
    return response.json()['data']['diff']
```

#### 新浪财经API

**优点：**
- 接口稳定
- 支持多市场
- 无需认证

**示例代码：**

```python
def get_sina_stock_data(symbol):
    """
    获取股票实时数据
    symbol: sh000001(上证), sz399001(深证), sz399006(创业板)
    """
    url = f"http://hq.sinajs.cn/list={symbol}"
    response = requests.get(url)
    data = response.text.split(',')
    return {
        'name': data[0].split('=')[1].strip('"'),
        'price': float(data[3]),
        'change': float(data[3]) - float(data[2]),
        'change_pct': ((float(data[3]) - float(data[2])) / float(data[2])) * 100
    }
```

### 方案2：网络爬取

使用BeautifulSoup或Selenium爬取公开网站数据。

**注意事项：**
- 遵守robots.txt
- 控制请求频率
- 处理反爬机制

**示例代码：**

```python
from bs4 import BeautifulSoup
import requests

def scrape_market_data():
    """爬取东方财富网行情数据"""
    url = "http://quote.eastmoney.com/center/gridlist.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 解析数据...
    return data
```

### 方案3：付费数据服务

#### Tushare Pro

**优点：**
- 数据质量高
- 接口规范
- 支持历史数据

**注册：** https://tushare.pro/register

**示例代码：**

```python
import tushare as ts

# 设置token
ts.set_token('YOUR_TOKEN')
pro = ts.pro_api()

def get_daily_basic():
    """获取每日指标"""
    df = pro.daily_basic(
        trade_date='20260213',
        fields='ts_code,close,turnover_rate,volume_ratio,pe,pb'
    )
    return df

def get_index_daily():
    """获取指数日线行情"""
    df = pro.index_daily(
        ts_code='000001.SH',
        start_date='20260213',
        end_date='20260213'
    )
    return df
```

#### Wind API

**优点：**
- 专业金融数据
- 覆盖全面
- 机构级服务

**费用：** 需要购买许可

## 集成到简报系统

### 修改主程序

在 `market_report_publisher.py` 中添加数据获取模块：

```python
class MarketReportPublisher:
    
    def fetch_market_data(self):
        """获取实时市场数据"""
        try:
            # A股数据
            sh_index = self.get_stock_data('sh000001')
            sz_index = self.get_stock_data('sz399001')
            cy_index = self.get_stock_data('sz399006')
            
            # 板块数据
            top_sectors = self.get_sector_ranking(sort='up', limit=4)
            bottom_sectors = self.get_sector_ranking(sort='down', limit=4)
            
            # 美股数据（需要其他API）
            us_stocks = self.get_us_market_data()
            
            # 期货数据
            futures = self.get_futures_data()
            
            return {
                'a_stock': {
                    'sh': sh_index,
                    'sz': sz_index,
                    'cy': cy_index
                },
                'sectors': {
                    'top': top_sectors,
                    'bottom': bottom_sectors
                },
                'us_stock': us_stocks,
                'futures': futures
            }
        except Exception as e:
            print(f"数据获取失败: {e}")
            return None
    
    def generate_market_report(self):
        """生成行情简报（使用实时数据）"""
        # 获取实时数据
        data = self.fetch_market_data()
        
        if not data:
            print("使用默认数据生成简报")
            return self._generate_default_report()
        
        # 使用实时数据生成简报
        today = datetime.now().strftime("%Y年%m月%d日")
        
        report = f"""<h2>📊 {today} 金融市场收盘简报</h2>

<h3>🇨🇳 A股市场</h3>
<p><strong>主要指数：</strong></p>
<ul>
<li>上证指数：{data['a_stock']['sh']['price']:.2f}点，
    {'+' if data['a_stock']['sh']['change'] > 0 else ''}{data['a_stock']['sh']['change_pct']:.2f}%</li>
<li>深证成指：{data['a_stock']['sz']['price']:.2f}点，
    {'+' if data['a_stock']['sz']['change'] > 0 else ''}{data['a_stock']['sz']['change_pct']:.2f}%</li>
<li>创业板指：{data['a_stock']['cy']['price']:.2f}点，
    {'+' if data['a_stock']['cy']['change'] > 0 else ''}{data['a_stock']['cy']['change_pct']:.2f}%</li>
</ul>

<p><strong>领涨板块：</strong></p>
<ul>
"""
        
        for sector in data['sectors']['top']:
            report += f"<li>{sector['name']}：涨{sector['change_pct']:.2f}%</li>\n"
        
        report += """</ul>

<p><strong>领跌板块：</strong></p>
<ul>
"""
        
        for sector in data['sectors']['bottom']:
            report += f"<li>{sector['name']}：跌{abs(sector['change_pct']):.2f}%</li>\n"
        
        report += """</ul>
"""
        
        # 添加美股和期货数据...
        
        return report
```

### 错误处理

```python
def safe_fetch_data(self, fetch_func, default_value=None):
    """安全的数据获取包装器"""
    try:
        return fetch_func()
    except requests.RequestException as e:
        print(f"网络请求失败: {e}")
        return default_value
    except Exception as e:
        print(f"数据处理失败: {e}")
        return default_value
```

### 数据缓存

```python
import json
from datetime import datetime, timedelta

class DataCache:
    def __init__(self, cache_file='data_cache.json'):
        self.cache_file = cache_file
    
    def get(self, key):
        """获取缓存数据"""
        try:
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
            
            if key in cache:
                data = cache[key]
                # 检查是否过期（5分钟）
                cache_time = datetime.fromisoformat(data['timestamp'])
                if datetime.now() - cache_time < timedelta(minutes=5):
                    return data['value']
        except:
            pass
        return None
    
    def set(self, key, value):
        """设置缓存数据"""
        try:
            cache = {}
            try:
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
            except:
                pass
            
            cache[key] = {
                'value': value,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f)
        except Exception as e:
            print(f"缓存写入失败: {e}")
```

## 数据验证

```python
def validate_market_data(data):
    """验证市场数据的合理性"""
    checks = []
    
    # 检查涨跌幅是否在合理范围
    if abs(data['change_pct']) > 20:
        checks.append(f"异常涨跌幅: {data['change_pct']}%")
    
    # 检查价格是否为正数
    if data['price'] <= 0:
        checks.append(f"异常价格: {data['price']}")
    
    # 检查成交量
    if data.get('volume', 0) == 0:
        checks.append("成交量为0")
    
    return len(checks) == 0, checks
```

## 最佳实践

1. **请求频率控制** - 避免频繁请求，使用缓存
2. **异常处理** - 网络请求必须有超时和重试机制
3. **数据验证** - 检查数据合理性，避免异常值
4. **降级策略** - API失败时使用备用数据源或默认数据
5. **日志记录** - 记录数据获取过程，便于排查问题

## 示例：完整集成

```python
class EnhancedMarketReportPublisher(MarketReportPublisher):
    def __init__(self, config_path='config.json'):
        super().__init__(config_path)
        self.cache = DataCache()
    
    def get_stock_data_with_cache(self, symbol):
        """带缓存的股票数据获取"""
        # 尝试从缓存获取
        cached = self.cache.get(f'stock_{symbol}')
        if cached:
            return cached
        
        # 从API获取
        data = self.safe_fetch_data(
            lambda: get_stock_data(symbol),
            default_value={'price': 0, 'change_pct': 0}
        )
        
        # 验证数据
        is_valid, errors = validate_market_data(data)
        if not is_valid:
            print(f"数据验证失败: {errors}")
            return None
        
        # 缓存数据
        self.cache.set(f'stock_{symbol}', data)
        return data
```

## 相关资源

- 东方财富API文档：http://quote.eastmoney.com/center/api.html
- Tushare文档：https://tushare.pro/document/2
- 新浪财经接口说明：https://blog.csdn.net/
- Yahoo Finance API：https://pypi.org/project/yfinance/
