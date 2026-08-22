from playwright.sync_api import sync_playwright


FORM_URL = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLSeue1efPeVQxi0N1rCVhCfqg7-DQn9cyfAk1vPh1Sr-uP6sXA/"
    "viewform"
)

PERGUNTA = "Melhor Criadora de Conteúdo Feminino"
OPCAO = "Luiza Sampaio"


def encontrar_botao_proxima(page):
    textos = [
        "Próxima",
        "Next",
        "Avançar",
    ]

    for texto in textos:
        locator = page.get_by_role(
            "button",
            name=texto
        )

        if locator.count() > 0:
            return locator.first

    return None


def encontrar_botao_enviar(page):
    textos = [
        "Enviar",
        "Submit",
    ]

    for texto in textos:
        locator = page.get_by_role(
            "button",
            name=texto
        )

        if locator.count() > 0:
            return locator.first

    return None


def encontrar_opcao(page, texto):
    # Tenta encontrar a opção pelos radios
    radios = page.get_by_role("radio")

    for i in range(radios.count()):
        radio = radios.nth(i)

        try:
            aria_label = radio.get_attribute("aria-label")

            if (
                aria_label
                and texto.lower() in aria_label.lower()
            ):
                return radio

        except Exception:
            pass

    # Fallback: procura pelo texto visível
    locator = page.get_by_text(
        texto,
        exact=True
    )

    if locator.count() > 0:
        return locator.first

    return None


def esperar_confirmacao(page):
    page.wait_for_timeout(3000)

    texto = page.locator("body").inner_text()
    texto_lower = texto.lower()

    mensagens_confirmacao = [
        "resposta registrada",
        "resposta foi registrada",
        "resposta registrada com sucesso",
        "response recorded",
        "your response has been recorded",
        "obrigado",
        "thank you",
    ]

    for mensagem in mensagens_confirmacao:
        if mensagem in texto_lower:
            return True

    return False


def votar():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            viewport={
                "width": 1280,
                "height": 900,
            }
        )

        print("=" * 60)
        print("ABRINDO FORMULÁRIO")
        print("=" * 60)

        page.goto(
            FORM_URL,
            wait_until="domcontentloaded"
        )

        page.wait_for_timeout(3000)

        # --------------------------------------------------
        # Procurar a pergunta
        # --------------------------------------------------

        pergunta = page.get_by_text(
            PERGUNTA,
            exact=False
        )

        if pergunta.count() > 0:

            print(
                f'\n✓ Pergunta encontrada: "{PERGUNTA}"'
            )

        else:

            print(
                f'\nA pergunta "{PERGUNTA}" '
                "não está na primeira página."
            )

            print("Procurando botão Próxima...")

            proxima = encontrar_botao_proxima(page)

            if proxima is None:

                print(
                    "\n✗ Botão Próxima não encontrado."
                )

                print(
                    "\nTexto atual da página:"
                )

                print(
                    page.locator("body").inner_text()[:5000]
                )

                browser.close()

                return

            print(
                "✓ Botão Próxima encontrado."
            )

            proxima.click()

            page.wait_for_timeout(2000)

            pergunta = page.get_by_text(
                PERGUNTA,
                exact=False
            )

            if pergunta.count() == 0:

                print(
                    f'\n✗ Pergunta "{PERGUNTA}" '
                    "não encontrada."
                )

                print(
                    "\nTexto da página atual:"
                )

                print(
                    page.locator("body").inner_text()[:5000]
                )

                browser.close()

                return

            print(
                f'✓ Pergunta encontrada: "{PERGUNTA}"'
            )

        # --------------------------------------------------
        # Procurar Luiza Sampaio
        # --------------------------------------------------

        print(
            f'\nProcurando opção "{OPCAO}"...'
        )

        opcao = encontrar_opcao(
            page,
            OPCAO
        )

        if opcao is None:

            print(
                "\n✗ Opção não encontrada."
            )

            print(
                "\nRadios encontrados:"
            )

            radios = page.get_by_role("radio")

            for i in range(radios.count()):

                radio = radios.nth(i)

                print(
                    f"{i}: "
                    f"{radio.get_attribute('aria-label')}"
                )

            print(
                "\nTexto da página:"
            )

            print(
                page.locator("body").inner_text()[:5000]
            )

            browser.close()

            return

        # --------------------------------------------------
        # Selecionar Luiza Sampaio
        # --------------------------------------------------

        print(
            f'✓ Opção encontrada: "{OPCAO}"'
        )

        opcao.scroll_into_view_if_needed()

        opcao.click()

        page.wait_for_timeout(500)

        print(
            f'\n✓ "{OPCAO}" selecionada.'
        )

        # --------------------------------------------------
        # Enviar automaticamente
        # --------------------------------------------------

        print(
            "\nProcurando botão Enviar..."
        )

        enviar = encontrar_botao_enviar(page)

        if enviar is None:

            print(
                "\n✗ Botão Enviar não encontrado."
            )

            print(
                "\nTexto da página:"
            )

            print(
                page.locator("body").inner_text()[:5000]
            )

            print(
                "\nFechando..."
            )

            browser.close()

            return

        print(
            "✓ Botão Enviar encontrado."
        )

        print(
            "\nEnviando formulário..."
        )

        enviar.click()

        # --------------------------------------------------
        # Aguardar confirmação
        # --------------------------------------------------

        print(
            "Aguardando confirmação..."
        )

        confirmado = esperar_confirmacao(page)

        if confirmado:

            print("\n" + "=" * 60)
            print("✓ RESPOSTA CONFIRMADA")
            print("=" * 60)

            print(
                "\nA confirmação foi detectada."
            )

            print(
                "Fechando navegador..."
            )

            page.wait_for_timeout(1000)

            browser.close()

        else:

            print("\n" + "=" * 60)
            print("⚠ CONFIRMAÇÃO NÃO IDENTIFICADA")
            print("=" * 60)

            print(
                "\nO navegador permanecerá aberto "
                "para você verificar o resultado."
            )

            print(
                "\nTexto recebido:"
            )

            print(
                page.locator("body").inner_text()[:3000]
            )

            print(
                "\nFechando..."
            )

            browser.close()


if __name__ == "__main__":
    votar()