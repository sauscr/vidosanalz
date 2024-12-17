import time 
seconds = 60
while seconds:
    timer = f'{seconds:02d}'
    print(timer, end = '\r')
    time.sleep(1)
    seconds -= 1
print("00")