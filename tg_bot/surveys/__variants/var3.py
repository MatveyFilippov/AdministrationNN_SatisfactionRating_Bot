from ..base import Question, Surveys, FREE_ANSWER


h = Question(
    question="Что, по Вашему мнению, помогает поддерживать позитивную культуру в компании?",
    question_number=9,
    options={
        FREE_ANSWER: None,
    }
)
g = Question(
    question="Пожалуйста, опишите, что именно, по Вашему мнению, следует изменить в корпоративной культуре или системе развития.",
    question_number=8,
    options={
        FREE_ANSWER: h,
    }
)
f = Question(
    question="Что, по Вашему мнению, больше всего влияет на атмосферу в коллективе?",
    question_number=7,
    options={
        "Поведение коллег": g,
        "Лидерство руководства": g,
        "Уровень стресса/нагрузки": g,
        "Стиль коммуникации": g,
        "Внутренние мероприятия": g,
        FREE_ANSWER: g,
    }
)
e = Question(
    question="Насколько Вы чувствуете себя принятым и уважаемым в коллективе?\n\n<i> 1 - совершенно не чувствую, 5 - полностью чувствую</i>",
    question_number=6,
    options={
        "1": f,
        "2": f,
        "3": f,
        "4": f,
        "5": f,
    }
)
d = Question(
    question="Насколько, по Вашему мнению, сотрудники в компании действительно следуют заявленным корпоративным ценностям?\n\n<i>1 - совсем не следуют, 5 - полностью следуют</i>",
    question_number=5,
    options={
        "1": e,
        "2": e,
        "3": e,
        "4": e,
        "5": e,
    }
)
c1_1 = Question(
    question="Есть ли у вас понимание того, какие навыки и знания вам нужно развивать для карьерного роста в компании?",
    question_number=4,
    options={
        "Да, полностью": d,
        "Частично": d,
        "Нет": d,
    }
)
c1 = Question(
    question="Чувствуете ли Вы, что компания предоставляет вам достаточно возможностей для профессионального и личного развития?",
    question_number=3,
    options={
        "Да, в полной мере": d,
        "В какой-то степени": d,
        "Нет": c1_1,
        "Затрудняюсь ответить": c1_1,
    }
)
c2 = Question(
    question="Какие формы развития Вы считаете наиболее эффективными для себя?",
    question_number=3,
    options={
        "Обучающие курсы и тренинги": d,
        "Наставничество": d,
        "Внутренние ротации": d,
        "Участие в проектах": d,
        "Конференции/внешнее обучение": d,
        FREE_ANSWER: d,
    }
)
b1 = Question(
    question="Что, по Вашему мнению, мешает вам чувствовать себя вовлечённым в корпоративную культуру?",
    question_number=2,
    options={
        "Недостаток коммуникации от руководства": c1,
        "Отсутствие общих ценностей": c1,
        "Чувство отчуждённости": c1,
        "Отсутствие мероприятий и инициатив": c1,
        FREE_ANSWER: c1,
    }
)
b2 = Question(
    question="Что, по Вашему мнению, особенно способствует сильной корпоративной культуре в компании?",
    question_number=2,
    options={
        "Прозрачная коммуникация": c2,
        "Открытость и доверие": c2,
        "Командные мероприятия": c2,
        "Ценности компании": c2,
        "Поддержка руководства": c2,
        FREE_ANSWER: c2,
    }
)
a = Question(
    question="Насколько Вы удовлетворены корпоративной культурой и возможностями для развития в Вашей компании?\n\n<i> 1 - Совершенно не удовлетворен(а), 5 - Полностью удовлетворе(а)</i>",
    question_number=1,
    options={
        "1": b1,
        "2": b1,
        "3": b1,
        "4": b2,
        "5": b2,
    }
)
Surveys.register(
    name="HR",
    survey_id=3,
    first_question=a,
)
