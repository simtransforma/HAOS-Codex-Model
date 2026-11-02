#!/usr/bin/env python3
"""
Script para geraÃ§Ã£o de thumbnails via API Nanobanana (OpenRouter + Gemini)
Canal: Script7
"""

raise RuntimeError('requires_user_config: render placeholders, review bindings and remove this guard only after local validation')


import os
import sys
import json
import base64
import requests
from pathlib import Path
from datetime import datetime

# ============================================
# CONFIGURAÃ‡Ã•ES - EDITE AQUI
# ============================================

# Sua API Key do OpenRouter (obtenha em https://service.example.invalid)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# Modelo para geraÃ§Ã£o de imagens (Nano Banana)
# NOTA: O modelo correto Ã© "google/gemini-2.5-flash-image" (SEM -preview)
MODEL = "google/gemini-2.5-flash-image"

# URL da API
OPENROUTER_API_URL = "https://service.example.invalid"

# DiretÃ³rio onde as thumbnails serÃ£o salvas
# Usar o diretÃ³rio pai do script (diretÃ³rio da skill)
SCRIPT_DIR = Path(__file__).parent.parent
OUTPUT_DIR = SCRIPT_DIR / "thumbnails"

# ============================================

def get_api_key():
    """Retorna a API key configurada."""
    if not OPENROUTER_API_KEY:
        print("âš ï¸  API Key nÃ£o configurada!")
        print("   Abra o arquivo generate-thumbnail.py")
        print("   Defina a variavel de ambiente OPENROUTER_API_KEY antes de executar")
        sys.exit(1)
    return OPENROUTER_API_KEY

def generate_thumbnail(prompt: str, api_key: str) -> dict:
    """
    Gera uma thumbnail via API Nanobanana/OpenRouter.

    Args:
        prompt: DescriÃ§Ã£o detalhada da thumbnail desejada
        api_key: OpenRouter API key

    Returns:
        dict com status, base64 da imagem ou erro
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://service.example.invalid",
        "X-Title": "Script7 YouTube Thumbnail Generator"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "modalities": ["text", "image"],
        # Configurar aspect ratio 16:9 para YouTube
        # NOTA: A API Gemini retorna resoluÃ§Ãµes prÃ©-definidas (ex: 1344x768 em vez de 1280x720)
        # Mas o aspect ratio 16:9 Ã© mantido, compatÃ­vel com YouTube
        "image_config": {
            "aspect_ratio": "16:9",  # 16:9 = formato horizontal YouTube
            "image_size": "1K"  # ResoluÃ§Ã£o padrÃ£o (~1344x768)
        }
    }

    try:
        print(f"ðŸš€ Enviando requisiÃ§Ã£o para {MODEL}...")
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        data = response.json()

        # Extrair base64 da resposta
        # OpenRouter retorna imagens no campo "images" da mensagem do assistente
        if "choices" in data and len(data["choices"]) > 0:
            message = data["choices"][0].get("message", {})

            # Verificar campo "images" (formato OpenRouter para geraÃ§Ã£o de imagens)
            images = message.get("images", [])
            if images and len(images) > 0:
                # Images podem vir em diferentes formatos:
                # 1. Lista de strings: ["data:image/png;base64,..."]
                # 2. Lista de dicts com type: 'image_url': [{"type": "image_url", "image_url": {"url": "data:..."}}]
                # 3. Lista de dicts com url direto: [{"url": "data:..."}]

                img = images[0]
                if isinstance(img, str):
                    image_url = img
                elif isinstance(img, dict):
                    # Tentar diferentes caminhos possÃ­veis
                    image_url = (
                        img.get("image_url", {}).get("url", "") or  # formato image_url.url
                        img.get("url", "")  # formato url direto
                    )

                if "," in image_url:
                    return {
                        "success": True,
                        "base64": image_url.split(",")[1],
                        "usage": data.get("usage", {})
                    }

            # Fallback: verificar content (compatibilidade com formatos antigos)
            content = message.get("content", "")

            # Tentar fazer parse do content se for JSON (inline_data format)
            if content:
                # Verificar se Ã© um JSON com inline_data
                try:
                    # Gemini pode retornar como string JSON
                    if "{" in content:
                        import re
                        # Extrair o JSON do content
                        json_match = re.search(r'\{[^{}]*"inline_data"[^{}]*\}', content, re.DOTALL)
                        if json_match:
                            json_str = json_match.group(0)
                            parsed = json.loads(json_str)
                            if "inline_data" in parsed and "image_uri" in parsed["inline_data"]:
                                # Extrair base64 do data URI (data:image/png;base64,...)
                                image_uri = parsed["inline_data"]["image_uri"]
                                if "," in image_uri:
                                    return {
                                        "success": True,
                                        "base64": image_uri.split(",")[1],
                                        "usage": data.get("usage", {})
                                    }
                except (json.JSONDecodeError, KeyError):
                    pass

                # Verificar se o content Ã© um data URI direto
                if content.startswith("data:image"):
                    if "," in content:
                        return {
                            "success": True,
                            "base64": content.split(",")[1],
                            "usage": data.get("usage", {})
                        }

            # Verificar reasoning_details para dados de imagem
            reasoning = message.get("reasoning_details", [])
            for detail in reasoning:
                if detail.get("type") == "image":
                    image_uri = detail.get("data", "")
                    if "," in image_uri:
                        return {
                            "success": True,
                            "base64": image_uri.split(",")[1],
                            "usage": data.get("usage", {})
                        }

        return {
            "success": False,
            "error": "Nenhuma imagem encontrada na resposta",
            "raw_response": data
        }

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Timeout na requisiÃ§Ã£o (120s)"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Erro na requisiÃ§Ã£o: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Erro ao decodificar resposta JSON: {str(e)}"}

def save_thumbnail(base64_data: str, filename: str) -> Path:
    """
    Converte base64 para PNG e salva o arquivo.

    Args:
        base64_data: Dados da imagem em base64
        filename: Nome do arquivo (sem extensÃ£o)

    Returns:
        Path do arquivo salvo
    """
    # Criar diretÃ³rio se nÃ£o existir
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Limpar nome do arquivo
    safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_filename = safe_filename.replace(' ', '-').lower()

    # Adicionar timestamp para evitar sobrescritas
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = OUTPUT_DIR / f"{safe_filename}-{timestamp}.png"

    # Remover prefixo data:image se presente
    if "," in base64_data:
        base64_data = base64_data.split(",")[1]

    # Decodificar e salvar
    try:
        image_data = base64.b64decode(base64_data)
        with open(output_path, "wb") as f:
            f.write(image_data)
        return output_path
    except Exception as e:
        raise ValueError(f"Erro ao salvar imagem: {str(e)}")

def build_prompt(
    text: str,
    style: str = "tutorial",
    visual_element: str = "",
    colors: str = "blue purple gradient"
) -> str:
    """
    ConstrÃ³i um prompt otimizado para thumbnail Script7.

    Args:
        text: Texto principal da thumbnail (mÃ¡x 6 palavras)
        style: Estilo (tutorial, review, news, list, tips)
        visual_element: Elemento visual principal (logo, Ã­cone, etc)
        colors: Esquema de cores

    Returns:
        Prompt formatado para a API
    """
    base_prompt = f"""Create a YouTube thumbnail in 16:9 aspect ratio (YouTube format):
- Bold, eye-catching text in 2-3 angled text boxes
- Text: "{text}"
- Style: Modern tech, {style}
- Colors: {colors}
- High contrast, mobile-readable text
- Professional design for tech/programming channel
- IMPORTANT: Must use 16:9 horizontal format for YouTube (like 1280x720 or 1344x768)"""

    if visual_element:
        base_prompt += f"\n- Include: {visual_element} as the main visual element"

    base_prompt += """
- Text boxes should be angled/tilted for dynamic look
- White bold text with subtle shadow
- Subtle code/tech elements in background"""

    return base_prompt


def interactive_prompt_builder(video_title: str = "") -> dict:
    """
    Modo interativo para construir o prompt da thumbnail com o usuÃ¡rio.
    PERGUNTA AO USUÃRIO ANTES DE GERAR.

    Args:
        video_title: TÃ­tulo do vÃ­deo (opcional, como referÃªncia)

    Returns:
        dict com text, style, visual_element, colors, prompt
    """
    print("=" * 60)
    print("ðŸŽ¨ CONSTRUTOR DE THUMBNAIL - MODO INTERATIVO")
    print("=" * 60)

    if video_title:
        print(f"\nðŸ“¹ VÃ­deo: {video_title}\n")

    # 1. Texto da thumbnail (mÃ¡ximo 6 palavras)
    print("1ï¸âƒ£  TEXTO DA THUMBNAIL")
    print("-" * 40)
    print("Importante: MÃ¡ximo 6 palavras para ser legÃ­vel no mobile")
    while True:
        text = input("Digite o texto da thumbnail: ").strip()
        word_count = len(text.split())
        if word_count <= 6:
            break
        print(f"âš ï¸  {word_count} palavras! Reduza para no mÃ¡ximo 6.")

    # 2. Estilo visual
    print("\n2ï¸âƒ£  ESTILO VISUAL")
    print("-" * 40)
    print("Estilos disponÃ­veis:")
    print("  1. tutorial  - Aprendizado, passo a passo")
    print("  2. review    - AvaliaÃ§Ã£o, opiniÃ£o")
    print("  3. news      - NotÃ­cia, novidade, lanÃ§amento")
    print("  4. list      - Lista, top X, melhores")
    print("  5. tips      - Dicas, hacks, truques")
    print("  6. viral     - Impactante, curiosidade")

    style_map = {
        "1": "tutorial", "tutorial": "tutorial",
        "2": "review", "review": "review",
        "3": "news", "news": "news",
        "4": "list", "list": "list",
        "5": "tips", "tips": "tips",
        "6": "viral", "viral": "viral"
    }

    while True:
        style_input = input("Escolha o estilo (nÃºmero ou nome) [tutorial]: ").strip().lower() or "tutorial"
        if style_input in style_map:
            style = style_map[style_input]
            break
        print("âš ï¸  OpÃ§Ã£o invÃ¡lida!")

    # 3. Elemento visual principal
    print("\n3ï¸âƒ£  ELEMENTO VISUAL PRINCIPAL")
    print("-" * 40)
    print("SugestÃµes de elementos visuais:")
    print("  - Logotipo da ferramenta/tecnologia")
    print("  - Screenshot ou mockup")
    print("  - Ãcones representativos")
    print("  - Foto ou ilustraÃ§Ã£o")
    print("  - Deixe vazio para fundo abstrato")

    visual_element = input("Elemento visual (opcional): ").strip()

    # 4. Cores
    print("\n4ï¸âƒ£  ESCOLHA DE CORES")
    print("-" * 40)
    print("Paletas populares Script7:")
    print("  1. blue purple gradient  (azul roxo - padrÃ£o)")
    print("  2. orange red gradient    (laranja vermelho - urgente)")
    print("  3. green cyan gradient    (verde ciano - fresco)")
    print("  4. dark neon              (fundo escuro com neon)")
    print("  5. white black contrast   (alto contraste)")

    color_map = {
        "1": "blue purple gradient",
        "2": "orange red gradient",
        "3": "green cyan gradient",
        "4": "dark neon",
        "5": "white black contrast"
    }

    color_input = input("Escolha as cores [1]: ").strip() or "1"
    colors = color_map.get(color_input, "blue purple gradient")

    # Construir prompt
    prompt = build_prompt(text, style, visual_element, colors)

    # Mostrar preview e pedir confirmaÃ§Ã£o
    print("\n" + "=" * 60)
    print("ðŸ“‹ PREVIEW DO PROMPT")
    print("=" * 60)
    print(f"\nTexto: \"{text}\"")
    print(f"Estilo: {style}")
    print(f"Elemento visual: {visual_element or '(nenhum)'}")
    print(f"Cores: {colors}")
    print(f"\nPrompt completo:\n{prompt}")
    print("\n" + "=" * 60)

    # Confirmar
    confirm = input("\nâœ… Gerar thumbnail com este prompt? (s/n): ").strip().lower()
    if confirm != 's':
        print("âŒ Cancelado. Execute novamente para ajustar.")
        return {"success": False, "cancelled": True}

    return {
        "success": True,
        "text": text,
        "style": style,
        "visual_element": visual_element,
        "colors": colors,
        "prompt": prompt
    }

def main():
    """FunÃ§Ã£o principal para execuÃ§Ã£o via CLI."""
    print("=" * 50)
    print("ðŸŽ¨ Script7 - YouTube Thumbnail Generator")
    print("=" * 50)

    # Obter API key
    api_key = get_api_key()

    # Verificar flag --interactive
    if "--interactive" in sys.argv or "-i" in sys.argv:
        # Modo interativo completo
        video_title = ""
        if len(sys.argv) > 2 and sys.argv[-1] not in ["--interactive", "-i"]:
            video_title = sys.argv[-1]

        result = interactive_prompt_builder(video_title)

        if not result.get("success"):
            if result.get("cancelled"):
                print("\nðŸ‘ OperaÃ§Ã£o cancelada pelo usuÃ¡rio.")
            else:
                print("\nâŒ Erro ao construir prompt.")
            sys.exit(0)

        # Gerar thumbnail com os dados coletados
        filename = input("\nðŸ“ Nome do arquivo para salvar [thumbnail]: ").strip() or "thumbnail"

        print(f"\nðŸ“‹ Prompt final:")
        print("-" * 40)
        print(result["prompt"])
        print("-" * 40)

        thumbnail_result = generate_thumbnail(result["prompt"], api_key)

        if thumbnail_result["success"]:
            print("\nâœ… Imagem gerada com sucesso!")

            try:
                output_path = save_thumbnail(thumbnail_result["base64"], filename)
                print(f"ðŸ’¾ Arquivo salvo: {output_path}")

                if "usage" in thumbnail_result:
                    usage = thumbnail_result["usage"]
                    print(f"\nðŸ“Š Uso:")
                    print(f"   - Tokens prompt: {usage.get('prompt_tokens', 'N/A')}")
                    print(f"   - Tokens completion: {usage.get('completion_tokens', 'N/A')}")
                    print(f"   - Custo estimado: ${usage.get('cost', 0):.4f}")

            except Exception as e:
                print(f"âŒ Erro ao salvar: {e}")
        else:
            print(f"\nâŒ Erro: {thumbnail_result.get('error', 'Erro desconhecido')}")

        print("\n" + "=" * 50)
        return

    # Modo interativo se sem argumentos (exceto flags)
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if len(args) < 1:
        print("\nðŸ“ Modo Interativo")
        print("-" * 30)

        text = input("Texto da thumbnail (mÃ¡x 6 palavras): ").strip()
        if not text:
            print("âŒ Texto Ã© obrigatÃ³rio!")
            sys.exit(1)

        style = input("Estilo (tutorial/review/news/list/tips) [tutorial]: ").strip() or "tutorial"
        visual = input("Elemento visual (ex: 'Claude logo', 'code editor') [opcional]: ").strip()
        colors = input("Cores (ex: 'blue purple gradient') [blue purple gradient]: ").strip() or "blue purple gradient"
        filename = input("Nome do arquivo [thumbnail]: ").strip() or "thumbnail"

        prompt = build_prompt(text, style, visual, colors)
    else:
        # Modo CLI com argumentos
        text = args[0]
        style = args[1] if len(args) > 1 else "tutorial"
        visual = args[2] if len(args) > 2 else ""
        colors = args[3] if len(args) > 3 else "blue purple gradient"
        filename = args[4] if len(args) > 4 else "thumbnail"

        prompt = build_prompt(text, style, visual, colors)

    print(f"\nðŸ“‹ Prompt gerado:")
    print("-" * 30)
    print(prompt)
    print("-" * 30)

    # Gerar thumbnail
    result = generate_thumbnail(prompt, api_key)

    if result["success"]:
        print("\nâœ… Imagem gerada com sucesso!")

        # Salvar arquivo
        try:
            output_path = save_thumbnail(result["base64"], filename)
            print(f"ðŸ’¾ Arquivo salvo: {output_path}")

            # Mostrar uso de tokens
            if "usage" in result:
                usage = result["usage"]
                print(f"\nðŸ“Š Uso:")
                print(f"   - Tokens prompt: {usage.get('prompt_tokens', 'N/A')}")
                print(f"   - Tokens completion: {usage.get('completion_tokens', 'N/A')}")
                print(f"   - Custo estimado: ${usage.get('cost', 0):.4f}")

        except Exception as e:
            print(f"âŒ Erro ao salvar: {e}")
            print(f"   Base64 disponÃ­vel para uso manual")

    else:
        print(f"\nâŒ Erro: {result.get('error', 'Erro desconhecido')}")
        if "raw_response" in result:
            print(f"   Resposta raw: {json.dumps(result['raw_response'], indent=2)[:500]}...")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()


# ============================================
# FunÃ§Ãµes para uso como mÃ³dulo
# ============================================

def generate_and_save(
    text: str,
    filename: str,
    style: str = "tutorial",
    visual_element: str = "",
    colors: str = "blue purple gradient",
    api_key: str = None
) -> dict:
    """
    FunÃ§Ã£o de conveniÃªncia para gerar e salvar thumbnail.

    Args:
        text: Texto da thumbnail
        filename: Nome do arquivo
        style: Estilo visual
        visual_element: Elemento visual principal
        colors: Esquema de cores
        api_key: API key (usa env se nÃ£o fornecida)

    Returns:
        dict com success, path ou error
    """
    if not api_key:
        api_key = (os.environ.get)("OPENROUTER_API_KEY")
        if not api_key:
            return {"success": False, "error": "API key nÃ£o fornecida"}

    prompt = build_prompt(text, style, visual_element, colors)
    result = generate_thumbnail(prompt, api_key)

    if result["success"]:
        try:
            path = save_thumbnail(result["base64"], filename)
            return {"success": True, "path": str(path), "prompt": prompt}
        except Exception as e:
            return {"success": False, "error": str(e), "prompt": prompt}

    return result

