@echo off

rem 作業フォルダ
set DIR=docs\step1

rem 初期化
if exist %DIR%\index_e.md del %DIR%\index_e.md

rem 残りは画像ファイル
for %%f in (%DIR%\image_e\*) do (
    echo %%~nxf
    echo ![%%~nxf]^(./image_e/%%~nxf^) >> %DIR%\index_e.md
)