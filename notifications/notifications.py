import threading, time
import schedule

from slack import slack

def automated_slack_notification():
    schedule.every(2).minutes.do(slack.automated_notification)
    while 1:
        schedule.run_pending()
        time.sleep(1)

thread = threading.Thread(target=automated_slack_notification, args=())
thread.start()
print("Automatic notifications running every 10 mins")
