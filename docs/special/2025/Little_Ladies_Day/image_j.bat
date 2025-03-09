@echo off

rem 作業フォルダ
set DIR=docs\special\2025\Little_Ladies_Day
rem 画像フォルダ
set IMG=image_j
rem サムネイルフォルダ
set IMG_THUMB=image_j_thumb
rem 対象
set OUTPUT=index_j.md

rem 初期化
if exist %DIR%\%OUTPUT% del %DIR%\%OUTPUT%
if exist %DIR%\%IMG_THUMB% rd /s /q %DIR%\%IMG_THUMB%
md %DIR%\%IMG_THUMB%

rem 残りは画像ファイル
for %%f in (%DIR%\%IMG%\*) do (
    echo %%~nxf
    magick convert -resize 480x270 %DIR%\%IMG%\%%~nxf %DIR%\%IMG_THUMB%\%%~nxf.thumb.jpg
    echo [![%%~nxf]^(./%IMG_THUMB%/%%~nxf.thumb.jpg^)]^(./%IMG%/%%~nxf^) >> %DIR%\%OUTPUT%
)