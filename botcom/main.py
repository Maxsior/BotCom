import logging
import uvicorn
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import PlainTextResponse
from fastapi.exception_handlers import http_exception_handler
from typing import Optional, Any
from entities import Message
import entities.keyboards as keyboards
from messengers import Messenger
from storage import Storage
import commands

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)-15s] %(levelname)s %(filename)s:%(lineno)d | %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()


@app.exception_handler(HTTPException)
async def immediately_response_handler(request, exc):
    if exc.status_code == 200:
        return PlainTextResponse(exc.detail, status_code=exc.status_code)
    return await http_exception_handler(request, exc)


@app.post('/{messenger}')
def main(messenger: str, data: Any = Body(...)):
    """post your data"""
    messenger_from = Messenger.get_instance(messenger)

    if messenger_from is None:
        raise HTTPException(status_code=404, detail="Unknown messenger")

    logger.info('Parsing the message')

    msg: Optional[Message] = messenger_from.parse(data)

    if msg is None:
        logger.info('Not new message')
        return PlainTextResponse('ok')

    logger.info('Message was parsed successfully')

    if not msg.sender.registered:
        logger.info('Registering user')
        msg.sender.key = Storage().add_user(msg.sender)
        logger.info('Sending welcome message')
        messenger_from.send(
            msg.sender.id,
            Message('MESSAGE.REGISTER').localize(msg.sender.lang),
            keyboards.ConnectKeyboard(msg.sender)
        )

        if msg.cmd is None:
            return PlainTextResponse('ok')

    if msg.cmd is not None:
        logger.info('Command detected')
        cmd_class = commands.get_class(msg.cmd.name)
        logger.info('Executing command')
        cmd_class(msg).execute()
        return PlainTextResponse('ok')

    if msg.sender.receiver is None:
        logger.info('No receiver')
        messenger_from.send(
            msg.sender.id,
            Message('MESSAGE.NO_RECIPIENT').localize(msg.sender.lang),
            keyboards.ConnectKeyboard(msg.sender)
        )
        return PlainTextResponse('ok')

    logger.info('Getting receiver')
    receiver = Storage().get_user(msg.sender.receiver)
    if receiver.receiver != msg.sender.key:
        logger.info('Receiver does not confirm the connection')
        messenger_from.send(
            msg.sender.id,
            Message('MESSAGE.CONN_WAIT').localize(msg.sender.lang,
                                                  name=receiver.name,
                                                  messenger=receiver.messenger),
            keyboards.ConnectKeyboard(msg.sender)
        )
        return PlainTextResponse('ok')

    logger.info('Getting receiver messenger instance')
    messenger_to = Messenger.get_instance(receiver.messenger)
    logger.info('Forwarding')
    messenger_to.send(
        receiver.id,
        Message('MESSAGE.TEMPLATE', msg.attachments).localize('', name=msg.sender.name, msg=msg.text),
        keyboards.ConnectKeyboard(receiver)
    )

    return PlainTextResponse('ok')


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    uvicorn.run('botcom.main:app', host="0.0.0.0", port=8000, reload=True)
