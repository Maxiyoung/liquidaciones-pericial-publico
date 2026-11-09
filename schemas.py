#!/usr/bin/env python3
"""Contratos de datos (Data Schemas) del Pipeline de Liquidación y Peritaje Vial.

Este módulo documenta la estructura tipada de los contratos JSON utilizados entre
los agentes multimodales y los motores determinísticos del repositorio privado:
  - `DatosCasoSchema`: Fuente única de verdad del siniestro (`datos.json`).
  - `ExtraidoFotosSchema`: Transcripción estricta de visión artificial para
    auditoría cruzada a doble ciego (`extraido_fotos.json`).
  - `RelevamientoVialSchema`: Salida geoespacial de intersecciones (`lugar.json`).
"""
from dataclasses import dataclass, field
from typing import List, Literal, Optional

OrientacionEje = Literal["norte-sur", "este-oeste"]
SentidoCirculacion = Literal["norte", "sur", "este", "oeste", "doble"]
RumboCardinal = Literal["norte", "sur", "este", "oeste"]
ManiobraVial = Literal["recto", "izquierda", "derecha", "retorno"]
CuadranteImpacto = Literal["centro", "noreste", "noroeste", "sureste", "suroeste"]


@dataclass(frozen=True)
class DestinatarioInforme:
    """Datos de la compañía aseguradora y área destinataria del dictamen."""
    compania: str
    area: str = "Dto. Legales."
    atencion: str = ""


@dataclass(frozen=True)
class DatosSiniestro:
    """Metadatos principales del hecho investigado."""
    numero: str
    titular: str
    domicilio_titular: str
    fecha_ocurrencia: str
    hora: str
    lugar: str


@dataclass(frozen=True)
class VehiculoParticipe:
    """Identificación técnica de un rodado interviniente (asegurado o tercero)."""
    marca: str
    modelo: str
    tipo: str
    dominio: str


@dataclass(frozen=True)
class ConductorParticipe:
    """Datos filiatorios y habilitación para conducir de un conductor."""
    nombre: str
    dni: str
    licencia: str = ""
    vigencia: str = ""
    categoria: str = ""
    t_medica: str = ""
    observ: str = ""
    domicilio: str = ""


@dataclass(frozen=True)
class ArteriaCroquis:
    """Definición geométrica y vial de una arteria en la intersección."""
    nombre: str
    orientacion: OrientacionEje
    sentido: SentidoCirculacion


@dataclass(frozen=True)
class TrayectoriaVehiculo:
    """Vector de aproximación y maniobra de un rodado para el trazado del croquis."""
    calle: Literal["a", "b"]
    viene_desde: RumboCardinal
    maniobra: ManiobraVial = "recto"


@dataclass(frozen=True)
class ConfiguracionCroquis:
    """Parámetros de entrada del motor gráfico planimétrico (`croquis.py`)."""
    calle_a: ArteriaCroquis
    calle_b: ArteriaCroquis
    asegurado: TrayectoriaVehiculo
    tercero: TrayectoriaVehiculo
    punto_impacto: CuadranteImpacto = "centro"
    referencias: str = ""


@dataclass
class ExpedienteSiniestro:
    """Estructura raíz consolidada del expediente pericial (`datos.json`)."""
    ciudad: str
    fecha: str
    destinatario: DestinatarioInforme
    siniestro: DatosSiniestro
    vehiculo_asegurado: VehiculoParticipe
    vehiculo_tercero: VehiculoParticipe
    conductor_asegurado: ConductorParticipe
    conductor_tercero: ConductorParticipe
    croquis: Optional[ConfiguracionCroquis] = None
    testigos: str = ""
    exclusion_cobertura: str = ""
    causales_rechazo: str = "Ver apartado conclusión.-"
    estado_rodado_asegurado: str = ""
    entrevista_asegurado: List[str] = field(default_factory=list)
    entrevista_tercero: List[str] = field(default_factory=list)
    ambiental: List[str] = field(default_factory=list)
    testigos_hecho: str = ""
    atenciones_medicas: str = ""
    conclusion: List[str] = field(default_factory=list)
    firmante: str = ""
