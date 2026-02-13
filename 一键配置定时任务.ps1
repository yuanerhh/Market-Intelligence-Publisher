# 金融行情早报+晚报 定时任务一键配置脚本
# 执行方式：右键 -> 使用PowerShell运行

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   金融行情早报+晚报 定时任务配置" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 检查管理员权限
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "✗ 需要管理员权限！请右键选择'以管理员身份运行PowerShell'" -ForegroundColor Red
    pause
    exit
}

Write-Host "✓ 管理员权限确认" -ForegroundColor Green

# 配置路径
$pythonPath = "D:\Program Files\Python310\python.exe"
$morningScript = "E:\jieyue_data\Market-Intelligence-Publisher\morning_report_publisher.py"
$eveningScript = "E:\jieyue_data\Market-Intelligence-Publisher\market_report_publisher.py"
$workingDir = "E:\jieyue_data\Market-Intelligence-Publisher"

# 检查文件是否存在
Write-Host "`n检查文件..." -ForegroundColor Yellow
if (-not (Test-Path $pythonPath)) {
    Write-Host "✗ Python未找到: $pythonPath" -ForegroundColor Red
    Write-Host "请修改脚本中的Python路径" -ForegroundColor Yellow
    pause
    exit
}
Write-Host "✓ Python路径正确" -ForegroundColor Green

if (-not (Test-Path $morningScript)) {
    Write-Host "✗ 早报脚本未找到: $morningScript" -ForegroundColor Red
    pause
    exit
}
Write-Host "✓ 早报脚本存在" -ForegroundColor Green

if (-not (Test-Path $eveningScript)) {
    Write-Host "✗ 晚报脚本未找到: $eveningScript" -ForegroundColor Red
    pause
    exit
}
Write-Host "✓ 晚报脚本存在" -ForegroundColor Green

# 创建早报任务
Write-Host "`n创建早报定时任务（每天7:00）..." -ForegroundColor Yellow

try {
    $morningAction = New-ScheduledTaskAction `
        -Execute $pythonPath `
        -Argument $morningScript `
        -WorkingDirectory $workingDir

    $morningTrigger = New-ScheduledTaskTrigger -Daily -At 7:00AM

    $morningPrincipal = New-ScheduledTaskPrincipal `
        -UserId $env:USERNAME `
        -RunLevel Highest

    $morningSettings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable

    # 删除已存在的任务
    Unregister-ScheduledTask -TaskName "金融行情早报发布" -Confirm:$false -ErrorAction SilentlyContinue

    Register-ScheduledTask `
        -TaskName "金融行情早报发布" `
        -Action $morningAction `
        -Trigger $morningTrigger `
        -Principal $morningPrincipal `
        -Settings $morningSettings `
        -Description "每天早上7:00自动发布金融行情早报（美股、亚太市场、市场要闻）" | Out-Null

    Write-Host "✓ 早报任务创建成功！" -ForegroundColor Green
} catch {
    Write-Host "✗ 早报任务创建失败: $_" -ForegroundColor Red
}

# 创建晚报任务
Write-Host "`n创建晚报定时任务（每天15:30）..." -ForegroundColor Yellow

try {
    $eveningAction = New-ScheduledTaskAction `
        -Execute $pythonPath `
        -Argument $eveningScript `
        -WorkingDirectory $workingDir

    $eveningTrigger = New-ScheduledTaskTrigger -Daily -At 3:30PM

    $eveningPrincipal = New-ScheduledTaskPrincipal `
        -UserId $env:USERNAME `
        -RunLevel Highest

    $eveningSettings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable

    # 删除已存在的任务
    Unregister-ScheduledTask -TaskName "金融行情晚报发布" -Confirm:$false -ErrorAction SilentlyContinue

    Register-ScheduledTask `
        -TaskName "金融行情晚报发布" `
        -Action $eveningAction `
        -Trigger $eveningTrigger `
        -Principal $eveningPrincipal `
        -Settings $eveningSettings `
        -Description "每天下午15:30自动发布金融行情晚报（A股、美股、期货收盘）" | Out-Null

    Write-Host "✓ 晚报任务创建成功！" -ForegroundColor Green
} catch {
    Write-Host "✗ 晚报任务创建失败: $_" -ForegroundColor Red
}

# 显示任务信息
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "   定时任务配置完成！" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan

Write-Host "`n已创建的定时任务：" -ForegroundColor Yellow
Write-Host "  1. 金融行情早报发布 - 每天 07:00" -ForegroundColor White
Write-Host "  2. 金融行情晚报发布 - 每天 15:30" -ForegroundColor White

Write-Host "`n任务管理命令：" -ForegroundColor Yellow
Write-Host "  查看任务：taskschd.msc" -ForegroundColor White
Write-Host "  立即测试：schtasks /run /tn `"金融行情早报发布`"" -ForegroundColor White
Write-Host "  禁用任务：schtasks /change /tn `"金融行情早报发布`" /disable" -ForegroundColor White
Write-Host "  启用任务：schtasks /change /tn `"金融行情早报发布`" /enable" -ForegroundColor White
Write-Host "  删除任务：schtasks /delete /tn `"金融行情早报发布`" /f" -ForegroundColor White

Write-Host "`n是否立即测试早报任务？(Y/N): " -ForegroundColor Yellow -NoNewline
$test = Read-Host
if ($test -eq 'Y' -or $test -eq 'y') {
    Write-Host "`n正在运行早报任务..." -ForegroundColor Yellow
    schtasks /run /tn "金融行情早报发布"
    Start-Sleep -Seconds 2
    Write-Host "请检查微信公众号后台草稿箱" -ForegroundColor Green
}

Write-Host "`n配置完成！按任意键退出..." -ForegroundColor Cyan
pause
