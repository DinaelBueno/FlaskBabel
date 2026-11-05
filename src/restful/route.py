from flask import render_template

from app import app
from forms import BuscaForm, CadastroForm, EdicaoForm


@app.route("/")
def pagina_cadastro():
    form = CadastroForm()
    return render_template("cadastro.html", form=form)


@app.route("/consulta")
def pagina_consulta():
    busca_form = BuscaForm()
    edicao_form = EdicaoForm()
    return render_template(
        "consulta.html",
        busca_form=busca_form,
        edicao_form=edicao_form,
    )