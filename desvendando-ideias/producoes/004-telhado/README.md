# 004 · Como se constrói um telhado

Roteiro e decisões: `../../roteiros/004-telhado.md`. Motor compartilhado: `../../motor/README.md`.

```sh
../../motor/voz-proc.sh                      # normaliza a voz de assets/voz/ para assets/voz/proc/
node ../../motor/build.mjs                   # gera index.html, compositions/, PLANOS.md e o som
node ../../motor/checar.mjs                  # confere duração, planos, voz, roteiro e (se houver) o render
npx hyperframes render --quality draft -o renders/004-telhado-rascunho1.mp4
```
