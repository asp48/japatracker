WHATSAPP_WEB_URL = "https://web.whatsapp.com"

# Xpath
CHATS_SELECT_PATH = "//div[@data-testid='chat-list']//div[@role='listitem']"
CONVERSATION_MSGS_XPATH = "//div[@data-testid='conversation-panel-messages']"
MSG_CONTAINER_XPATH = "//div[@role='row']//div[@data-testid='msg-container']"

# File Constants
FILE_DATE_TIME_FORMAT = "%d-%m-%Y_%H:%M:%S"
DEFAULT_SHEET_NAME = "Sheet1"
RAW_FILE_PREFIX = "raw_japa_entries"
PROCESSED_SUB_SHEET = "processed"
UNPROCESSED_SUB_SHEET = "unprocessed"
METRICS_REPORT_PREFIX = "metrics_report"
RAW_METRICS_PREFIX = "raw_metrics"
CHECKPOINT_FILE_PREFIX = "checkpoint"

# DateTimeFormats
WHATSAPP_TIMESTAMP_FORMAT = "%I:%M %p, %d/%m/%Y"
MSG_DATE_TIME_FORMAT = "%d-%m-%Y %H:%M:%S"

# Metrics
MSG_READ_COUNT = "msgs_read"
VALID_MSG_COUNT = "valid_msg_count"
JAPA_ENTRIES_COUNT = "japa_entries_count"
UNIQUE_CONTRIBUTOR_COUNT = "unique_contributor_count"
CURRENT_JAPA_COUNT = "current_japa_count"
TOTAL_JAPA_COUNT = "total_japa_count"
COMPLETION_PERCENTAGE = "completion_percentage"
DEVIATION_PERCENTAGE = "deviation_percentage"

# Targets
JAPA_YAGA_START_DATE = "01-07-2023"
JAPA_YAGA_TARGET_COUNT = 325000
JAPA_YAGA_DURATION = 90
