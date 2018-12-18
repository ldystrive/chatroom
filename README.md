# chatroom

支持聊天室聊天与用户和用户聊天

##Client

+ ```login(name)``` : 登录，不能使用其他人已经使用的id，退出登录后，可以使用原ip继续使用该id登录
+ ```chat(name, msg)``` : 聊天，发给其他人消息，或者发送在群里(group)发消息
+ ```update``` : 获取所有人的id
+ ```listen``` :监听是否有从服务器传来的消息，可能是收到的别人的消息或者update的列表
+ ```recv``` : 当受到聊天消息后，会调用该函数来处理。有三个参数：聊天窗口、发消息的用户id和消息内容
+ ```send``` : 可以通过该函数给其他用户发送消息，若聊天对象为group，就是发送给大聊天室