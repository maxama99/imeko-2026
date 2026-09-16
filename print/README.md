# Tiskoviny pro session chairy (IMEKO TC4 2026)

Dvě sady pro 8 sessionů konference (17.–18. 9. 2026, místnost T2:C3:340):

| Soubor | Co to je |
|---|---|
| `tent-cards.tex` → `tent-cards.pdf` | Jmenovka (tent card) pro každého chaira. A4 našířku, 8 stran (1 chair = 1 strana). |
| `session-programs.tex` → `session-programs.pdf` | Program sekce pro chaira. A4 navýšku, 8 stran (1 session = 1 strana), pod každým příspěvkem místo na poznámky. |
| `imeko-chair.sty` | Sdílený styl — makra `\tentcard`, prostředí `sessionpage`, `\talk`. |
| `logos/` | `imeko-logo.png` (z `themes/event/assets/logos/imeko-logo.gif`), `meas-logo.png` (katedra měření FEL ČVUT). |

## Sestavení

```bash
cd print
pdflatex tent-cards.tex && pdflatex tent-cards.tex   # dvakrát — karty používají TikZ overlay
pdflatex session-programs.tex
```

Potřeba je `pdflatex` (TeX Live) s balíčky `tikz`, `helvet`, `lmodern`, `geometry`, `microtype`.

## Tisk

- **Jmenovky:** A4 našířku, jednostranně, papír ideálně 160–250 g/m². Přeložit napůl podél čárkované linky — jméno je na obou polovinách, horní je otočená o 180°, takže po postavení čte jméno publikum i chair.
- **Program:** A4 navýšku, jednostranně, jedna strana pro každého chaira.

## Údržba

Obsah je **ručně přepsaný** z `data/program.example.yaml` (sekce `session_chairs` a `sessions`) — není to generátor. Po každé změně programu je nutné ručně srovnat:

- pořadí příspěvků = pořadí v YAML (chronologické; `ses-NNN` ID mají mezery, nikdy neřadit podle ID),
- časy, jména prezentujících, názvy příspěvků,
- u keynote se z názvu vypouští prefix `Invited Keynote: ` a místo něj je štítek KEYNOTE.

Afiliace chairů v YAML nejsou — jsou vepsané přímo v `tent-cards.tex`.

V LaTeXu escapovat `&` jako `\&` (v názvech sekcí i příspěvků je ho hodně), dále `%`, `#`, `_`.
