import pyautogui

pyautogui.prompt("Enter your Address","IG","ftp://192.168.43.215:2221")
myip = pyautogui.prompt("Enter your Address","IG","ftp://192.168.43.215:2221")
pyautogui.hotkey('win','e',interval=0.5)
pyautogui.hotkey('shift','f10','up')
pyautogui.hotkey('up','enter',interval=0.5)
pyautogui.press('enter',interval=0.5)
pyautogui.press('tab')
pyautogui.press('up')
pyautogui.press('enter')

pyautogui.write(myip)
pyautogui.press('enter',interval=0.5)
pyautogui.press('enter',interval=0.5)
pyautogui.press('enter',interval=0.5)



