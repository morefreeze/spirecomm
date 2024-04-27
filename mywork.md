
# my

## log

### Unable to create file

```log
2024-04-27 20:23:59,069 - ERROR - scraping.py:90 - Unable to create file: H:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\gameData\THE_SILENT\cards.json
2024-04-27 20:23:59,070 - ERROR - scraping.py:90 - Unable to create file: H:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\gameData\THE_SILENT\relics.json
2024-04-27 20:23:59,071 - ERROR - scraping.py:90 - Unable to create file: H:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\gameData\THE_SILENT\potions.json
2024-04-27 20:23:59,072 - ERROR - scraping.py:90 - Unable to create file: H:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\gameData\monsters.json
2024-04-27 20:23:59,077 - ERROR - scraping.py:90 - Unable to create file: H:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\gameData\events.json
2024-04-27 20:23:59,078 - ERROR - scraping.py:90 - Unable to create file: H:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\gameData\THE_SILENT\cards.json
2024-04-27 20:23:59,078 - ERROR - scraping.py:90 - Unable to create file: H:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\gameData\THE_SILENT\relics.json
2024-04-27 20:23:59,079 - ERROR - scraping.py:90 - Unable to create file: H:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\gameData\THE_SILENT\potions.json
2024-04-27 20:23:59,080 - ERROR - scraping.py:90 - Unable to create file: H:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\gameData\monsters.json
2024-04-27 20:23:59,080 - ERROR - scraping.py:90 - Unable to create file: H:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\gameData\events.json
2024-04-27 20:23:59,081 - ERROR - scraping.py:90 - Unable to create file: H:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\gameData\DEFECT\cards.json
2024-04-27 20:23:59,085 - ERROR - scraping.py:90 - Unable to create file: H:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\gameData\DEFECT\relics.json
2024-04-27 20:23:59,090 - ERROR - scraping.py:90 - Unable to create file: H:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\gameData\DEFECT\potions.json
2024-04-27 20:23:59,094 - ERROR - scraping.py:90 - Unable to create file: H:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\gameData\monsters.json
2024-04-27 20:23:59,094 - ERROR - scraping.py:90 - Unable to create file: H:\Program Files (x86)\Steam\steamapps\common\SlayTheSpire\gameData\events.json
```

I need fix these create failed error. because `os.mknod` report `module 'os' has no attribute 'mknod'`,
I simply comment this line to solve it and no idea why it need create file before `open(file, 'w')`.

### boto3 cannot connect proxy

```log
Failed to connect to proxy URL: "http://127.0.0.1:7890"
```

I add code that disable os env variable

```py
import os
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
```

### No credentials

No surprise I got this because the code invoke another boto3 service which belongs author.

```log
botocore.exceptions.NoCredentialsError: Unable to locate credentials
```

I'm going to try to connect local llm, but it cost about 10 seconds to take one action and some
decision is obviously wrong(like end turn even player has some actions).
