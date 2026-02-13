@echo off
chcp 65001 >nul
echo ============================================
echo   金融行情简报发布 - 手动执行
echo ============================================
echo.

REM 方式1：使用默认配置文件
echo [方式1] 使用默认配置 (config.json)
"D:\Program Files\Python310\python.exe" "E:\jieyue_data\financial-report-publisher\scripts\market_report_publisher.py"

REM 方式2：指定配置文件路径
REM echo [方式2] 使用指定配置
REM "D:\Program Files\Python310\python.exe" "E:\jieyue_data\financial-report-publisher\scripts\market_report_publisher.py" "E:\jieyue_data\config.json"

echo.
echo ============================================
echo 执行完成！
pause
