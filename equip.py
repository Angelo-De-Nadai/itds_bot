#!/usr/bin/env python3.10

from typing import Optional
from strenum import StrEnum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from dataclass_wizard import YAMLWizard
from decimal import *

Conio = StrEnum('Conio',[ 'denari', 'soldi', 'lire' ])
Qualità = StrEnum('Qualità', [ 'normale', 'buona', 'eccellente', 'ottima', 'straordinaria', 'scadente' ])
TipoOggetto = StrEnum('TipoOggetto',[ 'vesti', 'attrezzature delle abilità', 'attrezzature da viaggio', 'armi', 'armature', 'composti', 'animali', 'contenitori', 'finimenti' ])

@dataclass_json
@dataclass
class Oggetto(YAMLWizard):
  nome      : str           = ''
  qualità   : Qualità       = 'normale'
  categoria : TipoOggetto   = 'vesti'
  costo     : int           = 0
  conio     : Conio         = 'denari'
  peso      : Decimal       = Decimal(0)
  pregi     : list[str]     = field(default_factory=list)
  movimento : Optional[int] = None # solo animali
  abilità   : Optional[list[str]] = None # solo attrezzature
  ceto      : Optional[str] = None # Ceto, ma non è ancora inizializzato
  carico    : Optional[int] = None # solo contenitori e animali

  def __getitem__(self, item):
    return getattr(self, item)

  def __setitem__(self, item, value):
    return setattr(self, item, value)

@dataclass_json
@dataclass
class Arma(Oggetto):
  categoria : TipoOggetto   = 'armi'
  abilità  : str = 'armi comuni'
  danno    : int = 0
  tipo     : str = 'T'
  parata   : int = 0
  misura   : str = 'stretta'
  gittata  : int = 0
  ricarica : int = 0

@dataclass_json
@dataclass
class Armatura(Oggetto):
  categoria : TipoOggetto   = 'armature'
  protezione : int = 0

@dataclass_json
@dataclass
class ListaEquip(YAMLWizard):
  armi     : dict[str,Arma]     = field(default_factory=dict)
  armature : dict[str,Armatura] = field(default_factory=dict)
  oggetti  : dict[str,Oggetto]  = field(default_factory=dict)

  def __post_init__(self):
    for a in self.armi : 
      if self.armi[a].nome=='' : self.armi[a].nome=a
    for a in self.armature : 
      if self.armature[a].nome=='' : self.armature[a].nome=a
    for a in self.oggetti : 
      if self.oggetti[a].nome=='' : self.oggetti[a].nome=a

# Carica i dati esterni dai file YAML corrispondenti
import yaml
with open("data/equipaggiamento.yaml","r") as fin:
  equip = ListaEquip.from_yaml(fin.read())


