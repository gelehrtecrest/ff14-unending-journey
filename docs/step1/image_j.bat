@echo off

rem 作業フォルダ
set DIR=docs\step1

rem 最初はテンプレート
copy %DIR%\template_j.md %DIR%\index_j.md

rem 残りは画像ファイル
for %%f in (%DIR%\image_j\*) do (
    echo %%~nxf
    echo ![%%~nxf]^(./image_j/%%~nxf^) >> %DIR%\index_j.md
)