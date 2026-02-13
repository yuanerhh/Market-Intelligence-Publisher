# -*- coding: utf-8 -*-
"""
金融行情简报自动发布系统
功能：生成A股、美股、期货收盘简报，并发布到微信公众号草稿箱
"""

import json
import requests
import time
from datetime import datetime
import base64
import os


class MarketReportPublisher:
    def __init__(self, config_path='config.json'):
        """初始化配置"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.wechat_appid = self.config['wechat']['appid']
        self.wechat_secret = self.config['wechat']['secret']
        self.aliyun_api_key = self.config['aliyun']['api_key']
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
        """生成封面图片（本地生成，确保文字正确显示）"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import io
            
            print(f"正在生成封面图片...")
            
            # 创建1280x720的图片（16:9）
            width, height = 1280, 720
            
            # 创建深蓝到金色的渐变背景
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            
            # 绘制渐变背景（从深蓝到深蓝金色混合）
            for y in range(height):
                r = int(13 + (218 - 13) * y / height * 0.3)
                g = int(27 + (165 - 27) * y / height * 0.3)
                b = int(62 + (32 - 62) * y / height * 0.3)
                draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))
            
            # 添加金色装饰图案
            # 绘制一些金色线条和图形
            gold_color = (218, 165, 32)
            for i in range(5):
                x = 100 + i * 250
                draw.line([(x, 100), (x+150, 200)], fill=gold_color, width=3)
                draw.ellipse([x+100, 250, x+180, 330], outline=gold_color, width=2)
            
            # 尝试加载字体
            try:
                # Windows系统字体路径
                title_font = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 120)
                date_font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 50)
            except:
                try:
                    title_font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 120)
                    date_font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 50)
                except:
                    # 如果找不到字体，使用默认字体
                    title_font = ImageFont.load_default()
                    date_font = ImageFont.load_default()
                    print("⚠ 警告：未找到中文字体，使用默认字体")
            
            # 绘制标题"行情晚报"
            title_text = "行情晚报"
            # 获取文字边界框
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
            
            # 添加一些装饰元素（股票上涨箭头）
            arrow_color = (34, 197, 94)  # 绿色
            # 绘制上涨箭头
            draw.polygon([(width-150, 550), (width-100, 500), (width-50, 550), 
                         (width-80, 550), (width-80, 620), (width-120, 620), 
                         (width-120, 550)], fill=arrow_color)
            
            # 保存到本地
            local_path = f"cover_{int(time.time())}.jpg"
            image.save(local_path, 'JPEG', quality=95)
            print(f"✓ 封面图片生成成功: {local_path}")
            
            return local_path
            
        except ImportError:
            print("✗ 缺少PIL库，尝试安装...")
            import subprocess
            subprocess.run(["pip", "install", "Pillow"], check=True)
            print("✓ Pillow安装成功，请重新运行程序")
            return None
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
            
            # 上传到微信
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
    
    def generate_market_report(self):
        """生成行情简报内容"""
        today = datetime.now().strftime("%Y年%m月%d日")
        
        # 使用微信公众号支持的HTML格式，A股市场作为第一行
        report = f"""<p style="font-size:16px;font-weight:bold;color:#000;">A股市场</p>

<p style="font-size:14px;font-weight:bold;color:#34495e;margin-top:15px;">主要指数</p>
<p>• 上证指数：4082.07点，跌1.26%<br/>
• 深证成指：14100.19点，跌1.28%<br/>
• 创业板指：3275.96点，跌1.57%<br/>
• 成交额：1.98万亿元</p>

<p style="font-size:14px;font-weight:bold;color:#34495e;margin-top:15px;">领涨板块</p>
<p>🚀 半导体：涨0.14%，主力净流入17.30亿元<br/>
📱 消费电子：涨0.10%，主力净流入10.27亿元<br/>
🚢 船舶制造：涨3.66%，主力净流入7.98亿元<br/>
✈️ 航天航空：涨2.21%，主力净流入5.50亿元</p>

<p style="font-size:14px;font-weight:bold;color:#34495e;margin-top:15px;">领跌板块</p>
<p>📉 互联网服务：跌0.98%，主力净流出78.46亿元<br/>
🔩 有色金属：跌1.95%，主力净流出76.27亿元<br/>
☀️ 光伏设备：跌3.06%，主力净流出70.81亿元<br/>
🔋 小金属：跌2.97%，主力净流出60.36亿元</p>

<p style="font-size:16px;font-weight:bold;color:#000;margin-top:20px;">美股市场（2月12日收盘）</p>
<p>• 道琼斯指数：49451.98点，跌1.34%<br/>
• 标普500指数：6832.76点，跌1.57%<br/>
• 纳斯达克指数：22597.15点，跌2.03%</p>

<p style="font-size:16px;font-weight:bold;color:#000;margin-top:20px;">商品期货市场</p>

<p style="font-size:14px;font-weight:bold;color:#34495e;margin-top:15px;">贵金属</p>
<p>• COMEX黄金：4941.4美元/盎司，跌3.08%<br/>
• 沪金主连：1110.10元/克，跌1.61%<br/>
• 沪银主连：19782元/千克，跌5.52%</p>

<p style="font-size:14px;font-weight:bold;color:#34495e;margin-top:15px;">能源化工</p>
<p>• WTI原油：62.84美元/桶，跌2.77%<br/>
• 上期所原油：450元/桶，跌4.8%</p>

<p style="font-size:14px;font-weight:bold;color:#34495e;margin-top:15px;">工业金属</p>
<p>• 沪铜：102450元/吨，涨0.93%<br/>
• 螺纹钢：3055元/吨，跌0.46%</p>

<p style="font-size:16px;font-weight:bold;color:#000;margin-top:20px;">💡 市场观察</p>
<p style="color:#666;line-height:1.8;">今日A股蛇年收官，全年上证指数累涨25.58%，创业板指大涨58.73%。节前最后一个交易日，周期股回调，但军工、半导体、汽车产业链逆势走强。美股科技股承压，AI相关板块调整。商品期货贵金属回调明显，工业金属分化。</p>

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
                    "author": "AI-Trending",
                    "digest": "今日A股、美股、期货市场收盘行情汇总",
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
        print("金融行情简报自动发布系统")
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
        print("\n【步骤4】生成行情简报内容...")
        content = self.generate_market_report()
        print(f"✓ 简报内容生成完成，共{len(content)}字符")
        
        # 5. 创建草稿
        print("\n【步骤5】创建微信公众号草稿...")
        title = f"{date_str} 行情晚报"
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
        publisher = MarketReportPublisher('config.json')
        publisher.run()
    except FileNotFoundError:
        print("✗ 错误：找不到配置文件 config.json")
        print("请先填写配置文件中的微信公众号和阿里云API信息")
    except Exception as e:
        print(f"✗ 程序异常: {e}")
        import traceback
        traceback.print_exc()
