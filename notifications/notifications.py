import threading, time
import schedule

from slack import slack

def automated_slack_notification():
    schedule.every(1).minutes.do(slack.automated_notification)
    while 1:
        schedule.run_pending()
        time.sleep(1)



thread1 = threading.Thread(target=automated_slack_notification, args=())
thread1.start()
print("Automatic notifications running every 10 mins")

# thread2 = threading.Thread(target=handoff, args=())
# thread2.start()
# print("Handoff notifications running")