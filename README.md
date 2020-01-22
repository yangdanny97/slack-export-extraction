# slack-export-extraction

Simple module that reads Slack public data exports into a data structure for easy preprocessing and manipulation. Get messages by user, channel, date (year/month granularity supported), custom filter functions are supported. See `slack_extract.py` for documentation of fields and methods.

# Usage Instructions:
1. Put this file into the same directory as the notebook or file you're using for analysis.
2. Put the slack data export files into `/data` under that directory (messages for channel MyChannel would be in `/data/MyChannel`).
3. `from slack_extract import Data` to import
4. `slack = Data()` will read the files and initialize the data structure. 
5. Ex: To list all messages sent in August 2018, `slack.get_messages_by_datestring_prefix("2018-08")`

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
