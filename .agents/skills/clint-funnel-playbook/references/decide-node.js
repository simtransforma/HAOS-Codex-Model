// Decide node (n8n Code, Run Once for Each Item) - esqueleto reutilizavel
// =====================================================================
// Papel: a partir do contato achado (Busca Contato) e dos deals dele (Busca Deals),
// decidir se cria, move ou para. Emite um objeto plano que as branches consomem.
//
// Saida (campos estaveis nos 2 caminhos, create e move):
//   contact_id   : id do contato no Clint (null se ainda nao existe -> Cria Deal cria)
//   jaExiste     : ja existe deal NESTA suborigem?
//   deal_id      : id do deal desta suborigem (null se nao existe)
//   deal_status  : status do deal desta suborigem ("OPEN" | "WON" | ...)
//   should_move  : existe && esta OPEN  -> MOVE pro stage da plataforma do evento
//   won_targets  : ids de deals em suborigens ANTERIORES pra marcar WON (dar ganho)
//
// AJUSTAR por branch:
//   ORIGIN_ID            = origin_id desta suborigem (o evento desta branch)
//   PREVIOUS_ORIGIN_IDS  = suborigens anteriores que devem virar ganho ao avancar
//
// Premissas de input (renomeie conforme os nomes dos seus nodes):
//   - node "Busca Contato" retornou o contato (ou vazio)
//   - node "Busca Deals" retornou a lista de deals do contato (ou vazio)
// Use $items()/$node("...") conforme sua topologia; abaixo um padrao defensivo.

const ORIGIN_ID = 'PREENCHER-origin-desta-suborigem';
const PREVIOUS_ORIGIN_IDS = [
  // ex.: Carrinho, Gerou, Negada (as que existirem ANTES desta etapa)
];

// --- ler contato (defensivo: pode nao ter vindo) ---
let contact = null;
try {
  const c = $node['Busca Contato'].json;
  // a API costuma devolver { data: [...] } ou { data: {...} }
  if (c && c.data) contact = Array.isArray(c.data) ? (c.data[0] || null) : c.data;
} catch (e) { contact = null; }

const contact_id = contact ? (contact.id || null) : null;

// --- ler deals do contato ---
let deals = [];
try {
  const d = $node['Busca Deals'].json;
  if (d && Array.isArray(d.data)) deals = d.data;
  else if (Array.isArray(d)) deals = d;
} catch (e) { deals = []; }

// --- deal desta suborigem ---
const dealHere = deals.find(x => x && x.origin_id === ORIGIN_ID) || null;
const jaExiste = !!dealHere;
const deal_id = dealHere ? dealHere.id : null;
const deal_status = dealHere ? (dealHere.status || 'OPEN') : null;

// upsert-move: so move se existe E esta aberto. WON nao move.
const should_move = jaExiste && deal_status === 'OPEN';

// dar ganho: deals das suborigens anteriores que ainda nao estao WON
const won_targets = deals
  .filter(x => x && PREVIOUS_ORIGIN_IDS.includes(x.origin_id) && x.status !== 'WON')
  .map(x => x.id);

return [{
  json: {
    contact_id,
    jaExiste,
    deal_id,
    deal_status,
    should_move,
    won_targets,
  },
}];

