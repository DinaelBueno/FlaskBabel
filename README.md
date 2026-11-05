# Flask-Smorest Prova

Aplicação de cadastro e consulta de itens com interface em português e inglês,
usando Flask-Babel.

## Executar

Instale as dependências do projeto e inicie a aplicação:

```powershell
uv sync
uv run python src/restful/run.py
```

O idioma pode ser alternado no menu da aplicação. A escolha fica salva na
sessão; antes de uma escolha, o idioma do navegador é usado, com português como
opção padrão.

## Atualizar traduções

Com `uv sync` concluído, extraia as mensagens e compile o catálogo:

```powershell
uv run pybabel extract -F babel.cfg -k _l -o messages.pot .
uv run pybabel update -i messages.pot -d src/restful/translations -l en
uv run pybabel compile -d src/restful/translations
```