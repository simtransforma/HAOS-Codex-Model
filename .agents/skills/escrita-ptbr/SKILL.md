---
name: escrita-ptbr
description: "Escreve e revisa textos em português do Brasil com qualidade impecável. Une gramática normativa (concordância, regência, crase, colocação pronominal, ortografia do Acordo de 1990, pontuação) com remoção da \"cara de IA\" (gerundismo, translationese, formalismo, clichê) e técnica de copy natural brasileira. Use SEMPRE que for escrever, revisar ou reescrever QUALQUER texto em português: anúncios, e-mails, landing pages, posts, legendas, headlines, CTAs, mensagens, documentos, roteiros. Gatilhos típicos do usuário: \"revisa esse texto\", \"melhora essa copy\", \"tá soando ruim/robótico\", \"escreve em português\", \"corrige a gramática\", \"deixa mais natural\", \"tira a cara de IA\", \"isso tá ruim\", \"concordância\", \"crase\", \"ficou estranho\". Foca em qualidade linguística e naturalidade; para persuasão e estrutura de oferta, combine com a skill copywriting."
---

# Escrita PT-BR: copy impecável e humana

Faça qualquer texto em português do Brasil soar correto, natural e brasileiro. Esta skill junta 3 camadas que normalmente vivem separadas: (1) gramática normativa, (2) remoção da "cara de IA" e da tradução literal, (3) técnica de copy forte. Referências de base: Bechara, Cunha e Cintra, Cegalla, Manual da Folha, Ciberdúvidas.

## Regra inegociável (gate de saída, P0)
NUNCA use o travessão longo (em-dash, código U+2014). Onde ele caberia, use vírgula, dois-pontos, parênteses, ponto ou quebra de linha. Mesma proibição para: o travessão curto (en-dash, U+2013); as reticências em caractere único (U+2026, sempre troque por três pontos comuns: ...); as aspas curvas (use aspas retas "); e o apóstrofo curvo (use o apóstrofo reto '). Antes de entregar, faça uma busca literal por esses caracteres e zere todos. Isto vale para todo texto, sempre.

## Os 3 modos
- REVISAR: aponta os problemas (sem reescrever). Use quando o usuário quer entender o que está errado.
- REESCREVER: aponta e já entrega a versão corrigida. Modo padrão.
- ESCREVER: cria do zero já seguindo todas as regras abaixo.

Em qualquer modo, ao terminar, faça uma 2a passada: releia seu próprio texto e cace o que sobreviveu (sempre sobra algo).

## Travas ao revisar texto dos outros (mudança mínima + marca)
Quando o texto não é seu (revisar copy, e-mail, doc de outra pessoa), siga estas travas:
- Mudança mínima: corrija o ERRO, não o estilo. Não reescreva frase que está correta só porque você diria diferente. Não troque o vocabulário do autor por sinônimo "melhor". Preserve ritmo, tom e personalidade. Na dúvida entre duas formas corretas, mantenha a do autor.
- Preservar placeholders e tokens (NUNCA "corrigir"): não altere, acentue, pluralize nem reformate merge tags e variáveis (%FIRSTNAME%, %EMAIL%, {{nome}}, [[link]]), URLs, domínios, e-mails, código, hashtags, @mentions, IDs, e nomes oficiais de marca/produto/oferta (SIM, ${USER_BRAND}, ${USER_BRAND}, HAU, "Practitioner em PNL ${USER_BRAND}", "369FLIX"). Se um token parecer ter "erro", é proposital: deixe intacto.
- Voz da marca (não enrijecer): respeite o tom de cada marca (SIM = público 55+, acolhedor e simples; ${USER_BRAND} = informal e provocador). Corrija o ERRADO, nunca o INFORMAL-PORÉM-CORRETO. Naturalidade e gentileza vêm antes de purismo. Não force ênclise ou mesóclise pra "parecer culto".
- Compliance (sinalizar, não corrigir): não é função desta skill validar promessa. Mas se notar promessa de cura, garantia de saúde ou garantia de retorno financeiro, registre um ALERTA na saída (categoria compliance) pro humano decidir. Não reescreva nem suavize sozinho.

## Severidade (priorize nesta ordem)
- P0 (mata credibilidade): em-dash e símbolos proibidos; erro de concordância grosso ("houveram", "fazem 2 anos"); homófono trocado ("mas/mais", "mau/mal", "a gente/agente"); cara de IA explícita ("Ótima pergunta!", disclaimers de robô).
- P1 (cheiro óbvio de IA / erro claro): gerundismo, translationese, formalismo cartorial, clichê de IA, crase errada, regência errada, vírgula entre sujeito e verbo.
- P2 (polimento): ritmo, concisão, especificidade, variação de frase.

---

## CAMADA 1 - Tirar a "cara de IA" (o que mais entrega texto ruim)

### Gerundismo (ir + estar + gerúndio para ação pontual)
Vício de tradução do inglês ("will be sending"). Mate.
- ❌ Vou estar enviando amanhã. → ✅ Envio amanhã. / Vou enviar amanhã.
- ❌ Nossa equipe vai estar verificando. → ✅ Nossa equipe vai verificar.
- ❌ Estarei confirmando. → ✅ Confirmo. / Vou confirmar.
Gerúndio só vale para ação que dura ("Ele está estudando agora").

### Translationese (tradução literal do inglês)
- ❌ Faça sentido para o negócio. → ✅ Vale a pena. / Faz sentido pro negócio.
- ❌ No final do dia, o que importa... → ✅ No fim das contas...
- ❌ Nós te cobrimos. → ✅ Pode deixar com a gente. / A gente resolve.
- ❌ Endereçar o problema. → ✅ Resolver / tratar / atacar o problema.
- ❌ Suportar várias formas de pagamento. → ✅ Aceitar várias formas de pagamento.

### Formalismo e verbos-muleta
Copy boa fala como gente. Corte: realizar, efetuar, proceder, disponibilizar, possibilitar, viabilizar.
- ❌ Realizamos a disponibilização da funcionalidade. → ✅ Lançamos a função.
- ❌ Efetuar o pagamento. → ✅ Pagar.
- ❌ Venho por meio desta comunicar que... → ✅ (vá direto ao ponto).
Conectivos cartoriais a cortar: ademais, outrossim, destarte, por conseguinte, no que tange a, em virtude de, a nível de.
- ❌ A nível de Brasil, as vendas cresceram. → ✅ No Brasil, as vendas cresceram. ("a nível de" só no sentido de altura: ao nível do mar.)

### Pleonasmo
- ❌ Há dez anos atrás. → ✅ Há dez anos. / Dez anos atrás.
- ❌ Encarar de frente / Planejar antecipadamente / Opinião pessoal / Elo de ligação / Certeza absoluta / Entrar pra dentro. → ✅ Encarar / Planejar / Opinião / Elo / Certeza / Entrar.

### Queísmo, voz passiva e advérbios em -mente
- ❌ Acho que é importante que você saiba que esse é o plano que mais vende. → ✅ Esse é o plano mais vendido.
- ❌ As metas foram alcançadas pela equipe. → ✅ A equipe alcançou as metas.
- ❌ Basicamente funciona perfeitamente e entrega rapidamente. → ✅ Funciona e entrega rápido. (no máximo um -mente por frase, de preferência zero.)

### Clichê de IA (cortar ou trocar por concreto)
"Em um mundo cada vez mais...", "não é apenas X, é Y", "imagine poder...", "descubra o poder de...", "eleve seu/sua...", "leve a um novo patamar", "transforme sua jornada", "mergulhe em", "libere seu potencial", "potencialize", "robusto", "alavancar", "solução revolucionária".
- ❌ Eleve sua produtividade a um novo patamar. → ✅ Faça em 1 hora o que hoje leva a tarde toda.

---

## CAMADA 2 - Gramática normativa essencial

### Concordância
- "Haver" = existir é impessoal, SEMPRE singular: ❌ Houveram problemas / Haviam três opções / Devem haver soluções. → ✅ Houve problemas / Havia três opções / Deve haver soluções.
- "Fazer" de tempo é impessoal, singular: ❌ Fazem dois anos. → ✅ Faz dois anos.
- Sujeito composto antes do verbo vai pro plural: ❌ O preço e o prazo importa. → ✅ ...importam.
- Porcentagem concorda com o número: ✅ 1% cancelou / 30% dos usuários reclamaram.
- "Um dos que" → plural: ✅ Ele é um dos clientes que mais compraram.
- Concordância nominal: "anexo/obrigado/mesmo/incluso" concordam (❌ Segue anexo as notas → ✅ Seguem anexas; mulher diz ✅ Obrigada). "meio" = um pouco é invariável (❌ meia cansada → ✅ meio cansada). "menos" é sempre invariável ("menas" não existe). "bastante" varia como adjetivo (bastantes pedidos = muitos) e não varia como advérbio (bastante satisfeito = muito).

### Regência (os que mais erram)
- assistir (ver) pede "a": ❌ Assisti o filme. → ✅ Assisti ao filme.
- implicar (acarretar) é direto, sem "em": ❌ Implica em custo. → ✅ Implica custo.
- preferir: "A a B", sem "do que": ❌ Prefiro café do que chá. → ✅ Prefiro café a chá.
- chegar / ir pedem "a" (não "em"): ❌ Cheguei em casa / Vou na loja. → ✅ Cheguei a casa / Vou à loja. (em copy bem informal o "em" passa; em texto cuidado, use "a".)
- visar (ter como objetivo) pede "a"; em copy, reescreva: "A campanha quer aumentar vendas."

### Crase (regra prática)
Teste: troque a palavra feminina por uma masculina. Se virar "ao", tem crase. Se virar só "o", não tem.
- "Vou à praia" → "Vou ao parque" → tem crase. "Conheço a cidade" → "Conheço o bairro" → sem crase.
NÃO tem crase: antes de masculino (✅ a prazo, a cavalo), antes de verbo (✅ começou a vender), antes de pronome (✅ falei a você), entre palavras iguais (✅ cara a cara, dia a dia), antes de "uma".
TEM crase: horas (✅ às 9h), locuções femininas (à tarde, à noite, à vista, à toa, às vezes, à medida que, à esquerda), modo/instrumento (✅ feito à mão).
"à medida que" (proporção) ≠ "na medida em que" (causa, porque). ❌ "na medida que" e ❌ "à medida em que" não existem.

### Colocação pronominal (BRASIL primeiro)
O brasileiro usa próclise (pronome antes do verbo), até no começo de frase. Ênclise solta soa de Portugal e empolada em copy.
- ❌ Chamo-me João e ofereço-lhe... → ✅ Me chamo João e te ofereço...
- ❌ Empresta-me um minuto. → ✅ Me empresta um minuto.
- Mesóclise (dir-lhe-ei, far-se-á) em copy: NUNCA. Reescreva ("vou te dizer", "vai ser feito").
- Norma a respeitar mesmo em texto formal: negação, advérbio e conjunção puxam próclise. ❌ Não aceita-se. → ✅ Não se aceita. (hipercorreção é erro.)
- Calibre pelo registro: copy informal (anúncio, e-mail, social) usa próclise solta e soa humana; texto institucional/jurídico respeita a norma (Trata-se de..., Recomenda-se...).

---

## CAMADA 3 - Ortografia, homófonos e pontuação

### Acordo de 1990 (use a forma nova)
Sem trema (tranquilo, frequência). Sem acento no ditongo aberto de paroxítona (ideia, assembleia, jiboia, heroico; mas oxítona mantém: herói, papéis). Sem acento em "oo"/"eem" (voo, enjoo, creem, veem). "para" verbo sem acento (Ele para o carro). Mantêm-se os diferenciais: pôde × pode, pôr × por, têm/vêm (plural).

### Homófonos (o ouro da revisão, confira sempre)
- mas (porém) × mais (quantidade): teste trocando por "porém"/"menos". ❌ Quero, mais não posso. → ✅ Quero, mas não posso.
- mau (×bom) × mal (×bem): ❌ Estou passando mau. → ✅ ...mal. ❌ Atendimento mal. → ✅ ...mau.
- a gente (nós) × agente (profissional): ❌ Agente entrega hoje. → ✅ A gente entrega hoje.
- porque (causa/resposta) / por que (pergunta ou "pelo qual") / por quê (fim de frase) / porquê (substantivo): ✅ Compre porque o preço sobe. / Por que esperar? / Desistiu por quê? / Quero saber o porquê.
- senão (caso contrário) × se não (caso não): ✅ Garanta hoje, senão acaba. / Se não der certo, devolvemos.
- a fim de (finalidade) × afim (afinidade): ✅ Liguei a fim de fechar. / Ideias afins.
- há (passado/existir) × a (futuro/distância): ✅ Há 3 dias acabou. / Daqui a 3 dias chega. (❌ "há 3 dias atrás", ❌ "a muito tempo".)
- onde (lugar) × aonde (com movimento) × em que: ✅ A loja onde compro. / Aonde você vai? / O dia em que mudou (não "onde").

### Pontuação
- NUNCA separe sujeito do verbo, nem verbo do complemento, com uma vírgula só: ❌ O plano premium, oferece suporte. → ✅ ...premium oferece suporte. (termo intercalado fica entre DUAS vírgulas: ✅ O plano, lançado ontem, esgotou.)
- Vírgula antes de mas/porém/contudo/ou seja: ✅ Funciona, mas exige prática.
- Oração explicativa entre vírgulas (≠ restritiva sem vírgula): ✅ O curso, que é online, começa hoje. / O curso que comprei começou.
- Dois-pontos para anunciar: ✅ A regra é simples: comprou, ganhou.

### Naturalidade Brasil × Portugal
Use gerúndio, não "a + infinitivo": ❌ Estou a fazer → ✅ Estou fazendo. Vocabulário BR: celular (não telemóvel), tela (não ecrã), ônibus, banheiro, terno, suco, trem, sobrenome, legal. Trate por "você" (não "tu" conjugado à lusa, nem "vós").

---

## CAMADA 4 - Copy forte (estilo)
- Corte a gordura. Cada palavra paga aluguel. ❌ Gostaríamos de poder oferecer a possibilidade de testar. → ✅ Teste o produto. Cace e corte: que, muito, realmente, basicamente, é importante ressaltar, vale lembrar que.
- Voz ativa e verbo de ação. CTA com verbo forte (Garanta, Comece, Baixe, Teste), nunca "Enviar"/"Cadastro" soltos.
- Comece pelo concreto: ❌ Soluções inovadoras para sua jornada. → ✅ Faça o relatório da semana em 5 minutos.
- Especificidade vence o genérico: ❌ Atendimento rápido. → ✅ Resposta em até 2 minutos. ❌ Muitos confiam. → ✅ 12.480 clientes confiam.
- Ritmo: varie o tamanho da frase. Frase curta dá impacto. Alterne com uma mais longa pra respirar. Depois, corte. Alvo: média de 12 a 18 palavras, com variação.
- Fale com o leitor (você): ❌ Os clientes que adquirirem terão acesso. → ✅ Você compra e já tem acesso.

---

## Formato de saída

Modo REVISAR (revisar texto que já existe). Entregue nesta ordem:
1. TABELA DE ACHADOS, colunas: # | trecho original | correção | regra ou categoria | severidade.
2. VERSÃO FINAL: o texto com as correções de severidade "erro" e "inconsistência" aplicadas (sugestões de estilo só se pedirem, ou marcadas à parte), com mudança mínima e placeholders intactos.
3. CHECKLIST (o de baixo).
Severidades: erro (viola a norma, corrigir) · inconsistência (certo isolado, mas conflita com outra parte do texto: gênero, pessoa, tempo, capitalização) · sugestão de estilo (opcional, melhora naturalidade) · compliance (promessa sensível: só ALERTA, não corrigir). Se não houver nada: diga "Nenhum erro de português encontrado. Texto aprovado."

Modo REESCREVER (padrão):
1. PROBLEMAS por severidade P0/P1/P2.
2. VERSÃO CORRIGIDA: o texto pronto.
3. O QUE MUDOU: 1 linha por mudança relevante.

Modo ESCREVER: entregue o texto já seguindo todas as regras.

Em todos os modos, faça uma 2a passada interna: releu, zerou em-dash e símbolos proibidos, conferiu placeholders e sobras.

## Checklist final (rode na ordem antes de entregar)
1. Zero em-dash (U+2014), en-dash (U+2013) e reticências-caractere (U+2026); zero aspas e apóstrofo curvos. Busca literal por esses códigos.
2. Zero gerundismo ("vou estar -ndo").
3. Zero translationese/anglicismo e zero termo de Portugal.
4. Formalismo cortado (realizar/efetuar/disponibilizar; ademais/a nível de).
5. Pleonasmo eliminado.
6. Homófonos conferidos (mas/mais, mau/mal, a gente/agente, porque×4, senão/se não, a fim/afim, há/a, onde/aonde).
7. Crase pelo teste do "ao"; "à medida que" × "na medida em que".
8. Concordância (houve, faz X anos, a maioria, anexo/meio/menos).
9. Regência (assistir/visar a, implicar sem em, preferir A a B, chegar/ir a).
10. Colocação pronominal natural (próclise no informal, sem mesóclise, sem hipercorreção).
11. Vírgula (nada entre sujeito e verbo; antes de mas; vocativo/aposto isolados).
12. Voz ativa.
13. Frase 12 a 18 palavras com variação; cortar "que", -mente, gordura.
14. Concreto e específico; clichê morto.
15. Leitura em voz alta: travou ou soou de robô/de Portugal, reescreva.
16. Placeholders, variáveis, URLs e nomes oficiais de marca intactos (nenhum "corrigido" por engano).
17. Ao revisar texto dos outros: mudança mínima respeitada (não reescreveu nem trocou a voz do autor); alerta de compliance registrado se havia promessa sensível.

## Fontes
Gramáticas: Bechara (Moderna Gramática), Cunha e Cintra (Nova Gramática), Cegalla (Dicionário de Dificuldades). Manuais: Folha de S.Paulo, Estadão, Senado. Consultório: Ciberdúvidas. Gerundismo: BBC Brasil / Prof. Pasquale. Arquitetura de revisão anti-IA: conorbronsdon/avoid-ai-writing, blader/humanizer. Para persuasão e oferta, ver a skill copywriting (HAOS).

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
