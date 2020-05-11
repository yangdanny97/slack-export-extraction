import os
import json
from typing import Dict, List, Tuple, Any, Callable

Message = Dict[str, Any]
Channel = Dict[str, Any]
User = Dict[str, Any]


class Slack:
    def __init__(self, data_dir: str):
        self.users = None
        # set up users
        with open(data_dir + "/users.json") as f:
            self.users = json.load(f)
        with open(data_dir + "/channels.json") as f:
            self.channels = json.load(f)
        self.messages = {}
        # set up channels
        for subdir, dirs, files in os.walk(data_dir):
            for channel in dirs:
                self.messages[channel] = {}
            for fname in files:
                if fname in ["integration_logs.json", "users.json", "channels.json"] or not fname.endswith(".json"):
                    continue
                path = os.path.join(subdir, fname)
                s = path.split("/")
                cname = s[-2]
                date = fname.split(".")[-2]
                messages = []
                with open(path, "r") as f:
                    try:
                        messages = json.load(f)
                    except:
                        print("error: "+path)
                for m in messages:
                    m["date"] = date
                    m["channel"] = cname
                self.messages[cname][date] = messages

    def get_messages(self, channel=None) -> List[Message]:
        m = []
        if channel is None:
            for c in self.messages:
                for d in self.messages[c]:
                    m += self.messages[c][d]
        else:
            for d in self.messages[channel]:
                m += self.messages[c][d]
        return m

    def get_filtered_messages(self, filter_func: Callable[[Message], bool], channel=None) -> List[Message]:
        msgs = self.get_messages(channel)
        return [m for m in msgs if filter_func(m)]

    def get_messages_by_date(self, y: int, m: int, d: int) -> List[Message]:
        month = str(m) if m >= 10 else "0"+str(m)
        day = str(d) if d >= 10 else "0"+str(d)
        date = "{}-{}-{}".format(str(y), month, day)
        return self.get_filtered_messages(lambda m: m['date'] == date)

    def get_messages_by_datestring(self, date: str) -> List[Message]:
        return self.get_filtered_messages(lambda m: m['date'] == date)

    def get_messages_by_datestring_prefix(self, date: str) -> List[Message]:
        return self.get_filtered_messages(lambda m: m['date'].startswith(date))

    def get_messages_by_user(self, user: str) -> List[Message]:
        return self.get_filtered_messages(lambda m: 'user' in m and m['user'] == user)

    def get_channel_names(self) -> List[str]:
        return [c["name"] for c in self.channels]

    def get_user_ids(self) -> List[str]:
        return [u["id"] for u in self.users]
