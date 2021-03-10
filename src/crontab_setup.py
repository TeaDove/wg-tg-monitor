from crontab import CronTab
from pathlib import Path

COMMENT = 'wg-tg-monitor'

def setup():
    with CronTab(user=True) as cron:
        cron.remove_all(comment=COMMENT)
    scripts_directory_path = Path("./")
    files = list(scripts_directory_path.glob("channel.py"))
    with CronTab(user=True) as cron:
        for file in files:
            command = f"cd {file.parent.absolute()} && python3 {str(file.absolute())} >>{file.parent.parent.absolute()}/data/crontab.log 2>&1"
            print(command)
            job = cron.new(command=command, comment=COMMENT)
            job.setall("*/5 * * * *")


if __name__ == "__main__":
    setup()
    
