# slack-export-extraction

Simple module that reads Slack public data exports into a data structure for easy preprocessing and manipulation. Get messages by user, channel, date (year/month granularity supported), custom filter functions are supported. See `slack_extract.py` for documentation of fields and methods.

# Usage Instructions:
1. Put this file into the same directory as the notebook or file you're using for analysis.
2. `from slack_extract import Slack` to import
3. `slack = Data(dir)` will read the files in directory `dir` and initialize the data structure. 
4. Ex: To list all messages sent in August 2018, `slack.get_messages_by_datestring_prefix("2018-08")`

Note that the directory provided must exactly match the Slack data export format:
- 3 files: integration_logs.json, users.json, channels.json
- 1 subdirectory for each channel, each containing:
    - 1 file for each day of messages (message file for YYYY-MM-DD are named `YYYY-MM-DD.json`).

# Docs:

Attrs:
- `users` - Dict representing `users.json` (see below)
- `channels` - Dict representing `channels.json` (see below)
- `messages` - nested Dict of channel name -> channel messages
    - channel messages - a Dict of date -> list of messages for that date
    - message - a Dict following the message schema (seen below) with added String fields for date and channel for convenience

Methods:
- `get_messages(self, channel=None) -> List[Message]` - get list of all messages from a single channel, or all messages from all channels if a channel isn't provided
- `get_filtered_messages(self, filter_func: Callable[[Message], bool], channel=None) -> List[Message]` - use a custom lambda to return a list of filter messages (also optionally specify a channel)
- `get_messages_by_date(self, y: int, m: int, d: int) -> List[Message]` - list of all messages that were sent on a particular date
- `get_messages_by_datestring(self, date: str) -> List[Message]` - date is in the format YYYY-MM-DD
- `get_messages_by_datestring_prefix(self, date: str) -> List[Message]` - makes it easy to filter by year or month
- `get_messages_by_user(self, user: str) -> List[Message]` - list of all messages sent by a particular user ID
- `get_channel_names(self) -> List[str]` - list of all channel names
- `get_user_ids(self) -> List[str]` - list of user ids

# JSON Schemas

Note: not all fields will be included in each message. There are incomplete official docs [here](https://slack.com/help/articles/220556107-How-to-read-Slack-data-exports) which offer some more detailed explanation of some fields.

### User:
```
{
    "id": str,
    "team_id": str,
    "name": str,
    "deleted": true,
    "profile": {
        "title": str,
        "phone": str,
        "skype": str,
        "real_name": str,
        "real_name_normalized": str,
        "display_name": str,
        "display_name_normalized": str,
        "fields": null,
        "status_text": str,
        "status_emoji": str,
        "status_expiration": int,
        "avatar_hash": str,
        "image_original": str,
        "email": str,
        "first_name": str,
        "last_name": str,
        "image_24": str,
        "image_32": str,
        "image_48": str,
        "image_72": str,
        "image_192": str,
        "image_512": str,
        "image_1024": str,
        "status_text_canonical": str,
        "team": str
    },
    "is_bot": bool,
    "is_app_user": bool,
    "updated": int
}
```

### Channel:
```
{
    "id": str,
    "name": str,
    "created": str,
    "creator": str,
    "is_archived": bool,
    "is_general": bool,
    "members": [str],
    "pins": [
        {
            "id": str,
            "type": str,
            "created": int,
            "user": str,
            "owner": str
        }
    ],
    "topic": {
        "value": str,
        "creator": str,
        "last_set": str
    },
    "purpose": {
        "value": str,
        "creator": str,
        "last_set": str
    }
}
```

### Message:
```
{
    "client_msg_id": str,
    "type": str,
    "text": str,
    "user": str,
    "ts": str,
    "team": str,
    "user_team": str,
    "source_team": str,
    "user_profile": {
        "avatar_hash": str,
        "image_72": str,
        "first_name": str,
        "real_name": str,
        "display_name": str,
        "team": str,
        "name": str,
        "is_restricted": bool,
        "is_ultra_restricted": bool
    },
    "thread_ts": str,
    "parent_user_id": str,
    "reply_count": int,
    "reply_users_count": int,
    "latest_reply": str,
    "reply_users": [str],
    "replies": [
        {
            "user": str,
            "ts": str
        }
    ],
    "subscribed": false,
    "reactions": [
        {
            "name": str,
            "users": [str],
            "count": int
        }
    ]
}
```
