print("Loading...")
import time,sys,os

def Log(text="",end="\r\n"):
    sys.stdout.write((("%s" % text) + end))
    sys.stdout.flush()
    LogFile = open("valid_words.txt","ab")
    LogFile.write((("%s" % text) + end).encode())
    LogFile.close()

Log("Initialising rtx process...")
import requests, json

wordlist_file = "english.txt"
word_file = open(wordlist_file,"r")
wordlist = word_file.readlines()
word_file.close()

target_page = "https://forms.nvidia.eu/FP_20181017_rtx_treasure_hunt/process?isJs=1&returnAs=json"

headers = {'Accept':'*/*','Referer': 'https://www.nvidia.com/en-gb/geforce/contests/rtx-treasure-hunt/?nvid=nv-int-60278','Origin':'https://www.nvidia.com','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}


def test_word_valid(test_word):
    print("Testing: %s" % test_word)
    payload = {"rtx_answer": test_word, "ncid": "", "consumerOptInSentence": "Send me gaming & entertainment deals, announcements, and more from NVIDIA. I can unsubscribe at any time.", "region":"en_gb"}
    error = True
    while error:
        try:
            test_outcome = requests.post(target_page, data=payload, headers=headers)
            j = json.loads(test_outcome.content.decode())
            error = False
        except:
            pass
    if "Sorry, that's not it." in j["messages"][0]:
        return False
    else:
        print(j)
        return True

word_num = 1
max_words = len(wordlist)
for word in wordlist:
    print("%s / %s" % (word_num,max_words))
    if len(word) > 2 and len(word) < 11:
        if test_word_valid(word):
            Log("------------- Valid Word: %s" % word)
    word_num += 1
