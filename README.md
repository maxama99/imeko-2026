# Hugo Event Theme Demo

A demo event website built with the [Hugo Event Theme](https://github.com/medialesson/hugo-theme-event).

See it in action on https://medialesson.github.io/hugo-theme-event-demo.

You can use this repository as template for your new project.
[Click here to create a new repository.](https://github.com/new?template_name=hugo-theme-event-demo&template_owner=medialesson)

## Getting started

### Prerequisites

1. [Hugo](https://gohugo.io/installation/) is installed on your machine.
2. You're familiar with [Git Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules).

### Installation

1. Open a shell of your choice.
2. Clone this repository with submodules.
    ```shell
    git clone --recurse-submodules https://github.com/medialesson/hugo-theme-event-demo.git
    ```
3. Switch to the repository directory.
4. Run npm install to install the required dependencies.
    ```shell
    npm install
    ```
5. Run Hugo in development mode:
    ```shell
    hugo server
    ```
6. View the demo event website on http://localhost:1313/.

## Event content & schedule

- Základní nastavení webu: `hugo.yaml` → sekce `params.themes.event` (název konference, datum, adresa, CTA, barvy, loga, sociální odkazy). `sessionizeId` nech `test` pro lokální data; skutečné ID použij až když je dostupný internet.
- Lokální program/speakery: uprav YAML `data/program.example.yaml` (speakeři, sessions, tracky) a vygeneruj JSON pro Hugo:
  ```shell
  python scripts/generate_sessionize_view_all.py --input data/program.example.yaml --output themes/event/assets/test/sessionize-view-all.json
  ```
  Skript vytvoří `view/all` strukturu kompatibilní se Sessionize a Hugo ji načte místo vzdáleného API. Tracky lze předdefinovat v `tracks:` a u každé session stačí doplnit `title`, `speakers`, `type`, `track`, `room`, `start`, `end`.
