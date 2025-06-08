from ..base import Question, Surveys, FREE_ANSWER


e = Question(
    question="Что, по Вашему мнению, помогает поддерживать атмосферу в коллективе или, наоборот, требует улучшения?",
    question_number=5,
    options={
        FREE_ANSWER: None,
    }
)
d1 = Question(
    question="Часто ли конфликты остаются неразрешёнными?",
    question_number=4,
    options={
        "Да": e,
        "Нет": e,
    }
)
d2 = Question(
    question="Недопонимание возникает чаще из-за нечетких задач/процедур или из-за стиля общения?",
    question_number=4,
    options={
        "Нечеткие задачи": e,
        "Стиль общения": e,
    }
)
d3 = Question(
    question="Что мешает более активному общению в коллективе?",
    question_number=4,
    options={
        "Нет времени/места": e,
        "Нет инициативы": e,
        "Разные отделы": e,
        "Атмосфера не способствует": e,
    }
)
d4 = Question(
    question="Что бы Вы хотели изменить в коллективе?",
    question_number=4,
    options={
        FREE_ANSWER: e,
    }
)
d5 = Question(
    question="Есть ли у вас возможность обсудить трудности с руководством?",
    question_number=4,
    options={
        "Да": e,
        "Нет": e,
    }
)
d6 = Question(
    question="Что мешает ощущать поддержку со стороны руководства?",
    question_number=4,
    options={
        "Недостаток общения": e,
        "Недоверие": e,
        "Необъективность": e,
        FREE_ANSWER: e,
    }
)
c1 = Question(
    question="С какими трудностями Вы чаще всего сталкиваетесь?",
    question_number=3,
    options={
        "Конфликты": d1,
        "Недопонимание": d2,
        "Недостаток общения": d3,
        FREE_ANSWER: d4,
    }
)
c2 = Question(
    question="Чаще всего Вы чувствуете себя комфортно в коллективе?",
    question_number=3,
    options={
        "Да": e,
        "Нет": d4,
    }
)
c3 = Question(
    question="Считаете ли вы, что причина в личных отношениях или в общей атмосфере?",
    question_number=3,
    options={
        "Личные отношения": d5,
        "Общая атмосфера": e,
        "Трудно сказать": e,
    }
)
c4 = Question(
    question="Поддержка со стороны руководства ощущается так же, как со стороны коллег?\n\n<i>1 — совсем не ощущается, 5 — полностью ощущается</i>",
    question_number=3,
    options={
        "1": d6,
        "2": d6,
        "3": e,
        "4": e,
        "5": e,
    }
)
b1 = Question(
    question="Испытываете ли Вы трудности во взаимодействии с коллегами?",
    question_number=2,
    options={
        "Да": c1,
        "Нет": c2,
    }
)
b2 = Question(
    question="Чувствуете ли Вы поддержку со стороны коллег?\n\n<i>1 — совсем не чувствую, 5 — всегда чувствую</i>",
    question_number=2,
    options={
        "1": c3,
        "2": c3,
        "3": c4,
        "4": c4,
        "5": c4,
    }
)
a = Question(
    question="Как Вы в целом оцениваете атмосферу в Вашем коллективе?\n\n<i>1 — очень неблагоприятная, 5 — очень благоприятная</i>",
    question_number=1,
    options={
        "1": b1,
        "2": b1,
        "3": b2,
        "4": b2,
        "5": b2,
    }
)
Surveys.register(
    name="TODO",
    survey_id=4,
    first_question=a,
)
