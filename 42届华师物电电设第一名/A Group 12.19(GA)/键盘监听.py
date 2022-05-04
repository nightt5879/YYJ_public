from pynput import keyboard 
import threading   

def on_press(key):
    try:

        if key.char == 'w':
             print('w')
        if key.char == 'a':
             print('a')
        if key.char == 's':
             print('s')
        if key.char == 'd':
             print('d')
    except AttributeError:
        print('special {0}'.format(key))

   
def on_release(key):
    print(threading.current_thread().name+'{0}release'.format(key))
    if key == keyboard.Key.esc:
        return False


def anjian():
    with keyboard.Listener(
        on_press=on_press, on_release=on_release) as listener:
        listener.join()

# 子线程 1 键盘监听
thread = threading.Thread(target=anjian,name='1')
thread.start()


