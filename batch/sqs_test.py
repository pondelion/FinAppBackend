import sys
sys.path.append('..')
import json

from fin_app.notification.sqs_polling import (
    SQSPolling,
    SlackMessage
)


s = SQSPolling()

res = s.push_message(
    message=SlackMessage(message='testes', channel='finapp')
)
print(res)