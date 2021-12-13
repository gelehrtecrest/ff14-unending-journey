@echo off

rem 作業フォルダ
set DIR=docs\step1
rem 画像フォルダ
set IMG=image_j
rem 対象
set OUTPUT=index_j.md

rem 初期化
if exist %DIR%\%OUTPUT% del %DIR%\%OUTPUT%

rem 残りは画像ファイル
for %%f in (%DIR%\%IMG%\*) do (
    echo %%~nxf
    echo [![%%~nxf]^(./%IMG%/%%~nxf^)]^(./%IMG%/%%~nxf^) >> %DIR%\%OUTPUT%
)