from ..base import DP
from ..surveys import Question, FREE_ANSWER
import database.tasks as db
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, ReplyKeyboardRemove


@DP.message_handler(state=Question.STATES, content_types=ContentType.ANY)
async def processor(message: Message, state: FSMContext):
    survey_id = (await state.get_data())["survey_id"]
    current_question = Question.for_state(await state.get_state())
    if not message.text:
        await message.reply("🤷 Ответить можно только текстовым сообщением")
        await current_question.send(message.from_user.id)
        return
    if message.text == FREE_ANSWER:
        await message.reply("Пожалуйста, поясните, что именно:", reply_markup=ReplyKeyboardRemove())
        return
    try:
        next_question = current_question.for_answer(message.text)
    except ValueError:
        await message.reply("😔 Извините, не смог распознать Ваш ответ, попробуйте заново")
        await current_question.send(message.from_user.id)
        return
    db.question_answer.append_question_answer(
        survey_id=survey_id,
        question=current_question.question,
        local_number=current_question.question_number,
        answer=message.text,
    )
    if not next_question:
        await message.reply(
            "Это был завершающий вопрос. Спасибо за уделённое время ❣️", reply_markup=ReplyKeyboardRemove(),
        )
        await state.finish()
    else:
        await next_question.send(message.from_user.id)
