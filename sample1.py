# -*- coding: utf-8 -*-
#you can get $accountid from https://account.console.aliyun.com/#/secure
#you can get $accid and $acckey from https://ak-console.aliyun.com/#/accesskey
#you can generate $endpoint: http://$accountid.mns.cn-hangzhou.aliyuncs.com, eg. http://1234567890123456.mns.cn-hangzhou.aliyuncs.com
import sys
import time
from mns.account import Account
from mns.queue import *
from mns.topic import *
from mns.subscription import *
import ConfigParser

my_account = Account("http://1037980991456445.mns.cn-hangzhou.aliyuncs.com/", "LTAI1waLaAYoSvm7", "Lt4u9GsiTCn9RVE7ITCE7crestypvH")
topic_name = "sms.topic-cn-hangzhou"
my_topic = my_account.get_topic(topic_name)
#attributes for Mail
#direct_mail = DirectMailInfo(account_name="direct_mail_account_name@aliyun-inc.com", subject="TestMailSubject", address_type=0, is_html=0, reply_to_address=0)
#attributes for SMS
direct_sms_attr1 = DirectSMSInfo(free_sign_name="故指通知", template_code="SMS_51620020", single=False)
direct_sms_attr1.add_receiver(receiver="15056978947", params={"linename": "Tom" ,"devicename": "001" ,"message": "duanlu"})
#direct_sms.add_receiver(receiver="$phone2", params={"name": "David"})
#init TopicMessage
msg_body = "I am test message."
msg = TopicMessage(msg_body, direct_sms=direct_sms_attr1)
try:
    re_msg = my_topic.publish_message(msg)
    print "Publish Message Succeed. MessageBody:%s MessageID:%s" % (msg_body, re_msg.message_id)
except MNSExceptionBase,e:
    if e.type == "TopicNotExist":
        print "Topic not exist, please create it."
        sys.exit(1)
    print "Publish Message Fail. Exception:%s" % e
