from config import keys


def send_message():
    pass


def parse(data):
    data_type = data['type']
    if data_type == 'message_new':
        return {
            'uid': data['user_id'],
            'msg': data['body']
        }
    elif data_type == 'confirmation':
        if data['group_id'] == 176977577:
            return '894adea0'
        else:
            return ''
