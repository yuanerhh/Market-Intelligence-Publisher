@echo off
echo ============================================
echo    金融行情早报+晚报 定时任务配置
echo ============================================
echo.
echo 正在创建定时任务...
echo.

REM 删除已存在的任务（如果有）
schtasks /delete /tn "金融行情早报发布" /f >nul 2>&1
schtasks /delete /tn "金融行情晚报发布" /f >nul 2>&1

REM 创建早报任务（每天7:00）
schtasks /create /tn "金融行情早报发布" ^
  /tr "\"D:\Program Files\Python310\python.exe\" \"E:\jieyue_data\Market-Intelligence-Publisher\morning_report_publisher.py\"" ^
  /sc daily /st 07:00 /rl highest /f

if %errorlevel% equ 0 (
    echo [成功] 早报任务创建成功！每天7:00执行
) else (
    echo [失败] 早报任务创建失败，错误代码: %errorlevel%
)

echo.

REM 创建晚报任务（每天15:30）
schtasks /create /tn "金融行情晚报发布" ^
  /tr "\"D:\Program Files\Python310\python.exe\" \"E:\jieyue_data\Market-Intelligence-Publisher\market_report_publisher.py\"" ^
  /sc daily /st 15:30 /rl highest /f

if %errorlevel% equ 0 (
    echo [成功] 晚报任务创建成功！每天15:30执行
) else (
    echo [失败] 晚报任务创建失败，错误代码: %errorlevel%
)

echo.
echo ============================================
echo    配置完成！
echo ============================================
echo.
echo 已创建的定时任务：
echo   1. 金融行情早报发布 - 每天 07:00
echo   2. 金融行情晚报发布 - 每天 15:30
echo.
echo 管理命令：
echo   查看任务：taskschd.msc
echo   立即测试：schtasks /run /tn "金融行情早报发布"
echo   禁用任务：schtasks /change /tn "金融行情早报发布" /disable
echo   启用任务：schtasks /change /tn "金融行情早报发布" /enable
echo   删除任务：schtasks /delete /tn "金融行情早报发布" /f
echo.
echo 按任意键退出...
pause >nul
