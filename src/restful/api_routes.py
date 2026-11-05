from flask.views import MethodView
from flask_babel import gettext as _
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields, validate
from sqlalchemy.exc import IntegrityError

from app import db
from model import Item

blp = Blueprint(
    "items",
    "items",
    url_prefix="/api/items",
    description="Operações RESTful sobre itens",
)


# ── Schemas de Validação e Serialização ──
class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    quantidade = fields.Int(load_default=0, validate=validate.Range(min=0))
    valor = fields.Float(load_default=0.0, validate=validate.Range(min=0))


class ItemUpdateSchema(Schema):
    nome = fields.Str(validate=validate.Length(min=1, max=120))
    quantidade = fields.Int(validate=validate.Range(min=0))
    valor = fields.Float(validate=validate.Range(min=0))


class ItemQuerySchema(Schema):
    search = fields.Str(load_default="")


# ── Classes RESTful (MethodViews) ──
@blp.route("/")
class ListaItens(MethodView):
    @blp.arguments(ItemQuerySchema, location="query")
    @blp.response(200, ItemSchema(many=True))
    def get(self, args):
        termo = args.get("search", "").strip()
        if len(termo) < 3:
            return []
        return Item.query.filter(Item.nome.ilike(f"%{termo}%")).all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        nome = item_data["nome"].strip()
        if not nome:
            abort(422, message=_("O nome é obrigatório."))
        if Item.query.filter_by(nome=nome).first():
            abort(409, message=_("Já existe um item com esse nome."))

        item = Item(
            nome=nome,
            quantidade=item_data["quantidade"],
            valor=item_data["valor"],
        )
        db.session.add(item)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(409, message=_("Já existe um item com esse nome."))
        return item


@blp.route("/<int:item_id>")
class ItemTela(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        return Item.query.get_or_404(item_id)

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = Item.query.get_or_404(item_id)

        if "nome" in item_data:
            nome = item_data["nome"].strip()
            if not nome:
                abort(422, message=_("O nome é obrigatório."))
            duplicate = Item.query.filter(
                Item.nome == nome,
                Item.id != item_id,
            ).first()
            if duplicate:
                abort(409, message=_("Já existe um item com esse nome."))
            item.nome = nome
        if "quantidade" in item_data:
            item.quantidade = item_data["quantidade"]
        if "valor" in item_data:
            item.valor = item_data["valor"]

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(409, message=_("Já existe um item com esse nome."))
        return item

    @blp.response(200)
    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"mensagem": _("Item removido com sucesso.")}