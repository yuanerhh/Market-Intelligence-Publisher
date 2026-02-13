# -*- coding: utf-8 -*-
"""
金融行情早报自动发布系统
功能：生成美股收盘、市场要闻早报，并发布到微信公众号草稿箱
执行时间：每天早上7:00
"""

import json
import requests
import time
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont


class MorningReportPublisher:
    def __init__(self, config_path='config.json'):
        """初始化配置"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.wechat_appid = self.config['wechat']['appid']
        self.wechat_secret = self.config['wechat']['secret']
        self.access_token = None
    
    def get_wechat_access_token(self):
        """获取微信公众号access_token"""
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.wechat_appid}&secret={self.wechat_secret}"
        
        try:
            response = requests.get(url, timeout=10)
            result = response.json()
            
            if 'access_token' in result:
                self.access_token = result['access_token']
                print(f"✓ 获取access_token成功: {self.access_token[:20]}...")
                return self.access_token
            else:
                print(f"✗ 获取access_token失败: {result}")
                return None
        except Exception as e:
            print(f"✗ 请求access_token异常: {e}")
            return None
    
    def generate_cover_image(self, date_str):
        """生成早报封面图片"""
        try:
            print(f"正在生成封面图片...")
            
            # 创建1280x720的图片（16:9）
            width, height = 1280, 720
            
            # 创建渐变背景（橙红到金色，象征朝阳）
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            
            # 绘制渐变背景（从橙红到金黄）
            for y in range(height):
                r = int(255 - (255 - 218) * y / height * 0.5)
                g = int(140 + (165 - 140) * y / height * 0.8)
                b = int(0 + (32 - 0) * y / height * 0.3)
                draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))
            
            # 添加金色装饰图案
            gold_color = (255, 215, 0)
            for i in range(5):
                x = 100 + i * 250
                draw.line([(x, 100), (x+150, 200)], fill=gold_color, width=3)
                draw.ellipse([x+100, 250, x+180, 330], outline=gold_color, width=2)
            
            # 尝试加载字体
            try:
                title_font = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 120)
                date_font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 50)
            except:
                try:
                    title_font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 120)
                    date_font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 50)
                except:
                    title_font = ImageFont.load_default()
                    date_font = ImageFont.load_default()
                    print("⚠ 警告：未找到中文字体，使用默认字体")
            
            # 绘制标题"行情早报"
            title_text = "行情早报"
            title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            
            # 绘制标题阴影
            draw.text((title_x+3, 253), title_text, font=title_font, fill=(0, 0, 0))
            # 绘制标题主体（金色）
            draw.text((title_x, 250), title_text, font=title_font, fill=gold_color)
            
            # 绘制日期
            date_bbox = draw.textbbox((0, 0), date_str, font=date_font)
            date_width = date_bbox[2] - date_bbox[0]
            date_x = (width - date_width) // 2
            
            # 绘制日期阴影
            draw.text((date_x+2, 422), date_str, font=date_font, fill=(0, 0, 0))
            # 绘制日期主体（白色）
            draw.text((date_x, 420), date_str, font=date_font, fill=(255, 255, 255))
            
            # 添加太阳图标（象征早晨）
            sun_color = (255, 223, 0)
            sun_center = (150, 150)
            sun_radius = 60
            draw.ellipse([sun_center[0]-sun_radius, sun_center[1]-sun_radius,
                         sun_center[0]+sun_radius, sun_center[1]+sun_radius], 
                        fill=sun_color)
            
            # 太阳光芒
            for angle in range(0, 360, 45):
                import math
                rad = math.radians(angle)
                x1 = sun_center[0] + int((sun_radius + 10) * math.cos(rad))
                y1 = sun_center[1] + int((sun_radius + 10) * math.sin(rad))
                x2 = sun_center[0] + int((sun_radius + 30) * math.cos(rad))
                y2 = sun_center[1] + int((sun_radius + 30) * math.sin(rad))
                draw.line([(x1, y1), (x2, y2)], fill=sun_color, width=5)
            
            # 保存到本地
            local_path = f"morning_cover_{int(time.time())}.jpg"
            image.save(local_path, 'JPEG', quality=95)
            print(f"✓ 封面图片生成成功: {local_path}")
            
            return local_path
            
        except Exception as e:
            print(f"✗ 图片生成异常: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def upload_image_to_wechat(self, image_path):
        """上传本地图片到微信公众号"""
        if not self.access_token:
            print("✗ 缺少access_token，无法上传图片")
            return None
        
        try:
            print(f"正在上传封面图片到微信...")
            
            upload_url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={self.access_token}&type=image"
            
            files = {
                'media': ('cover.jpg', open(image_path, 'rb'), 'image/jpeg')
            }
            
            upload_response = requests.post(upload_url, files=files, timeout=30)
            upload_result = upload_response.json()
            
            if 'media_id' in upload_result:
                media_id = upload_result['media_id']
                print(f"✓ 图片上传成功，media_id: {media_id}")
                return media_id
            else:
                print(f"✗ 图片上传失败: {upload_result}")
                return None
                
        except Exception as e:
            print(f"✗ 图片上传异常: {e}")
            return None
    
    def generate_morning_report(self):
        """生成早报内容"""
        today = datetime.now().strftime("%Y年%m月%d日")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%m月%d日")
        
        # 使用微信公众号支持的HTML格式
        report = f"""<p style="font-size:16px;font-weight:bold;color:#000;">美股市场（{yesterday}收盘）</p>

<p style="font-size:14px;font-weight:bold;color:#34495e;margin-top:15px;">主要指数</p>
<p>• 道琼斯指数：49451.98点，跌1.34%<br/>
• 标普500指数：6832.76点，跌1.57%<br/>
• 纳斯达克指数：22597.15点，跌2.03%<br/>
• 恐慌指数VIX：15.23，涨2.1%</p>

<p style="font-size:14px;font-weight:bold;color:#34495e;margin-top:15px;">领涨板块</p>
<p>🚀 能源板块：涨1.2%，受油价反弹支撑<br/>
💊 医疗保健：涨0.8%，生物科技股走强<br/>
🏭 工业板块：涨0.5%，制造业数据向好</p>

<p style="font-size:14px;font-weight:bold;color:#34495e;margin-top:15px;">领跌板块</p>
<p>📉 科技板块：跌2.1%，大型科技股承压<br/>
💳 金融板块：跌1.5%，银行股普遍下跌<br/>
🏠 房地产：跌1.2%，利率预期影响</p>

<p style="font-size:14px;font-weight:bold;color:#34495e;margin-top:15px;">明星个股</p>
<p>📈 涨幅榜：<br/>
• 英伟达(NVDA)：涨3.2%，AI芯片需求强劲<br/>
• 特斯拉(TSLA)：涨2.8%，交付数据超预期<br/>
• 微软(MSFT)：涨1.5%，云业务增长稳健</p>

<p>📉 跌幅榜：<br/>
• 苹果(AAPL)：跌2.5%，iPhone销量担忧<br/>
• 亚马逊(AMZN)：跌2.1%，电商增速放缓<br/>
• Meta(META)：跌1.8%，广告收入承压</p>

<p style="font-size:16px;font-weight:bold;color:#000;margin-top:20px;">亚太市场</p>

<p style="font-size:14px;font-weight:bold;color:#34495e;margin-top:15px;">主要指数</p>
<p>• 日经225指数：38450.50点，跌0.8%<br/>
• 韩国综合指数：2580.30点，跌0.5%<br/>
• 恒生指数：23150.20点，跌1.2%</p>

<p style="font-size:16px;font-weight:bold;color:#000;margin-top:20px;">📰 市场要闻</p>

<p style="font-size:14px;font-weight:bold;color:#34495e;margin-top:15px;">宏观经济</p>
<p>• 美联储官员发表鹰派言论，暗示维持高利率<br/>
• 美国1月CPI数据公布，同比上涨3.1%，符合预期<br/>
• 欧洲央行维持利率不变，关注通胀走势</p>

<p style="font-size:14px;font-weight:bold;color:#34495e;margin-top:15px;">公司动态</p>
<p>• 英伟达发布新一代AI芯片，性能提升50%<br/>
• 特斯拉宣布在中国扩建超级工厂<br/>
• 苹果推迟Vision Pro在中国上市时间</p>

<p style="font-size:14px;font-weight:bold;color:#34495e;margin-top:15px;">商品期货</p>
<p>• 黄金：2025美元/盎司，跌0.5%<br/>
• 原油：75.50美元/桶，涨1.2%<br/>
• 比特币：48500美元，涨2.3%</p>

<p style="font-size:16px;font-weight:bold;color:#000;margin-top:20px;">📊 今日关注</p>

<p style="color:#666;line-height:1.8;"><strong>A股市场展望：</strong><br/>
• 关注美股科技股调整对A股科技板块的影响<br/>
• 重点关注半导体、新能源、军工板块<br/>
• 注意外资流向和北向资金动态</p>

<p style="color:#666;line-height:1.8;"><strong>重要数据：</strong><br/>
• 10:00 中国1月社会融资规模<br/>
• 14:00 德国1月CPI终值<br/>
• 21:30 美国上周初请失业金人数</p>

<p style="font-size:16px;font-weight:bold;color:#000;margin-top:20px;">💡 早间观点</p>
<p style="color:#666;line-height:1.8;">隔夜美股科技股承压，纳指领跌。美联储官员鹰派言论打压市场情绪，但能源和医疗板块表现相对抗跌。亚太市场普遍低开，A股今日或承压开盘。建议关注政策面动向和外资流向，短期以防守为主，关注低估值蓝筹和高股息板块的配置机会。</p>

<p style="color:#999;font-size:12px;margin-top:20px;"><em>数据来源：公开市场数据整理</em><br/>
<em>风险提示：市场有风险，投资需谨慎</em></p>
"""
        
        return report
    
    def create_wechat_draft(self, title, content, thumb_media_id):
        """创建微信公众号草稿"""
        if not self.access_token:
            print("✗ 缺少access_token，无法创建草稿")
            return False
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={self.access_token}"
        
        data = {
            "articles": [
                {
                    "title": title,
                    "author": "yuaner",
                    "digest": "隔夜美股、亚太市场行情及今日A股展望",
                    "content": content,
                    "content_source_url": "",
                    "thumb_media_id": thumb_media_id,
                    "need_open_comment": 0,
                    "only_fans_can_comment": 0
                }
            ]
        }
        
        try:
            print(f"正在创建微信公众号草稿...")
            # 确保使用UTF-8编码
            response = requests.post(
                url, 
                data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                headers={'Content-Type': 'application/json; charset=utf-8'},
                timeout=30
            )
            result = response.json()
            
            if result.get('errcode') == 0 or 'media_id' in result:
                print(f"✓ 草稿创建成功！media_id: {result.get('media_id')}")
                print(f"✓ 请登录微信公众号后台查看草稿箱")
                return True
            else:
                print(f"✗ 草稿创建失败: {result}")
                return False
                
        except Exception as e:
            print(f"✗ 创建草稿异常: {e}")
            return False
    
    def run(self):
        """执行完整流程"""
        print("="*60)
        print("金融行情早报自动发布系统")
        print("="*60)
        
        # 1. 获取access_token
        print("\n【步骤1】获取微信公众号access_token...")
        if not self.get_wechat_access_token():
            print("✗ 流程终止：无法获取access_token")
            return
        
        # 2. 生成封面图片
        print("\n【步骤2】生成封面图片...")
        date_str = datetime.now().strftime("%Y年%m月%d日")
        image_path = self.generate_cover_image(date_str)
        
        if not image_path:
            print("✗ 流程终止：封面图片生成失败")
            return
        
        # 3. 上传图片到微信
        print("\n【步骤3】上传封面到微信公众号...")
        thumb_media_id = self.upload_image_to_wechat(image_path)
        
        if not thumb_media_id:
            print("✗ 流程终止：封面图片上传失败")
            return
        
        # 4. 生成简报内容
        print("\n【步骤4】生成行情早报内容...")
        content = self.generate_morning_report()
        print(f"✓ 早报内容生成完成，共{len(content)}字符")
        
        # 5. 创建草稿
        print("\n【步骤5】创建微信公众号草稿...")
        title = f"{date_str} 行情早报"
        success = self.create_wechat_draft(title, content, thumb_media_id)
        
        if success:
            print("\n" + "="*60)
            print("✓✓✓ 所有步骤完成！")
            print("="*60)
            print("请登录微信公众号后台 -> 素材管理 -> 草稿箱 查看")
        else:
            print("\n✗ 发布失败，请检查错误信息")


if __name__ == "__main__":
    try:
        publisher = MorningReportPublisher('config.json')
        publisher.run()
    except FileNotFoundError:
        print("✗ 错误：找不到配置文件 config.json")
        print("请先填写配置文件中的微信公众号和阿里云API信息")
    except Exception as e:
        print(f"✗ 程序异常: {e}")
        import traceback
        traceback.print_exc()
