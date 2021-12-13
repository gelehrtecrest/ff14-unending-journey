@echo off

rem 作業フォルダ
set DIR=docs\step1
rem 対象
set OUTPUT=index_e.md

rem 初期化
if exist %DIR%\%OUTPUT% del %DIR%\%OUTPUT%

rem 残りは画像ファイル
for %%f in (%DIR%\image_e\*) do (
    echo %%~nxf
    echo [![%%~nxf]^(./image_e/%%~nxf^)]^(./image_e/%%~nxf^) >> %DIR%\%OUTPUT%
)