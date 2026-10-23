"""Genera gatito.svg: Apolo, un gatito negro con rayitas que pasea por el perfil.

Según la fecha (hora de Perú) se viste para la ocasión:
  - Año nuevo       (31 dic - 2 ene):  gorrito de fiesta y confeti
  - San Valentín    (10 - 14 feb):     corazones
  - Fiestas Patrias (20 - 31 jul):     escarapela y banderas del Perú
  - Halloween       (20 oct - 1 nov):  sombrero de bruja y calabazas
  - Navidad         (1 - 26 dic):      gorro de Papá Noel y arbolitos

Uso:
  python generar_gatito.py                     # tema según la fecha de hoy
  python generar_gatito.py --tema navidad      # forzar un tema (para probar)
  python generar_gatito.py --tema todos        # genera ejemplos en ejemplos/

La GitHub Action (.github/workflows/apolo.yml) lo ejecuta todos los días.
"""

import argparse
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

PERU = timezone(timedelta(hours=-5))
TEMAS = ["normal", "anio_nuevo", "san_valentin", "fiestas_patrias", "halloween", "navidad"]


def tema_del_dia(hoy: date) -> str:
    m, d = hoy.month, hoy.day
    if (m == 12 and d == 31) or (m == 1 and d <= 2):
        return "anio_nuevo"
    if m == 2 and 10 <= d <= 14:
        return "san_valentin"
    if m == 7 and 20 <= d <= 31:
        return "fiestas_patrias"
    if (m == 10 and d >= 20) or (m == 11 and d == 1):
        return "halloween"
    if m == 12 and 1 <= d <= 26:
        return "navidad"
    return "normal"


# ---------- Accesorios que lleva Apolo (coordenadas del gatito) ----------

COLLAR = """
      <path d="M100 55 Q 107 64 117 63" fill="none" stroke="#dc2626" stroke-width="5" stroke-linecap="round"/>"""

CASCABEL = """
      <circle cx="108" cy="65" r="3.5" fill="#fbbf24" stroke="#92400e" stroke-width="1.2"/>"""

ACCESORIOS = {
    "normal": CASCABEL,
    "anio_nuevo": CASCABEL + """
      <path d="M106 23 L 117 -10 L 128 23 Z" fill="#ec4899" stroke="#831843" stroke-width="2"/>
      <path d="M110 12 L 124 12 M113 2 L 121 2" stroke="#fde047" stroke-width="3" stroke-linecap="round"/>
      <circle cx="117" cy="-12" r="4.5" fill="#fde047"/>""",
    "san_valentin": CASCABEL + """
      <g class="latido"><path d="M117 4 C 112 -4, 101 0, 106 9 L 117 19 L 128 9 C 133 0, 122 -4, 117 4 Z"
        fill="#f43f5e" stroke="#881337" stroke-width="1.5"/></g>""",
    "fiestas_patrias": """
      <path d="M103 66 L 99 80 L 105 76 Z M113 66 L 117 80 L 111 76 Z" fill="#d91023"/>
      <circle cx="108" cy="65" r="8" fill="#d91023"/>
      <circle cx="108" cy="65" r="5" fill="#ffffff"/>
      <circle cx="108" cy="65" r="2" fill="#d91023"/>""",
    "halloween": CASCABEL + """
      <ellipse cx="118" cy="23" rx="24" ry="5" fill="#6d28d9" stroke="#2e1065" stroke-width="2"/>
      <path d="M105 22 L 125 -16 L 132 22 Z" fill="#7c3aed" stroke="#2e1065" stroke-width="2"/>
      <path d="M106 17 L 131 17" stroke="#f97316" stroke-width="5"/>""",
    "navidad": CASCABEL + """
      <path d="M100 24 Q 116 -16 152 8 L 138 24 Z" fill="#dc2626" stroke="#7f1d1d" stroke-width="2"/>
      <rect x="97" y="19" width="44" height="9" rx="4.5" fill="#ffffff" stroke="#d1d5db" stroke-width="1"/>
      <circle cx="153" cy="8" r="5.5" fill="#ffffff" stroke="#d1d5db" stroke-width="1"/>""",
}

# Color de la etiqueta con el nombre
COLOR_NOMBRE = {
    "normal": "#f59e0b",
    "anio_nuevo": "#ec4899",
    "san_valentin": "#f43f5e",
    "fiestas_patrias": "#d91023",
    "halloween": "#f97316",
    "navidad": "#16a34a",
}


# ---------- Decoración del suelo (fija, Apolo pasa por delante) ----------

def calabaza(x, y):
    return f"""
  <g transform="translate({x} {y})">
    <path d="M0 -30 C 2 -36, 6 -38, 8 -38" stroke="#15803d" stroke-width="4" fill="none" stroke-linecap="round"/>
    <ellipse cx="-9" cy="-14" rx="11" ry="14" fill="#ea580c" stroke="#9a3412" stroke-width="2"/>
    <ellipse cx="9" cy="-14" rx="11" ry="14" fill="#ea580c" stroke="#9a3412" stroke-width="2"/>
    <ellipse cx="0" cy="-14" rx="10" ry="15" fill="#f97316" stroke="#9a3412" stroke-width="2"/>
    <path d="M-9 -19 L -5 -24 L -1 -19 Z M1 -19 L 5 -24 L 9 -19 Z" fill="#431407"/>
    <path d="M-10 -10 L -6 -6 L -2 -10 L 2 -6 L 6 -10 L 10 -6" fill="none" stroke="#431407" stroke-width="2.5" stroke-linejoin="round"/>
  </g>"""


def arbolito(x, y):
    return f"""
  <g transform="translate({x} {y})">
    <rect x="-5" y="-12" width="10" height="12" fill="#92400e"/>
    <path d="M-28 -12 L 0 -40 L 28 -12 Z" fill="#16a34a" stroke="#14532d" stroke-width="2"/>
    <path d="M-22 -30 L 0 -56 L 22 -30 Z" fill="#16a34a" stroke="#14532d" stroke-width="2"/>
    <path d="M-15 -47 L 0 -68 L 15 -47 Z" fill="#16a34a" stroke="#14532d" stroke-width="2"/>
    <circle cx="-12" cy="-18" r="3.5" fill="#dc2626"/>
    <circle cx="10" cy="-22" r="3.5" fill="#fbbf24"/>
    <circle cx="-6" cy="-38" r="3" fill="#3b82f6"/>
    <circle cx="8" cy="-42" r="3" fill="#dc2626"/>
    <path class="brillo" d="M0 -78 L 3 -71 L 10 -71 L 4 -66 L 6 -59 L 0 -63 L -6 -59 L -4 -66 L -10 -71 L -3 -71 Z" fill="#fde047"/>
  </g>"""


def bandera(x, y):
    return f"""
  <g transform="translate({x} {y})">
    <line x1="0" y1="0" x2="0" y2="-66" stroke="#9ca3af" stroke-width="3" stroke-linecap="round"/>
    <g class="ondear">
      <rect x="2" y="-64" width="13" height="26" fill="#d91023"/>
      <rect x="15" y="-64" width="13" height="26" fill="#ffffff"/>
      <rect x="28" y="-64" width="13" height="26" fill="#d91023"/>
      <rect x="2" y="-64" width="39" height="26" fill="none" stroke="#9ca3af" stroke-width="1"/>
    </g>
  </g>"""


def confeti(x, y):
    colores = ["#ec4899", "#fde047", "#22c55e", "#3b82f6", "#f97316"]
    piezas = "".join(
        f'<rect class="brillo" x="{x + dx}" y="{y + dy}" width="5" height="9" rx="1" '
        f'fill="{colores[i % 5]}" transform="rotate({(i * 37) % 90 - 45} {x + dx} {y + dy})" '
        f'style="animation-delay:-{i * .3:.1f}s"/>'
        for i, (dx, dy) in enumerate([(-20, -60), (-6, -40), (8, -70), (20, -48), (-14, -22), (14, -18)])
    )
    return "\n  " + piezas


def corazon(x, y):
    return f"""
  <path class="latido" d="M{x} {y - 30} c -5 -8, -16 -4, -11 5 l 11 10 l 11 -10 c 5 -9, -6 -13, -11 -5 z"
    fill="#fb7185" stroke="#be123c" stroke-width="1.5"/>"""


DECORACION = {
    "normal": None,
    "anio_nuevo": confeti,
    "san_valentin": corazon,
    "fiestas_patrias": bandera,
    "halloween": calabaza,
    "navidad": arbolito,
}


def generar(tema: str, hoy: date) -> str:
    deco = DECORACION[tema]
    suelo = "".join(deco(x, 146) for x in (110, 450, 790)) if deco else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 150" width="900" height="150">
  <!-- Apolo - tema: {tema} - generado el {hoy.isoformat()} con generar_gatito.py -->
  <style>
    .paseo {{ animation: cruzar 16s linear infinite; }}
    @keyframes cruzar {{ from {{ transform: translateX(-170px); }} to {{ transform: translateX(940px); }} }}

    .pata {{ animation: paso .45s ease-in-out infinite alternate; }}
    .pata.b {{ animation-delay: -.45s; }}
    .p1 {{ transform-origin: 34px 74px; }}
    .p2 {{ transform-origin: 46px 74px; }}
    .p3 {{ transform-origin: 80px 74px; }}
    .p4 {{ transform-origin: 92px 74px; }}
    @keyframes paso {{ from {{ transform: rotate(-18deg); }} to {{ transform: rotate(18deg); }} }}

    .cuerpo {{ animation: rebote .45s ease-in-out infinite alternate; }}
    @keyframes rebote {{ to {{ transform: translateY(-2px); }} }}

    .cola {{ transform-origin: 22px 60px; animation: mecer 1.2s ease-in-out infinite alternate; }}
    @keyframes mecer {{ from {{ transform: rotate(-12deg); }} to {{ transform: rotate(14deg); }} }}

    .ojos {{ transform-origin: 118px 39px; animation: parpadear 4s infinite; }}
    @keyframes parpadear {{ 0%, 92%, 100% {{ transform: scaleY(1); }} 95% {{ transform: scaleY(.1); }} }}

    .brillo {{ animation: brillar 1.6s ease-in-out infinite alternate; }}
    @keyframes brillar {{ from {{ opacity: 1; }} to {{ opacity: .35; }} }}

    .latido {{ transform-box: fill-box; transform-origin: center; animation: latir .8s ease-in-out infinite alternate; }}
    @keyframes latir {{ to {{ transform: scale(1.15); }} }}

    .ondear {{ transform-box: fill-box; transform-origin: left center; animation: ondear 1.4s ease-in-out infinite alternate; }}
    @keyframes ondear {{ to {{ transform: skewY(6deg) scaleX(.94); }} }}

    .pelo {{ fill: #26262c; stroke: #8b8f9a; stroke-width: 2.5; }}
    .raya {{ fill: none; stroke: #55556a; stroke-width: 4; stroke-linecap: round; }}
    .bigote {{ stroke: #c4c7cf; stroke-width: 1.5; stroke-linecap: round; }}
  </style>
{suelo}

  <g class="paseo">
    <g transform="translate(0 46)">
      <rect class="pata p2 b pelo" x="42" y="68" width="10" height="30" rx="5" style="fill:#1b1b20"/>
      <rect class="pata p4 pelo" x="88" y="68" width="10" height="30" rx="5" style="fill:#1b1b20"/>

      <g class="cuerpo">
        <path class="cola" d="M24 60 C 4 54, -6 34, 6 16" fill="none" stroke="#8b8f9a" stroke-width="11" stroke-linecap="round"/>
        <path class="cola" d="M24 60 C 4 54, -6 34, 6 16" fill="none" stroke="#26262c" stroke-width="7" stroke-linecap="round"/>
        <ellipse class="pelo" cx="62" cy="62" rx="44" ry="21"/>
        <path class="raya" d="M48 44 C 50 52, 50 58, 46 66"/>
        <path class="raya" d="M62 42 C 64 50, 64 58, 60 68"/>
        <path class="raya" d="M76 43 C 78 50, 78 56, 74 64"/>

        <path class="pelo" d="M98 30 L 101 8 L 114 24 Z"/>
        <path class="pelo" d="M120 24 L 132 8 L 134 32 Z"/>
        <path d="M102 26 L 103 14 L 110 23 Z" fill="#f9a8b8"/>
        <path d="M124 24 L 130 14 L 131 29 Z" fill="#f9a8b8"/>
        <circle class="pelo" cx="117" cy="42" r="21"/>
        <path class="raya" d="M112 24 L 113 30 M118 23 L 118 29 M124 24 L 123 30" stroke-width="2.5"/>
        <g class="ojos">
          <ellipse cx="110" cy="39" rx="4.5" ry="5.5" fill="#facc15"/>
          <ellipse cx="125" cy="39" rx="4.5" ry="5.5" fill="#facc15"/>
          <ellipse cx="111" cy="39" rx="1.4" ry="4.5" fill="#111"/>
          <ellipse cx="126" cy="39" rx="1.4" ry="4.5" fill="#111"/>
        </g>
        <path d="M115 47 L 121 47 L 118 50.5 Z" fill="#f472b6"/>
        <path d="M118 50.5 C 116 54, 112 54, 111 52 M118 50.5 C 120 54, 124 54, 125 52" fill="none" stroke="#8b8f9a" stroke-width="1.5" stroke-linecap="round"/>
        <line class="bigote" x1="126" y1="48" x2="146" y2="44"/>
        <line class="bigote" x1="126" y1="51" x2="146" y2="52"/>
        <line class="bigote" x1="110" y1="48" x2="92" y2="44"/>
        <line class="bigote" x1="110" y1="51" x2="92" y2="52"/>
{COLLAR}{ACCESORIOS[tema]}

        <rect x="34" y="10" width="56" height="20" rx="10" fill="{COLOR_NOMBRE[tema]}"/>
        <text x="62" y="24.5" text-anchor="middle" font-family="system-ui, -apple-system, Segoe UI, sans-serif"
          font-size="13" font-weight="700" fill="#ffffff">Apolo</text>
      </g>

      <rect class="pata p1 pelo" x="30" y="68" width="10" height="30" rx="5"/>
      <rect class="pata p3 b pelo" x="76" y="68" width="10" height="30" rx="5"/>
    </g>
  </g>
</svg>
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tema", choices=TEMAS + ["todos"], help="forzar un tema en vez de usar la fecha")
    args = parser.parse_args()

    carpeta = Path(__file__).parent
    hoy = datetime.now(PERU).date()

    if args.tema == "todos":
        (carpeta / "ejemplos").mkdir(exist_ok=True)
        for t in TEMAS:
            (carpeta / "ejemplos" / f"{t}.svg").write_text(generar(t, hoy), encoding="utf-8")
        print("Ejemplos en", carpeta / "ejemplos")
    else:
        tema = args.tema or tema_del_dia(hoy)
        (carpeta / "gatito.svg").write_text(generar(tema, hoy), encoding="utf-8")
        print(f"gatito.svg generado con el tema: {tema}")
