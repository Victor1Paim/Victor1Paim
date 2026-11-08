# Geradores dos projetos HyperFrames

`build_sono.py`, `build_alongar.py` e `build_passos.py` geraram os projetos em `producoes/<post>/video/`.
`build_sono.py` contém a base reaproveitável (paleta, Tito em SVG com boca que fala, balões
"PERGUNTA DO TITO" / "O QUE O TITO ENTENDEU", legendas por palavra, CTA com card do perfil);
`build_alongar.py` importa essa base e acrescenta transições, contadores, gráficos de barras,
selo "✕ MITO", partículas e poses do Tito em imagem.

Os caminhos no topo apontam para a pasta temporária da sessão em que foram criados; ajustar
`SCR`/`POST`/`V` antes de reutilizar. O projeto gerado (HTML) é a fonte editável de verdade.
