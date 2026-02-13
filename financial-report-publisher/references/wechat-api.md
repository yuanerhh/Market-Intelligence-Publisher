# 微信公众号API参考

本文档介绍金融行情简报发布所需的微信公众号API接口。

## API概述

### 基础URL

```
https://api.weixin.qq.com
```

### 认证方式

所有API请求需要携带 `access_token` 参数。

## 1. 获取Access Token

### 接口说明

access_token是公众号的全局唯一接口调用凭据，有效期为7200秒（2小时）。

### 请求方式

```
GET /cgi-bin/token
```

### 请求参数

| 参数 | 必填 | 说明 |
|------|------|------|
| grant_type | 是 | 固定值：client_credential |
| appid | 是 | 第三方用户唯一凭证 |
| secret | 是 | 第三方用户唯一凭证密钥 |

### 示例代码

```python
def get_access_token(appid, secret):
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": appid,
        "secret": secret
    }
    response = requests.get(url, params=params)
    result = response.json()
    
    if 'access_token' in result:
        return result['access_token']
    else:
        raise Exception(f"获取access_token失败: {result}")
```

### 返回示例

```json
{
  "access_token": "65_xxxxx",
  "expires_in": 7200
}
```

### 错误码

| 错误码 | 说明 |
|--------|------|
| 40001 | AppSecret错误 |
| 40002 | 请确保grant_type字段值为client_credential |
| 40164 | 调用接口超过限制 |

## 2. 上传临时素材

### 接口说明

上传图片素材，获取media_id用于草稿封面。

### 请求方式

```
POST /cgi-bin/material/add_material?access_token=ACCESS_TOKEN&type=TYPE
```

### 请求参数

| 参数 | 必填 | 说明 |
|------|------|------|
| access_token | 是 | 调用接口凭证 |
| type | 是 | 媒体文件类型：image |
| media | 是 | form-data中媒体文件标识 |

### 示例代码

```python
def upload_image(access_token, image_path):
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material"
    params = {
        "access_token": access_token,
        "type": "image"
    }
    
    files = {
        'media': ('cover.jpg', open(image_path, 'rb'), 'image/jpeg')
    }
    
    response = requests.post(url, params=params, files=files)
    result = response.json()
    
    if 'media_id' in result:
        return result['media_id']
    else:
        raise Exception(f"上传图片失败: {result}")
```

### 返回示例

```json
{
  "media_id": "_NnM_1z6zBKY92qZKhSNP...",
  "url": "http://mmbiz.qpic.cn/..."
}
```

### 限制说明

- 图片大小不超过2MB
- 支持格式：jpg, png
- 临时素材有效期为3天

## 3. 新建草稿

### 接口说明

创建图文消息草稿，可在公众号后台编辑后发布。

### 请求方式

```
POST /cgi-bin/draft/add?access_token=ACCESS_TOKEN
```

### 请求参数

| 参数 | 必填 | 说明 |
|------|------|------|
| access_token | 是 | 调用接口凭证 |
| articles | 是 | 图文消息数组 |

### articles字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| title | 是 | 标题（不超过64字符） |
| author | 否 | 作者（不超过8字符） |
| digest | 否 | 摘要（不超过120字符） |
| content | 是 | 图文消息内容（HTML格式） |
| content_source_url | 否 | 原文链接 |
| thumb_media_id | 是 | 封面图片media_id |
| need_open_comment | 否 | 是否打开评论（0/1） |
| only_fans_can_comment | 否 | 是否粉丝才可评论（0/1） |

### 示例代码

```python
def create_draft(access_token, title, content, thumb_media_id):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
    params = {
        "access_token": access_token
    }
    
    data = {
        "articles": [
            {
                "title": title,
                "author": "小跃",
                "digest": "今日A股、美股、期货市场收盘行情汇总",
                "content": content,
                "content_source_url": "",
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0
            }
        ]
    }
    
    # 重要：确保UTF-8编码
    response = requests.post(
        url,
        params=params,
        data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'}
    )
    
    result = response.json()
    
    if result.get('errcode') == 0 or 'media_id' in result:
        return result.get('media_id')
    else:
        raise Exception(f"创建草稿失败: {result}")
```

### 返回示例

```json
{
  "media_id": "_NnM_1z6zBKY92qZKhSNP..."
}
```

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 40001 | access_token无效 | 重新获取access_token |
| 40007 | media_id无效 | 检查封面图片是否上传成功 |
| 45003 | title size out of limit | 标题不超过64字符 |
| 45110 | author size out of limit | 作者不超过8字符 |
| 87009 | 内容含有违规内容 | 检查内容是否符合规范 |

## 4. 获取草稿列表

### 接口说明

获取草稿列表，用于查看已创建的草稿。

### 请求方式

```
POST /cgi-bin/draft/batchget?access_token=ACCESS_TOKEN
```

### 请求参数

```json
{
  "offset": 0,
  "count": 20,
  "no_content": 1
}
```

### 示例代码

```python
def get_draft_list(access_token, offset=0, count=20):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget"
    params = {
        "access_token": access_token
    }
    
    data = {
        "offset": offset,
        "count": count,
        "no_content": 1  # 不返回content字段
    }
    
    response = requests.post(url, params=params, json=data)
    return response.json()
```

## 5. 删除草稿

### 接口说明

删除指定的草稿。

### 请求方式

```
POST /cgi-bin/draft/delete?access_token=ACCESS_TOKEN
```

### 请求参数

```json
{
  "media_id": "MEDIA_ID"
}
```

### 示例代码

```python
def delete_draft(access_token, media_id):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/delete"
    params = {
        "access_token": access_token
    }
    
    data = {
        "media_id": media_id
    }
    
    response = requests.post(url, params=params, json=data)
    result = response.json()
    
    if result.get('errcode') == 0:
        return True
    else:
        raise Exception(f"删除草稿失败: {result}")
```

## HTML内容规范

### 支持的标签

- 标题：`<h1>` ~ `<h6>`
- 段落：`<p>`
- 列表：`<ul>`, `<ol>`, `<li>`
- 强调：`<strong>`, `<em>`
- 链接：`<a href="">`
- 图片：`<img src="">`
- 分割线：`<hr>`
- 引用：`<blockquote>`

### 样式建议

```html
<!-- 标题 -->
<h2 style="color: #333; font-size: 20px; margin: 20px 0;">标题</h2>

<!-- 段落 -->
<p style="line-height: 1.8; color: #666;">段落内容</p>

<!-- 列表 -->
<ul style="list-style: disc; padding-left: 20px;">
  <li style="margin: 10px 0;">列表项</li>
</ul>

<!-- 强调 -->
<strong style="color: #e74c3c;">重要内容</strong>
```

### 注意事项

1. **编码问题** - 必须使用UTF-8编码，设置正确的Content-Type
2. **图片链接** - 图片必须使用HTTPS链接
3. **外链限制** - 原文链接需要在公众号后台配置白名单
4. **内容审核** - 内容需符合微信公众平台运营规范

## 完整示例

```python
class WeChatPublisher:
    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret
        self.access_token = None
    
    def get_access_token(self):
        """获取access_token"""
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.secret
        }
        response = requests.get(url, params=params)
        result = response.json()
        
        if 'access_token' in result:
            self.access_token = result['access_token']
            return self.access_token
        else:
            raise Exception(f"获取access_token失败: {result}")
    
    def upload_image(self, image_path):
        """上传图片"""
        url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
        params = {
            "access_token": self.access_token,
            "type": "image"
        }
        
        files = {
            'media': ('cover.jpg', open(image_path, 'rb'), 'image/jpeg')
        }
        
        response = requests.post(url, params=params, files=files)
        result = response.json()
        
        if 'media_id' in result:
            return result['media_id']
        else:
            raise Exception(f"上传图片失败: {result}")
    
    def create_draft(self, title, content, thumb_media_id):
        """创建草稿"""
        url = "https://api.weixin.qq.com/cgi-bin/draft/add"
        params = {
            "access_token": self.access_token
        }
        
        data = {
            "articles": [
                {
                    "title": title,
                    "author": "小跃",
                    "digest": "今日行情汇总",
                    "content": content,
                    "thumb_media_id": thumb_media_id,
                    "need_open_comment": 0,
                    "only_fans_can_comment": 0
                }
            ]
        }
        
        response = requests.post(
            url,
            params=params,
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            headers={'Content-Type': 'application/json; charset=utf-8'}
        )
        
        result = response.json()
        
        if result.get('errcode') == 0 or 'media_id' in result:
            return result.get('media_id')
        else:
            raise Exception(f"创建草稿失败: {result}")
    
    def publish(self, title, content, cover_image_path):
        """完整发布流程"""
        # 1. 获取access_token
        self.get_access_token()
        
        # 2. 上传封面
        thumb_media_id = self.upload_image(cover_image_path)
        
        # 3. 创建草稿
        media_id = self.create_draft(title, content, thumb_media_id)
        
        return media_id

# 使用示例
publisher = WeChatPublisher(appid="xxx", secret="xxx")
media_id = publisher.publish(
    title="2026年02月13日 行情晚报",
    content="<h2>行情简报</h2><p>内容...</p>",
    cover_image_path="cover.jpg"
)
print(f"草稿创建成功: {media_id}")
```

## 相关资源

- 微信公众平台技术文档：https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html
- 草稿箱API：https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html
- 素材管理API：https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html
