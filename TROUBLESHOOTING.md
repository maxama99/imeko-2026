# Troubleshooting: ikonky v sekci "Event highlights"

## Příznak
Na produkci se nezobrazovaly ikonky u čísel (2 Speakers, 3 Sessions, 3 Days, Prague) a přímý přístup na URL typu `/icons/speaker.svg` vracel 404.

## Příčina
- Šablona `event-highlights` odkazuje na ikonky pomocí cest `icons/*.svg` a Hugo je nejprve zkouší načíst přes `resources.Get` (což funguje jen pro soubory v `assets/`).【F:themes/event/layouts/partials/sections/event-highlights.html†L37-L65】【F:themes/event/layouts/partials/highlight-figure.html†L5-L20】
- Repozitář ale neobsahoval žádné zdroje ikon v `assets/` ani v `static/icons/`, takže build na produkci nevytvořil odpovídající soubory. Výsledné stránky ukazovaly na `/icons/*.svg`, které na serveru neexistovaly, proto 404.

## Řešení
- Přidali jsme SVG soubory do `static/icons/`, aby byly vždy publikované i bez Hugo asset pipeline.【F:static/icons/speaker.svg†L1-L22】
- Partial `highlight-figure` má fallback na statickou cestu, takže se ikony načítají i když `resources.Get` vrátí `nil` (typicky na produkci, kde neexistují assety).【F:themes/event/layouts/partials/highlight-figure.html†L5-L20】

Pokud by se problém zopakoval, ověřte, že cílové prostředí nasazuje obsah adresáře `static/` (zejména `static/icons/`).
