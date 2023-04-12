# yt-channel-comment-analysis

### Background
For channels whose growth stagnates, Collab can help them to overcome it with data analysis like creator report and comment analysis report.

### Objective
- To monitor the reaction of viewers of the channel in detail
- To give insights about how the channel should go to meet viewers' needs
- To monitor the comments on competitors' channels

### Running Instruction
1. Download service account json file from GCP - use `ADD KEY`
2. Make `.env` file
```commandline
PROJECT_ID=
CREDENTIAL_BUCKET=
CREDENTIAL_FILE=
CLIENT_SECRET_FILE={the file path of json file downloaded at the first step}
GCP_BUCKET=
LOCAL_BASE_PATH=
GCP_BASE_PATH=
PRESENTATION_ID=
```
3. Run `main.py`
- Channel ID: ID starting with "UC"
- Start Date: Format %Y%m%d ex. 20230401
