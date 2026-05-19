"""
embeddings.py
=============

Programa educativo que genera embeddings (vectores semánticos) a partir
de un archivo de texto, usando un modelo de embeddings desplegado en
Microsoft Foundry.

Para cada línea del archivo de entrada se calcula un vector y se escriben
dos archivos compatibles con el TensorFlow Embedding Projector
(https://projector.tensorflow.org):

    - vectors.tsv  -> una línea por vector, valores separados por tabulación
    - metadata.tsv -> una línea por texto original (etiquetas del vector)

Lectura de credenciales desde un archivo .env con las variables:

    AZURE_FOUNDRY_ENDPOINT   = https://<recurso>.services.ai.azure.com/models
    AZURE_FOUNDRY_KEY        = <clave de API>
    AZURE_FOUNDRY_DEPLOYMENT = <nombre del modelo desplegado, p.ej. text-embedding-3-small>
"""

import os
import sys
from pathlib import Path

# --- Librerías de terceros -------------------------------------------------
# python-dotenv: carga las variables del archivo .env en el entorno.
# azure-ai-inference: cliente oficial para llamar a modelos de Foundry.
# rich: interfaz de consola con colores, paneles y barras de progreso.
from dotenv import load_dotenv
from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
)
from rich.table import Table


# Una única consola Rich para todo el programa.
console = Console()


# ---------------------------------------------------------------------------
# 1. Configuración: cargar credenciales desde .env
# ---------------------------------------------------------------------------
def cargar_configuracion() -> tuple[str, str, str]:
    """
    Lee las tres variables necesarias desde el archivo .env y las devuelve.

    Si falta alguna, muestra un mensaje claro y termina el programa.
    """
    # load_dotenv() busca un archivo .env en el directorio actual y carga
    # sus variables en os.environ. No sobreescribe variables ya definidas.
    load_dotenv()

    endpoint = os.getenv("AZURE_FOUNDRY_ENDPOINT")
    key = os.getenv("AZURE_FOUNDRY_KEY")
    deployment = os.getenv("AZURE_FOUNDRY_DEPLOYMENT")

    # Validamos que las tres variables estén presentes.
    faltantes = [
        nombre
        for nombre, valor in [
            ("AZURE_FOUNDRY_ENDPOINT", endpoint),
            ("AZURE_FOUNDRY_KEY", key),
            ("AZURE_FOUNDRY_DEPLOYMENT", deployment),
        ]
        if not valor
    ]

    if faltantes:
        console.print(
            Panel.fit(
                "[bold red]Faltan variables en el archivo .env[/bold red]\n\n"
                + "\n".join(f"  • {nombre}" for nombre in faltantes)
                + "\n\nCrea un archivo [bold].env[/bold] con el siguiente formato:\n\n"
                "[dim]AZURE_FOUNDRY_ENDPOINT=https://<recurso>.services.ai.azure.com/models\n"
                "AZURE_FOUNDRY_KEY=<tu-clave>\n"
                "AZURE_FOUNDRY_DEPLOYMENT=text-embedding-3-small[/dim]",
                title="Configuración incompleta",
                border_style="red",
            )
        )
        sys.exit(1)

    return endpoint, key, deployment


# ---------------------------------------------------------------------------
# 2. Lectura del archivo de entrada
# ---------------------------------------------------------------------------
def leer_lineas(ruta: Path) -> list[str]:
    """
    Lee el archivo y devuelve una lista con las líneas no vacías.

    - Se eliminan los saltos de línea finales con .rstrip().
    - Se omiten las líneas en blanco para no generar vectores inútiles.
    """
    if not ruta.exists():
        console.print(f"[bold red]El archivo no existe:[/bold red] {ruta}")
        sys.exit(1)

    # Leemos con UTF-8 que es el estándar moderno y soporta acentos/eñes.
    with ruta.open("r", encoding="utf-8") as archivo:
        # rstrip("\n") preserva espacios internos pero quita el salto final.
        # Filtramos líneas vacías o que solo tengan espacios.
        lineas = [linea.rstrip("\n") for linea in archivo if linea.strip()]

    if not lineas:
        console.print("[bold yellow]El archivo está vacío.[/bold yellow]")
        sys.exit(1)

    return lineas


# ---------------------------------------------------------------------------
# 3. Cliente de embeddings de Microsoft Foundry
# ---------------------------------------------------------------------------
def crear_cliente(endpoint: str, key: str) -> EmbeddingsClient:
    """
    Construye el cliente que se comunica con el modelo desplegado en Foundry.

    Usa autenticación por clave (AzureKeyCredential). Para producción se
    recomienda Microsoft Entra ID con DefaultAzureCredential.
    """
    return EmbeddingsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )


def obtener_embedding(
    cliente: EmbeddingsClient, texto: str, deployment: str
) -> list[float]:
    """
    Pide a Foundry el embedding de un único texto.

    Devuelve una lista de números flotantes (la dimensión depende del modelo;
    por ejemplo text-embedding-3-small produce 1536 dimensiones).
    """
    # La API admite varios textos a la vez en 'input', pero aquí pedimos
    # uno solo para poder mostrar el progreso línea a línea.
    respuesta = cliente.embed(input=[texto], model=deployment)
    return respuesta.data[0].embedding


# ---------------------------------------------------------------------------
# 4. Escritura de los archivos de salida
# ---------------------------------------------------------------------------
def escribir_tsv(
    vectores: list[list[float]],
    textos: list[str],
    ruta_vectores: Path,
    ruta_metadata: Path,
) -> None:
    """
    Guarda los dos archivos en el formato del Embedding Projector.

    - vectors.tsv: cada fila son los componentes del vector separados por \\t.
    - metadata.tsv: cada fila es el texto original que dio origen al vector.

    El orden de las filas se mantiene exactamente igual en ambos archivos
    para que cada vector quede asociado a su etiqueta correspondiente.
    """
    with ruta_vectores.open("w", encoding="utf-8") as f_vec:
        for vector in vectores:
            # Convertimos cada float a string con suficiente precisión.
            f_vec.write("\t".join(f"{valor:.8f}" for valor in vector) + "\n")

    with ruta_metadata.open("w", encoding="utf-8") as f_meta:
        for texto in textos:
            # Sustituimos tabulaciones internas por espacios para no romper
            # el formato TSV (columna única, una línea por entrada).
            f_meta.write(texto.replace("\t", " ") + "\n")


# ---------------------------------------------------------------------------
# 5. Programa principal
# ---------------------------------------------------------------------------
def main() -> None:
    # Encabezado visual del programa.
    console.print(
        Panel.fit(
            "[bold cyan]Generador de Embeddings[/bold cyan]\n"
            "[dim]Microsoft Foundry · Azure AI Inference SDK[/dim]",
            border_style="cyan",
        )
    )

    # 1) Cargar credenciales.
    endpoint, key, deployment = cargar_configuracion()

    # Mostramos un resumen de la configuración (ocultando la clave por seguridad).
    tabla = Table(show_header=False, box=None, padding=(0, 1))
    tabla.add_column(style="bold")
    tabla.add_column()
    tabla.add_row("Endpoint:", endpoint)
    tabla.add_row("Deployment:", deployment)
    tabla.add_row("Clave:", f"{key[:4]}…{key[-4:]}  [dim](oculta)[/dim]")
    console.print(tabla)
    console.print()

    # 2) Preguntar al usuario por el archivo de entrada.
    #    Prompt.ask repite la pregunta hasta obtener una respuesta válida.
    nombre_archivo = Prompt.ask(
        "[bold]Nombre del archivo de texto[/bold]",
        default="entrada.txt",
    )
    ruta_entrada = Path(nombre_archivo).expanduser().resolve()

    # 3) Leer el archivo.
    lineas = leer_lineas(ruta_entrada)
    console.print(
        f"[green]✓[/green] Se leyeron [bold]{len(lineas)}[/bold] líneas "
        f"desde [italic]{ruta_entrada.name}[/italic]"
    )

    # 4) Crear el cliente de Foundry.
    cliente = crear_cliente(endpoint, key)

    # 5) Calcular el embedding de cada línea con barra de progreso.
    vectores: list[list[float]] = []
    fallos: list[tuple[int, str]] = []  # Guardamos errores para reportarlos al final.

    # Configuramos columnas ricas: spinner, descripción, barra, conteo, tiempos.
    columnas = [
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        TextColumn("•"),
        TimeRemainingColumn(),
    ]

    with Progress(*columnas, console=console) as progreso:
        tarea = progreso.add_task(
            "[cyan]Generando embeddings…", total=len(lineas)
        )

        for indice, texto in enumerate(lineas, start=1):
            try:
                vector = obtener_embedding(cliente, texto, deployment)
                vectores.append(vector)
            except HttpResponseError as error:
                # Capturamos errores HTTP (autenticación, cuota, modelo no
                # encontrado, etc.) sin abortar todo el proceso.
                fallos.append((indice, str(error)))
                # Para mantener la correspondencia 1-a-1 entre vectors.tsv
                # y metadata.tsv, descartamos también el texto.
                vectores.append(None)  # type: ignore[arg-type]

            # Avanzamos la barra después de cada línea.
            progreso.update(tarea, advance=1)

    # 6) Filtrar las líneas que fallaron para mantener archivos coherentes.
    pares_validos = [
        (texto, vec)
        for texto, vec in zip(lineas, vectores)
        if vec is not None
    ]

    if not pares_validos:
        console.print("[bold red]No se pudo generar ningún embedding.[/bold red]")
        sys.exit(1)

    textos_validos, vectores_validos = zip(*pares_validos)

    # 7) Escribir los archivos TSV en el mismo directorio del script.
    ruta_vectores = Path("vectors.tsv").resolve()
    ruta_metadata = Path("metadata.tsv").resolve()
    escribir_tsv(
        list(vectores_validos),
        list(textos_validos),
        ruta_vectores,
        ruta_metadata,
    )

    # 8) Mostrar resumen final.
    dimension = len(vectores_validos[0])
    resumen = Table(title="Resumen", title_style="bold green", show_header=False)
    resumen.add_column(style="bold")
    resumen.add_column()
    resumen.add_row("Líneas procesadas:", str(len(lineas)))
    resumen.add_row("Embeddings generados:", str(len(vectores_validos)))
    resumen.add_row("Errores:", str(len(fallos)))
    resumen.add_row("Dimensión del vector:", str(dimension))
    resumen.add_row("Archivo de vectores:", str(ruta_vectores))
    resumen.add_row("Archivo de metadatos:", str(ruta_metadata))
    console.print()
    console.print(resumen)

    # Si hubo errores parciales, los listamos al final.
    if fallos:
        console.print()
        console.print("[bold yellow]Detalles de los errores:[/bold yellow]")
        for indice, mensaje in fallos:
            console.print(f"  [red]✗[/red] Línea {indice}: {mensaje}")

    console.print(
        "\n[dim]Sube los dos archivos a "
        "https://projector.tensorflow.org para visualizarlos.[/dim]"
    )


if __name__ == "__main__":
    main()
