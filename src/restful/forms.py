from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class CadastroForm(FlaskForm):
    nome = StringField(
        _l("Nome"),
        validators=[
            DataRequired(message=_l("O nome é obrigatório.")),
            Length(min=1, max=120, message=_l("O nome deve ter entre 1 e 120 caracteres.")),
        ],
        render_kw={"placeholder": _l("Nome do item")},
    )
    quantidade = IntegerField(
        _l("Quantidade"),
        validators=[Optional(), NumberRange(min=0, message=_l("Valor mínimo: 0"))],
        default=0,
        render_kw={"min": 0},
    )
    valor = FloatField(
        _l("Valor (R$)"),
        validators=[Optional(), NumberRange(min=0.0, message=_l("Valor mínimo: 0"))],
        default=0.0,
        render_kw={"step": "0.01", "min": 0},
    )
    submit = SubmitField(_l("Cadastrar"))


class BuscaForm(FlaskForm):
    busca = StringField(
        _l("Buscar item"),
        validators=[
            DataRequired(message=_l("Informe um item para buscar.")),
            Length(min=3, message=_l("Digite ao menos 3 letras")),
        ],
        render_kw={"autocomplete": "off", "placeholder": _l("Mínimo 3 letras")},
    )


class EdicaoForm(FlaskForm):
    nome = StringField(
        _l("Nome"),
        validators=[
            DataRequired(message=_l("O nome é obrigatório.")),
            Length(min=1, max=120, message=_l("O nome deve ter entre 1 e 120 caracteres.")),
        ],
    )
    quantidade = IntegerField(
        _l("Quantidade"),
        validators=[Optional(), NumberRange(min=0, message=_l("Valor mínimo: 0"))],
        render_kw={"min": 0},
    )
    valor = FloatField(
        _l("Valor (R$)"),
        validators=[Optional(), NumberRange(min=0.0, message=_l("Valor mínimo: 0"))],
        render_kw={"step": "0.01", "min": 0},
    )
    submit_atualizar = SubmitField(_l("Atualizar"))
    submit_deletar = SubmitField(_l("Deletar"))
