let tempoEspera;

async function autocompletar () {
  clearTimeout(tempoEspera);
  const termo = document.getElementById("busca").value.trim();
  const lista = document.getElementById("sugestoes");
  const erro = document.getElementById("erro-busca");
  erro.textContent = "";

  if (termo.length < 3) {
    lista.classList.add("hidden");
    lista.innerHTML = "";
    if (termo.length > 0) {
      erro.textContent = window.i18n.search_minimum;
    }
    return;
  }
  console.log("Digitando");
  tempoEspera = setTimeout(async () => {
    try {
      const res = await fetch(`/api/items/?search=${encodeURIComponent(termo)}`);
      if (!res.ok) throw new Error("Falha na busca dos itens.");
      const itens = await res.json();

      lista.innerHTML = "";
      if (itens.length === 0) {
        lista.classList.add("hidden");
        return;
      }

      itens.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item.nome;
        li.className = "px-3 py-2 cursor-pointer hover:bg-blue-50 text-gray-700 text-sm";
        li.onclick = () => carregarItem(item.id, item.nome);
        lista.appendChild(li);
      });
      lista.classList.remove("hidden");
    } catch (err) {
      lista.classList.add("hidden");
      const msg = document.getElementById("mensagem");
      msg.className = "msg err";
      msg.textContent = window.i18n.connection_error;
    }
  }, 500);
}

/* Autocomplete  */
document.getElementById("busca").addEventListener("input", autocompletar);

/* Carregar dados do item */
async function carregarItem(id, nome) {
  document.getElementById("sugestoes").classList.add("hidden");
  document.getElementById("busca").value = nome;

  try {
    const res = await fetch(`/api/items/${id}`);
    if (!res.ok) throw new Error("Falha ao carregar o item.");
    const item = await res.json();

    document.getElementById("item_id").value = item.id;
    document.getElementById("nome").value = item.nome;
    document.getElementById("quantidade").value = item.quantidade;
    document.getElementById("valor").value = item.valor;
    document.getElementById("formulario-edicao").classList.remove("hidden");
    document.getElementById("mensagem").className = "msg";
  } catch (err) {
    const msg = document.getElementById("mensagem");
    msg.className = "msg err";
    msg.textContent = window.i18n.connection_error;
  }
}

/*  Validação client-side */
function validarEdicao() {
  let valido = true;
  ["nome", "quantidade", "valor"].forEach(c => {
    document.getElementById("erro-" + c).textContent = "";
  });

  const nome = document.getElementById("nome").value.trim();
  const qtd = document.getElementById("quantidade").value;
  const val = document.getElementById("valor").value;

  if (!nome) {
    document.getElementById("erro-nome").textContent = window.i18n.required;
    valido = false;
  }
  if (qtd !== "" && Number(qtd) < 0) {
    document.getElementById("erro-quantidade").textContent = window.i18n.minimum;
    valido = false;
  }
  if (val !== "" && Number(val) < 0) {
    document.getElementById("erro-valor").textContent = window.i18n.minimum;
    valido = false;
  }
  return valido;
}

/* Atualizar (PUT) */
document.getElementById("btn-atualizar").addEventListener("click", async (e) => {
  e.preventDefault();
  if (!validarEdicao()) return;

  const id = document.getElementById("item_id").value;
  const msg = document.getElementById("mensagem");
  const body = {
    nome: document.getElementById("nome").value.trim(),
    quantidade: Number(document.getElementById("quantidade").value || 0),
    valor: Number(document.getElementById("valor").value || 0),
  };

  try {
    const res = await fetch(`/api/items/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();

    if (res.ok) {
      msg.className = "msg ok";
      msg.textContent = window.i18n.item_updated;
      document.getElementById("busca").value = data.nome;
    } else {
      msg.className = "msg err";
      msg.textContent = res.status === 409
        ? window.i18n.item_exists
        : data.message || data.erro || window.i18n.update_error;
    }
  } catch (err) {
    msg.className = "msg err";
    msg.textContent = window.i18n.connection_error;
  }
});

/*  Deletar (DELETE) */
document.getElementById("btn-deletar").addEventListener("click", async (e) => {
  e.preventDefault();
  if (!confirm(window.i18n.delete_confirmation)) return;

  const id = document.getElementById("item_id").value;
  const msg = document.getElementById("mensagem");

  try {
    const res = await fetch(`/api/items/${id}`, { method: "DELETE" });
    const data = await res.json();

    if (res.ok) {
      msg.className = "msg ok";
      msg.textContent = data.mensagem;
      document.getElementById("formulario-edicao").classList.add("hidden");
      document.getElementById("busca").value = "";
    } else {
      msg.className = "msg err";
      msg.textContent = data.message || data.erro || window.i18n.delete_error;
    }
  } catch (err) {
    msg.className = "msg err";
    msg.textContent = window.i18n.connection_error;
  }
});
