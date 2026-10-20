// TaskTracker - front-end em JavaScript puro.
// Conversa com a API Flask (/tarefas, /estatisticas) usando fetch().

let todasAsTarefas = [];

// ---------- Utilidades ----------

function $(id) {
  return document.getElementById(id);
}

// Cria um elemento HTML com texto (textContent evita injeção de HTML).
function criar(tag, texto, classe) {
  const el = document.createElement(tag);
  if (texto !== undefined) el.textContent = texto;
  if (classe) el.className = classe;
  return el;
}

function selo(texto, tipo) {
  return criar("span", texto, "selo selo-" + tipo);
}

function tipoPrioridade(prioridade) {
  return { Alta: "alta", "Média": "media", Baixa: "baixa" }[prioridade];
}

function avisar(texto) {
  const aviso = $("aviso");
  aviso.textContent = texto;
  aviso.hidden = false;
  clearTimeout(avisar.timer);
  avisar.timer = setTimeout(() => (aviso.hidden = true), 3000);
}

async function api(caminho, opcoes) {
  const resposta = await fetch(caminho, opcoes);
  const dados = await resposta.json();
  if (!resposta.ok) throw dados.erro || { mensagem: "Erro inesperado." };
  return dados;
}

// ---------- Abas ----------

function mostrarAba(nome) {
  document.querySelectorAll(".aba").forEach((secao) => (secao.hidden = secao.id !== nome));
  document.querySelectorAll(".abas a[data-aba]").forEach((link) =>
    link.classList.toggle("ativa", link.dataset.aba === nome)
  );
}

function abaDoEndereco() {
  return location.hash === "#tarefas" ? "tarefas" : "visao-geral";
}

// ---------- Visão geral ----------

async function carregarVisaoGeral() {
  const e = await api("/estatisticas");
  const p = e.por_prioridade;

  $("hoje").textContent = "Hoje: " + e.hoje;
  $("n-total").textContent = e.total;
  $("d-total").textContent = `${p.Alta.total} alta, ${p["Média"].total} média, ${p.Baixa.total} baixa`;
  $("n-pendentes").textContent = e.pendentes;
  $("n-concluidas").textContent = e.concluidas;
  $("d-concluidas").textContent = e.percentual_concluidas + "%";
  $("n-atrasadas").textContent = e.atrasadas;
  const primeiraAtrasada = e.proximos_prazos.find((t) => t.atrasada);
  $("d-atrasadas").textContent = primeiraAtrasada ? primeiraAtrasada.titulo : "nenhuma";
  $("n-semana").textContent = e.vencem_em_7_dias;

  // Barras por prioridade
  const maior = Math.max(1, ...Object.values(p).map((d) => d.total));
  const barras = $("barras");
  barras.replaceChildren();
  for (const [nome, d] of Object.entries(p)) {
    const linha = criar("div", undefined, "barra-linha");
    linha.append(criar("span", nome, "barra-nome"));
    const trilho = criar("div", undefined, "barra-trilho");
    const pend = criar("div", undefined, "barra barra-pendente");
    pend.style.width = (100 * d.pendentes) / maior + "%";
    const conc = criar("div", undefined, "barra barra-concluida");
    conc.style.width = (100 * d.concluidas) / maior + "%";
    trilho.append(pend, conc);
    linha.append(trilho);
    const partes = [];
    if (d.pendentes) partes.push(d.pendentes + (d.pendentes > 1 ? " pendentes" : " pendente"));
    if (d.concluidas) partes.push(d.concluidas + (d.concluidas > 1 ? " concluídas" : " concluída"));
    linha.append(criar("span", partes.join(", ") || "nenhuma", "barra-texto"));
    barras.append(linha);
  }

  // Próximos prazos
  const lista = $("proximos");
  lista.replaceChildren();
  if (!e.proximos_prazos.length) lista.append(criar("li", "Nenhuma tarefa pendente.", "vazio"));
  for (const t of e.proximos_prazos) {
    const item = criar("li");
    item.append(criar("span", t.data_limite_br.slice(0, 5), "data"));
    const meio = criar("div");
    meio.append(criar("strong", t.titulo), criar("span", t.prazo, t.atrasada ? "prazo perigo" : "prazo"));
    item.append(meio, selo(t.prioridade, tipoPrioridade(t.prioridade)));
    lista.append(item);
  }
}

// ---------- Tarefas ----------

async function carregarTarefas() {
  todasAsTarefas = await api("/tarefas");
  desenharTabela();
}

function desenharTabela() {
  const busca = $("busca").value.trim().toLowerCase();
  const prioridade = $("filtro-prioridade").value;
  const status = $("filtro-status").value;

  const visiveis = todasAsTarefas.filter(
    (t) =>
      (!busca || (t.titulo + " " + t.descricao).toLowerCase().includes(busca)) &&
      (!prioridade || t.prioridade === prioridade) &&
      (!status || t.status === status)
  );

  const pendentes = todasAsTarefas.filter((t) => t.status === "Pendente").length;
  $("resumo-tarefas").textContent =
    `${todasAsTarefas.length} tarefas, ${pendentes} pendentes. Ordenadas pela data limite.`;

  const corpo = $("linhas");
  corpo.replaceChildren();
  for (const t of visiveis) {
    const tr = criar("tr");

    const celTarefa = criar("td");
    celTarefa.append(criar("strong", t.titulo));
    if (t.descricao) celTarefa.append(criar("span", t.descricao, "descricao"));

    const celPrioridade = criar("td");
    celPrioridade.append(selo(t.prioridade, tipoPrioridade(t.prioridade)));

    const celStatus = criar("td");
    celStatus.append(selo(t.status, t.status === "Pendente" ? "pendente" : "concluida"));

    const celAcao = criar("td");
    if (t.status === "Pendente") {
      const botao = criar("button", "Concluir", "botao");
      botao.type = "button";
      botao.addEventListener("click", () => concluir(t.id));
      celAcao.append(botao);
    }

    tr.append(
      celTarefa,
      celPrioridade,
      criar("td", t.data_limite_br, "mono"),
      criar("td", t.prazo, t.atrasada ? "perigo" : ""),
      celStatus,
      celAcao
    );
    corpo.append(tr);
  }
  $("vazio").hidden = visiveis.length > 0;
}

async function concluir(id) {
  try {
    const tarefa = await api(`/tarefas/${id}/concluir`, { method: "PATCH" });
    avisar(`"${tarefa.titulo}" concluída.`);
    await atualizarTudo();
  } catch (erro) {
    avisar(erro.mensagem);
  }
}

async function cadastrar(evento) {
  evento.preventDefault();
  const formulario = evento.target;
  const caixaErro = $("erro-formulario");
  const dados = Object.fromEntries(new FormData(formulario));

  formulario.querySelectorAll(".invalido").forEach((el) => el.classList.remove("invalido"));
  try {
    await api("/tarefas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });
    caixaErro.hidden = true;
    formulario.reset();
    avisar("Tarefa cadastrada com sucesso! Status: Pendente.");
    await atualizarTudo();
  } catch (erro) {
    caixaErro.textContent = erro.mensagem;
    caixaErro.hidden = false;
    const campo = formulario.elements[erro.campo];
    if (campo) {
      campo.classList.add("invalido");
      campo.focus();
    }
  }
}

// ---------- Data limite ----------

// Coloca as barras sozinho enquanto a pessoa digita: 25102026 -> 25/10/2026
function mascaraData(evento) {
  const digitos = evento.target.value.replace(/\D/g, "").slice(0, 8);
  evento.target.value = [digitos.slice(0, 2), digitos.slice(2, 4), digitos.slice(4)]
    .filter(Boolean)
    .join("/");
}

// Abre o calendário do navegador, já posicionado na data digitada (se houver)
function abrirCalendario() {
  const campo = $("formulario").elements.data_limite;
  const calendario = $("calendario");
  const [dia, mes, ano] = campo.value.split("/");
  calendario.value = ano && ano.length === 4 ? `${ano}-${mes}-${dia}` : "";
  if (calendario.showPicker) calendario.showPicker();
  else calendario.click();
}

// Data escolhida no calendário (AAAA-MM-DD) -> campo de texto (DD/MM/AAAA)
function escolherNoCalendario(evento) {
  const [ano, mes, dia] = evento.target.value.split("-");
  if (!ano) return;
  const campo = $("formulario").elements.data_limite;
  campo.value = `${dia}/${mes}/${ano}`;
  campo.classList.remove("invalido");
}

async function atualizarTudo() {
  await Promise.all([carregarVisaoGeral(), carregarTarefas()]);
}

// ---------- Início ----------

document.addEventListener("DOMContentLoaded", () => {
  mostrarAba(abaDoEndereco());
  window.addEventListener("hashchange", () => mostrarAba(abaDoEndereco()));
  document.querySelector("[data-ir-formulario]").addEventListener("click", () =>
    setTimeout(() => document.querySelector("#formulario [name=titulo]").focus(), 0)
  );

  $("formulario").addEventListener("submit", cadastrar);
  $("formulario").elements.data_limite.addEventListener("input", mascaraData);
  $("abrir-calendario").addEventListener("click", abrirCalendario);
  $("calendario").addEventListener("change", escolherNoCalendario);
  ["busca", "filtro-prioridade", "filtro-status"].forEach((id) =>
    $(id).addEventListener("input", desenharTabela)
  );

  atualizarTudo().catch(() => avisar("Não foi possível falar com a API."));
});
