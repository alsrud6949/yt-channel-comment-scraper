# yt-channel-comment-analysis

### Background
For channels whose growth stagnates, comment analysis can help them to overcome it, capturing what viewers or subscribers like or dislike.

### Objective
- To monitor the reaction of viewers of the channel in detail
- To give insights about how the channel should go to meet viewers' needs
- To monitor the comments on competitors' channels

### Running Instruction
1. Download service account json file from GCP - use `ADD KEY`
2. Make `.env` file
```commandline
CLIENT_SECRET_FILE={the file path of json file downloaded at the first step}
```
3. Run `main.py`
- Channel ID: ID starting with "UC"
- Start Date: Format %Y%m%d ex. 20230401
