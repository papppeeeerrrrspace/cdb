import os
import sys
import base64
def replaceName(a, b):
    aa =a*2648
    aa += b
    return str(aa)
if len(sys.argv) > 1 :
    number = sys.argv[1]
    counter=-1
    if int(number) > 19 or 0 > int(number) :
        print("invalid number")
    else:
        with open('result1.txt', 'a') as file:
            file.write('start\n')
        file.close()
        with open('counter'+number+'.txt') as f:
            
            for line in f:
                counter += 1
                base64_string =line.strip('\n')
                base64_bytes = base64_string.encode("ascii")
                sample_string_bytes = base64.b64decode(base64_bytes)
                sample_string = sample_string_bytes.decode("ascii")
                os.system('python3.8 a1.py '+sample_string+' '+replaceName(int(number), counter))
                os.system('python3.8 a2.py '+sample_string+' '+replaceName(int(number), counter))
                with open('result1.txt', 'a') as file:
                    file.write(str(counter)+'\n')
                file.close()
        with open('result1.txt', 'a') as file:
            file.write('fin\n')
        file.close()
else :
    print("usage : python execute.py number")
