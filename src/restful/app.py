from flask import Flask, redirect, request, session, url_for
from flask_babel import Babel, gettext as _
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///itens.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"
app.config["BABEL_DEFAULT_LOCALE"] = "pt"
app.config["BABEL_SUPPORTED_LOCALES"] = ["pt", "en"]

# Configurações do OpenAPI / Swagger UI para o Flask-smorest
app.config["API_TITLE"] = "API de Itens"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


def get_locale():
    idiomas_suportados = app.config["BABEL_SUPPORTED_LOCALES"]
    idioma_sessao = session.get("lang")
    if idioma_sessao in idiomas_suportados:
        return idioma_sessao
    return (
        request.accept_languages.best_match(idiomas_suportados)
        or app.config["BABEL_DEFAULT_LOCALE"]
    )


babel = Babel(app, locale_selector=get_locale)
db = SQLAlchemy(app)
api = Api(app)

# Registro do Blueprint de API
from restful.api_routes import blp as items_blueprint

api.register_blueprint(items_blueprint)


@app.context_processor
def inject_language_context():
    return {
        "get_locale": get_locale,
        "i18n": {
            "required": _("O nome é obrigatório."),
            "minimum": _("Valor mínimo: 0"),
            "search_minimum": _("Digite ao menos 3 letras"),
            "item_created": _('Item "{name}" cadastrado com sucesso!'),
            "item_updated": _("Item atualizado com sucesso."),
            "create_error": _("Erro ao cadastrar."),
            "update_error": _("Erro ao atualizar."),
            "connection_error": _("Erro de conexão."),
            "item_exists": _("Já existe um item com esse nome."),
            "delete_confirmation": _("Tem certeza que deseja excluir este item?"),
            "delete_error": _("Erro ao deletar."),
        },
    }


@app.route("/mudar-idioma/<lang>")
def mudar_idioma(lang):
    if lang in app.config["BABEL_SUPPORTED_LOCALES"]:
        session["lang"] = lang
    return redirect(request.referrer or url_for("pagina_cadastro"))


import route
