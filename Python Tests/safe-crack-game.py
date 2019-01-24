from random import randrange
import base64
duplicate_chars = False
characters = ["0","1","2","3","4","5","6","7","8","9"]
code_length = 4
safe_contents = "ICAgICAgICAgICAgICAgICAsLj1jdEU1NXR0dDU1M3R6cy4sICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgLCxjNTt6PT0hITo6OjogIC46Ojc6PT1pdDM+LiwgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAseEM7eiE6Ojo6OjogICAgOjo6Ojo6Ojo6Ojo6IT1jMzN4LCAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAsY3p6ITo6Ojo6ICA6Ojs7Li49PT06Li46OjogICA6Ojo6IWN0My4gICAgICAgICAgICAgICAgICAgIAogICAgICAsQzsvLjo6IDogIDs9YyE6Ojo6Ojo6Ojo6Ojo6OjouLiAgICAgICF0dDMuICAgICAgICAgICAgICAgICAgCiAgICAgL3ovLjogICA6O3ohOjo6OjpKICA6RTMuICBFOjo6Ojo6Oi4uICAgICAhY3QzLiAgICAgICAgICAgICAgICAKICAgLEU7RiAgIDo6O3Q6Ojo6Ojo6OkogIDpFMy4gIEU6Oi4gICAgIDo6LiAgICAgXHR0TCAgICAgICAgICAgICAgIAogIDtFNy4gICAgOmM6Ojo6RioqKioqKiAgICoqLiAgKj09YzsuLiAgICA6OiAgICAgSnR0ayAgICAgICAgICAgICAgCiAuRUouICAgIDs6Ojo6OjpMICAgICAgICAgICAgICAgICAgICJcOi4gICA6Oi4gICAgSnR0bCAgICAgICAgICAgICAKIFs6LiAgICA6Ojo6Ojo6Ojo3NzMuICAgIEpFNzczenMuICAgICBJOi4gOjo6Oi4gICAgSXQzTCAgICAgICAgICAgIAo7OlsgICAgIEw6Ojo6Ojo6Ojo6OkwgICAgfHQ6OiE6OkogICAgIHw6Ojo6Ojo6OiAgICA6RXQzICAgICAgICAgICAgCls6TCAgICAhOjo6Ojo6Ojo6Ojo6TCAgICB8dDo6O3oyRiAgICAuRXQ6OjouOjo6LiAgOjpbMTMgICAgQklUQ09JTlMKRTouICAgICE6Ojo6Ojo6Ojo6OjpMICAgICAgICAgICAgICAgPUV0Ojo6Ojo6OjohICA6OnwxMyAgICBCTEFIICAgIApFOi4gICAgKDo6Ojo6Ojo6Ojo6OkwgICAgLi4uLi4uLiAgICAgICBcOjo6Ojo6OiEgIDo6fGkzICAgIEJMQUggICAgCls6TCAgICAhOjo6OiAgICAgIDo6TCAgICB8M3Q6Ojo6ITMuICAgICBdOjo6Ojo6LiAgOjpbMTMgICAgQkxBSCAgICAKITooICAgICAuOjo6OjogICAgOjpMICAgIHx0Ojo6Ojo6M0wgICAgIHw6Ojo6OjsgOjo6OkVFMyAgICBCTEFIICAgIAogRTMuICAgIDo6Ojo6Ojo6Ojt6NS4gICAgSno7Ozt6PUYuICAgICA6RTo6Ojo6Ljo6OjpJSTNbICAgICAgICAgICAgCiBKdDEuICAgIDo6Ojo6OjpbICAgICAgICAgICAgICAgICAgICA7ejU6Ojo6Oy46Ojo6OzN0MyAgICAgICAgICAgICAKICBcejEuOjo6Ojo6Ojo6OmwuLi4uLi4gICAuLiAgIDsuPWN0NTo6Ojo6Oi8uOjo6OjtFdDNMICAgICAgICAgICAgIAogICBcdDMuOjo6Ojo6Ojo6Ojo6Ojo6SiAgOkUzLiAgRXQ6Ojo6Ojo6OjshOjo6Ojo7NUUzTCAgICAgICAgICAgICAgCiAgICAiY3pcLjo6Ojo6Ojo6Ojo6OjpKICAgRTMuICBFOjo6Ojo6OnohICAgICA7WnozN2AgICAgICAgICAgICAgICAKICAgICAgXHozLiAgICAgICA6Ojs6Ojo6Ojo6Ojo6Ojo6Ojo7PScgICAgICAuLzM1NUYgICAgICAgICAgICAgICAgIAogICAgICAgIFx6M3guICAgICAgICAgOjp+PT09PT09PScgICAgICAgICAsYzI1M0YgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAidHozPS4gICAgICAgICAgICAgICAgICAgICAgLi5jNXQzMl4gICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICI9enozPT0uLi4gICAgICAgICAuLi49dDN6MTNQXiAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgIGAqPXpqemN6SUlJSTN6enp0RTM+Kl5gICAgICAgICAgICAgICAgICAgICAgICAgICAgCgpBbGwgeW91IGdvdCB3YXMgYSB1c2VsZXNzIGJpdGNvaW4u"
globals()["safe-code"] = ""

def unlock(code):
    safe_code = ""
    for i in globals()["safe-code"]:
        safe_code += i
    if code == safe_code:
        print("[MASTERLOCK-1337] SAFE CONTENTS:\n")
        contents = base64.b64decode(safe_contents) + b"\n\n"
        print(contents.decode())

def gameloop():
    print("===NEW GAME===\n")
    print("[MASTERLOCK-1337] -=LOCKING SAFE=-\n")
    safe_code = []
    for i in range(code_length):
        randchar = characters[randrange(len(characters))]
        while randchar in safe_code and not duplicate_chars:
            randchar = characters[randrange(len(characters))]
        safe_code.append(randchar)
    globals()["safe-code"] = safe_code
    # print(safe_code)
    print("""The safe has been locked, try to guess the %s digit code.
Due to a firmware glitch, the safe leaks information about your guess.
It will tell you how many correct numbers you guessed,
how many of the numbers are correct, but in the wrong position,
and how many are wrong.
Good Luck, and have fun!\n""" % code_length)
    strchars = ""
    for i in characters:
        strchars += i + ", "
    print("Possible Characters: %s\n" % strchars[:-2])
    if duplicate_chars:
        print("[MASTERLOCK-1337] Code Can Contain Duplicates")
    else:
        print("[MASTERLOCK-1337] Code Cannot Contain Duplicates")
    guessed_code = False
    guesses = 0
    while not guessed_code:
        got_guess = False
        guess = ""
        while not got_guess:
            print()
            guess = input("[MASTERLOCK-1337] GUESS: ")
            if len(guess) == code_length:
                good_guess = 0
                for i in guess:
                    if i in characters:
                        good_guess += 1
                if good_guess == code_length:
                    got_guess = True
        print()
        output_hint = [0,0,0]
        for i in range(code_length):
            gchar = guess[i]
            if gchar == safe_code[i]:
                output_hint[0] += 1
            elif gchar in safe_code:
                output_hint[1] += 1
            else:
                output_hint[2] += 1
        print("[MASTERLOCK-1337] Correct Character and Position: %s" % output_hint[0])
        print("[MASTERLOCK-1337] Correct Character:              %s" % output_hint[1])
        print("[MASTERLOCK-1337] Wrong Characters:               %s\n" % output_hint[2])
        guesses += 1
        if output_hint[0] == code_length:
            print("[MASTERLOCK-1337] -=Safe Unlocked=- Code: %s    Guesses: %s\n\n" % (guess,guesses))
            unlock(guess)
            guessed_code = True

if __name__ == "__main__":
    while True:
        gameloop()
