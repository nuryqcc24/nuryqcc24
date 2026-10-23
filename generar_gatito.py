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

CASCABEL = """
        <circle cx="101" cy="79" r="4" fill="#fbbf24" stroke="#92400e" stroke-width="1.2"/>
        <path d="M98.5 79.5 L 103.5 79.5" stroke="#92400e" stroke-width="1"/>"""

ESCARAPELA = """
        <path d="M96 80 L 92 93 L 98 89 Z M106 80 L 110 93 L 104 89 Z" fill="#d91023"/>
        <circle cx="101" cy="79" r="8" fill="#d91023"/>
        <circle cx="101" cy="79" r="5" fill="#ffffff"/>
        <circle cx="101" cy="79" r="2" fill="#d91023"/>"""

# lo que va en el cuello
CUELLO = {tema: CASCABEL for tema in TEMAS}
CUELLO["fiestas_patrias"] = ESCARAPELA

# lo que va en la cabeza (se mueve con ella)
SOMBRERO = {
    "normal": "",
    "fiestas_patrias": "",
    "anio_nuevo": """
          <path d="M94 20 L 105 -12 L 116 20 Z" fill="#ec4899" stroke="#831843" stroke-width="2" stroke-linejoin="round"/>
          <path d="M98 10 L 112 10 M101 0 L 109 0" stroke="#fde047" stroke-width="3" stroke-linecap="round"/>
          <circle cx="105" cy="-14" r="4.5" fill="#fde047"/>""",
    "san_valentin": """
          <path class="latido" d="M105 -2 C 100 -10, 89 -6, 94 3 L 105 13 L 116 3 C 121 -6, 110 -10, 105 -2 Z"
            fill="#f43f5e" stroke="#881337" stroke-width="1.5"/>""",
    "halloween": """
          <ellipse cx="105" cy="22" rx="28" ry="6" fill="#6d28d9" stroke="#2e1065" stroke-width="2"/>
          <path d="M90 21 L 110 -20 Q 112 -22 113 -18 L 121 21 Z" fill="#7c3aed" stroke="#2e1065" stroke-width="2" stroke-linejoin="round"/>
          <path d="M92 15 L 119 15" stroke="#f97316" stroke-width="5"/>""",
    "navidad": """
          <path d="M86 24 Q 104 -18 142 6 L 126 24 Z" fill="#dc2626" stroke="#7f1d1d" stroke-width="2" stroke-linejoin="round"/>
          <rect x="82" y="18" width="48" height="10" rx="5" fill="#ffffff" stroke="#d1d5db" stroke-width="1"/>
          <circle cx="143" cy="6" r="6" fill="#ffffff" stroke="#d1d5db" stroke-width="1"/>""",
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
    .paseo {{ animation: cruzar 18s linear infinite; }}
    @keyframes cruzar {{ from {{ transform: translateX(-160px); }} to {{ transform: translateX(940px); }} }}

    /* pasitos cortos y rápidos */
    .pata {{ animation: paso .35s ease-in-out infinite alternate; }}
    .pata.b {{ animation-delay: -.35s; }}
    .p1 {{ transform-origin: 36px 82px; }}
    .p2 {{ transform-origin: 48px 82px; }}
    .p3 {{ transform-origin: 72px 82px; }}
    .p4 {{ transform-origin: 84px 82px; }}
    @keyframes paso {{ from {{ transform: rotate(-16deg); }} to {{ transform: rotate(16deg); }} }}

    .cuerpo {{ animation: rebote .35s ease-in-out infinite alternate; }}
    @keyframes rebote {{ to {{ transform: translateY(-2.5px); }} }}

    /* la cabeza se inclina de un lado a otro, con curiosidad */
    .cabeza {{ transform-origin: 104px 64px; animation: inclinar 2.6s ease-in-out infinite alternate; }}
    @keyframes inclinar {{ from {{ transform: rotate(-5deg); }} to {{ transform: rotate(5deg); }} }}

    .cola {{ transform-origin: 26px 68px; animation: mecer 1.1s ease-in-out infinite alternate; }}
    @keyframes mecer {{ from {{ transform: rotate(-10deg); }} to {{ transform: rotate(16deg); }} }}

    .ojos {{ transform-origin: 105px 48px; animation: parpadear 4s infinite; }}
    @keyframes parpadear {{ 0%, 93%, 100% {{ transform: scaleY(1); }} 96% {{ transform: scaleY(.1); }} }}

    .brillo {{ animation: brillar 1.6s ease-in-out infinite alternate; }}
    @keyframes brillar {{ from {{ opacity: 1; }} to {{ opacity: .35; }} }}

    .latido {{ transform-box: fill-box; transform-origin: center; animation: latir .8s ease-in-out infinite alternate; }}
    @keyframes latir {{ to {{ transform: scale(1.15); }} }}

    .ondear {{ transform-box: fill-box; transform-origin: left center; animation: ondear 1.4s ease-in-out infinite alternate; }}
    @keyframes ondear {{ to {{ transform: skewY(6deg) scaleX(.94); }} }}

    .pelo {{ fill: #2a2a33; stroke: #9095a3; stroke-width: 2.5; stroke-linejoin: round; }}
    .raya {{ fill: none; stroke: #4d4d5e; stroke-width: 3.5; stroke-linecap: round; }}
    .bigote {{ stroke: #c4c7cf; stroke-width: 1.4; stroke-linecap: round; }}
  </style>
{suelo}

  <g class="paseo">
    <g transform="translate(0 48)">
      <!-- patitas de atrás -->
      <rect class="pata p2 b pelo" x="42" y="80" width="12" height="16" rx="6" style="fill:#202028"/>
      <rect class="pata p4 pelo" x="78" y="80" width="12" height="16" rx="6" style="fill:#202028"/>

      <g class="cuerpo">
        <!-- colita enroscada -->
        <path class="cola" d="M26 68 C 6 66, 2 44, 14 38 C 23 34, 28 43, 21 47" fill="none" stroke="#9095a3" stroke-width="12" stroke-linecap="round"/>
        <path class="cola" d="M26 68 C 6 66, 2 44, 14 38 C 23 34, 28 43, 21 47" fill="none" stroke="#2a2a33" stroke-width="7" stroke-linecap="round"/>

        <!-- cuerpito redondo con rayitas -->
        <ellipse class="pelo" cx="57" cy="72" rx="34" ry="20"/>
        <path class="raya" d="M44 55 C 46 61, 46 66, 43 71"/>
        <path class="raya" d="M56 53 C 58 60, 58 66, 55 72"/>
        <path class="raya" d="M68 54 C 70 60, 70 65, 67 70"/>
        <ellipse cx="62" cy="82" rx="18" ry="6" fill="#3a3a46"/>

        <!-- collar -->
        <path d="M86 70 Q 101 80 118 71" fill="none" stroke="#dc2626" stroke-width="5" stroke-linecap="round"/>
        {CUELLO[tema]}

        <g class="cabeza">
          <!-- orejitas redondeadas -->
          <path class="pelo" d="M80 36 C 75 20, 79 9, 86 10 C 92 11, 98 18, 101 24 Z"/>
          <path class="pelo" d="M109 23 C 113 17, 121 9, 127 11 C 133 13, 133 24, 130 36 Z"/>
          <path d="M84 30 C 82 21, 84 15, 87 15 C 91 16, 94 20, 96 23 Z" fill="#f9a8c8"/>
          <path d="M114 23 C 117 19, 121 15, 124 15 C 127 16, 127 23, 126 29 Z" fill="#f9a8c8"/>

          <!-- cabezota redondita -->
          <ellipse class="pelo" cx="105" cy="48" rx="31" ry="27"/>
          <path class="raya" d="M98 23 L 99 29 M105 22 L 105 28 M112 23 L 111 29" stroke-width="2.5"/>

          <!-- ojazos brillantes -->
          <g class="ojos">
            <circle cx="93" cy="48" r="8" fill="#facc15"/>
            <circle cx="117" cy="48" r="8" fill="#facc15"/>
            <circle cx="94" cy="49" r="5.8" fill="#111118"/>
            <circle cx="118" cy="49" r="5.8" fill="#111118"/>
            <circle cx="91.5" cy="46" r="2.4" fill="#ffffff"/>
            <circle cx="115.5" cy="46" r="2.4" fill="#ffffff"/>
            <circle cx="96" cy="51.5" r="1.1" fill="#ffffff"/>
            <circle cx="120" cy="51.5" r="1.1" fill="#ffffff"/>
          </g>

          <!-- cachetes, naricita y boquita "w" -->
          <ellipse cx="83" cy="59" rx="5.5" ry="3.2" fill="#f472b6" opacity=".55"/>
          <ellipse cx="127" cy="59" rx="5.5" ry="3.2" fill="#f472b6" opacity=".55"/>
          <path d="M102.5 55.5 L 107.5 55.5 L 105 58.5 Z" fill="#f9a8c8" stroke-linejoin="round"/>
          <path d="M100 60 Q 102.5 64 105 60 Q 107.5 64 110 60" fill="none" stroke="#c4c7cf" stroke-width="1.6" stroke-linecap="round"/>
          <line class="bigote" x1="122" y1="56" x2="138" y2="53"/>
          <line class="bigote" x1="122" y1="59" x2="138" y2="60"/>
          <line class="bigote" x1="88" y1="56" x2="72" y2="53"/>
          <line class="bigote" x1="88" y1="59" x2="72" y2="60"/>
          {SOMBRERO[tema]}
        </g>

        <!-- etiqueta con su nombre -->
        <rect x="18" y="20" width="56" height="20" rx="10" fill="{COLOR_NOMBRE[tema]}"/>
        <text x="46" y="34.5" text-anchor="middle" font-family="system-ui, -apple-system, Segoe UI, sans-serif"
          font-size="13" font-weight="700" fill="#ffffff">Apolo</text>
      </g>

      <!-- patitas de adelante -->
      <rect class="pata p1 pelo" x="30" y="80" width="12" height="16" rx="6"/>
      <rect class="pata p3 b pelo" x="66" y="80" width="12" height="16" rx="6"/>
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
