from binance.client import Client
import time

client = Client()

# 定义币种及其分类
classifications = {
    '第一级别': ['DOGEUSDT', 'NEARUSDT', 'DEGOUSDT'],
    '第二级别': ['ANKRUSDT', 'ARDRUSDT', 'CHRUSDT', 'COTIUSDT', 'CTSIUSDT', 'FUNUSDT', 'KAVAUSDT', 'KEYUSDT', 'LTOUSDT', 'NKNUSDT', 'RVNUSDT', 'VITEUSDT', 'WRXUSDT'],
    '第三级别': ['BLZUSDT', 'BNTUSDT', 'DEXEUSDT', 'LINAUSDT', 'SFPUSDT', 'YFIUSDT'],
    '第四级别': ['ATOMUSDT', 'AVAUSDT', 'AXSUSDT', 'FARMUSDT', 'LUNAUSDT', 'MLNUSDT', 'ROSEUSDT', 'SCUSDT']
}

# 初始化价格数据结构
price_data = {}
for classification, symbols in classifications.items():
    for symbol in symbols:
        if symbol not in price_data:
            price_data[symbol] = {"classification": classification, "initial": 0, "highest_gain": 0, "current_gain": 0}

def initialize_prices():
    """初始化所有币种的价格和涨幅信息"""
    for symbol in price_data.keys():
        current_price = float(client.get_symbol_ticker(symbol=symbol)["price"])
        price_data[symbol]["initial"] = current_price

def monitor_price_changes():
    """监控价格变化并记录最高涨幅和当前涨幅"""
    while True:
        for symbol in price_data.keys():
            current_price = float(client.get_symbol_ticker(symbol=symbol)["price"])
            initial_price = price_data[symbol]["initial"]
            current_gain = ((current_price - initial_price) / initial_price) * 100
            price_data[symbol]["current_gain"] = current_gain
            if current_gain > price_data[symbol]["highest_gain"]:
                price_data[symbol]["highest_gain"] = current_gain
        
        # 每小时输出所有币种的最高涨幅和当前涨幅，按分类组织
        print("Current and Highest Gains for Each Symbol by Classification:")
        for classification in classifications.keys():
            print(f"\n{classification}:")
            for symbol in classifications[classification]:
                print(f"{symbol}: Current Gain: {price_data[symbol]['current_gain']:.2f}%, Highest Gain: {price_data[symbol]['highest_gain']:.2f}%")
        
        time.sleep(3600)  # 暂停60分钟

initialize_prices()
monitor_price_changes()
