pyinstaller "src\main.py" --onefile --name asteroids --windowed
xcopy "src\sounds" "dist\asteroids\sounds" /Y /I
move /Y "dist\asteroids.exe" "dist\asteroids\asteroids.exe"
tar.exe acf "dist/asteroids.zip" "dist/asteroids/*"