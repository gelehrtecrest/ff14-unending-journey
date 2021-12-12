@echo off

rem 作業フォルダ
set DIR=docs\step1

rem 初期化
if exist %DIR%\index_j.md del %DIR%\index_j.md

rem 残りは画像ファイル
for %%f in (%DIR%\image_j\*) do (
    echo %%~nxf
    echo ![%%~nxf]^(./image_j/%%~nxf^) >> %DIR%\index_j.md
)