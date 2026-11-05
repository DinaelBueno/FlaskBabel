document.getElementById("form-cadastro").addEventListener("submit", async (e) => {
  e.preventDefault();
  const msg = document.getElementById("mensagem");
  msg.textContent = "";
  msg.className = "msg";

  ["nome", "quantidade", "valor"].forEach(c => {
    document.getElementById("erro-" + c).textContent = "";
  });

  const nome = document.getElementById("nome").value.trim();
  const quantidade = document.getElementById("quantidade").value;
  const valor = document.getElementById("valor").value;

  /* ── Validação client-side espelhando WTForms ── */
  let valido = true;
  if (!nome) {
    document.getElementById("erro-nome").textContent = window.i18n.required;
    valido = false;
  }
  if (quantidade !== "" && Number(quantidade) < 0) {
    document.getElementById("erro-quantidade").textContent = window.i18n.minimum;
    valido = false;
  }
  if (valor !== "" && Number(valor) < 0) {
    document.getElementById("erro-valor").textContent = window.i18n.minimum;
    valido = false;
  }
  if (!valido) return;

  const body = {
    nome: nome,
    quantidade: quantidade === "" ? 0 : Number(quantidade),
    valor: valor === "" ? 0.0 : Number(valor)
  };

  try {
    const res = await fetch("/api/items/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    const data = await res.json();

    if (res.ok) {
      msg.className = "msg ok";
      msg.textContent = window.i18n.item_created.replace("{name}", data.nome);
      document.getElementById("form-cadastro").reset();
    } else {
      msg.className = "msg err";
      msg.textContent = res.status === 409
        ? window.i18n.item_exists
        : data.message || data.erro || window.i18n.create_error;
    }
  } catch (err) {
    msg.className = "msg err";
    msg.textContent = window.i18n.connection_error;
  }
});
