# flake8: noqa

from app.schemas.languages import Languages

ERROR_GENERIC = {
    Languages.EN: """
        I'm really sorry I can't give you a clear answer right now.
    """,
    Languages.PL: """
        Naprawdę mi przykro, że nie mogę teraz udzielić Ci jednoznacznej odpowiedzi.
    """,
    Languages.ES: """
        Lamento mucho no poder darte una respuesta clara en este momento.
    """,
    Languages.DE: """
        Es tut mir wirklich leid, dass ich dir im Moment keine klare Antwort geben kann.
    """,
}

REFUSAL_GENERIC = {
    Languages.EN: """
        I'm really sorry, but I’m not able to respond to your message. {refusal_reason}
    """,
    Languages.PL: """
        Bardzo przepraszam, ale nie mogę odpowiedzieć na Twoją wiadomość. {refusal_reason}
    """,
    Languages.ES: """
        Lo siento mucho, pero no puedo responder a tu mensaje. {refusal_reason}
    """,
    Languages.DE: """
        Es tut mir wirklich leid, aber ich kann auf deine Nachricht nicht antworten. {refusal_reason}
    """,
}
