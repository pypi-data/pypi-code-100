import re
import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Iterable, Set, Union

import libsbml

if TYPE_CHECKING:
    from .. import Compound, Model, Reaction
    from ..core.gene import MonomerLink


@dataclass
class Unit:
    kind: libsbml.UnitDefinition
    scale: int
    multiplier: int
    exponent: float


@dataclass
class UnitDefinition:
    name: str
    units: Iterable[Unit]


SBML_DOT = "__SBML_DOT__"
RE_TO_SBML = re.compile(r"([^0-9_a-zA-Z])")


def _escape_non_alphanum(non_ascii: re.Match) -> str:
    """converts a non alphanumeric character to a string representation of
    its ascii number"""
    return "__" + str(ord(non_ascii.group())) + "__"


def _format_name_to_sbml(sid: str, prefix: str = "") -> str:
    sid = RE_TO_SBML.sub(_escape_non_alphanum, sid)
    sid = sid.replace(".", SBML_DOT)
    return f"{prefix}{sid}"


def export_model_name(model: "Model", sbml_model: libsbml.Model) -> None:
    if model.name is not None:
        sbml_model.setId(_format_name_to_sbml(model.name))  # str
        sbml_model.setMetaId(f"meta_{model.name}")  # str
        sbml_model.setName(model.name)  # str
    else:
        sbml_model.setMetaId("meta_model")  # str


def export_model_annotations(model: "Model", sbml_model: libsbml.Model) -> None:
    raise NotImplementedError


def export_model_notes(model: "Model", sbml_model: libsbml.Model) -> None:
    raise NotImplementedError


def export_model_meta_data(model: "Model", sbml_model: libsbml.Model) -> None:
    raise NotImplementedError


def export_units(model: "Model", sbml_model: libsbml.Model) -> None:
    default = UnitDefinition(
        name="mmol_per_gDW_per_hr",
        units=[
            Unit(kind=libsbml.UNIT_KIND_MOLE, scale=-3, multiplier=1, exponent=1.0),
            Unit(kind=libsbml.UNIT_KIND_GRAM, scale=0, multiplier=1, exponent=-1.0),
            Unit(kind=libsbml.UNIT_KIND_SECOND, scale=0, multiplier=3600, exponent=-1.0),
        ],
    )

    flux_udef: libsbml.UnitDefinition = sbml_model.createUnitDefinition()
    flux_udef.setId(_format_name_to_sbml(default.name))  # str
    for u in default.units:
        unit: libsbml.Unit = flux_udef.createUnit()
        unit.setKind(u.kind)
        unit.setExponent(u.exponent)  # int
        unit.setScale(u.scale)  # int
        unit.setMultiplier(u.multiplier)  # float


def export_compartments(model: "Model", sbml_model: libsbml.Model) -> None:
    for name, suffix in model.compartments.items():
        compartment: libsbml.Compartment = sbml_model.createCompartment()

        if compartment.setId(_format_name_to_sbml(suffix)) != libsbml.LIBSBML_OPERATION_SUCCESS:  # str
            warnings.warn(f"Could not set compartment id {suffix}")

        if compartment.setName(name) != libsbml.LIBSBML_OPERATION_SUCCESS:  # str
            warnings.warn(f"Could not set compartment name {name}")

        compartment.setConstant(True)  # bool


def _add_identifier_annotation(
    element: Union["Compound", "Reaction", "MonomerLink"],
    sbml_element: Union[libsbml.Species, libsbml.Reaction],
    db_to_resource: Dict[str, str],
) -> None:
    for db, data in element.database_links.items():
        if (resource := db_to_resource.get(db)) is not None:
            for item in data:
                cv: libsbml.CVTerm = libsbml.CVTerm()
                cv.setQualifierType(libsbml.BIOLOGICAL_QUALIFIER)
                cv.setBiologicalQualifierType(libsbml.BQB_IS)
                cv.addResource(f"https://identifiers.org/{resource}:{item}")  # str
                sbml_element.addCVTerm(cv)


def export_compounds(model: "Model", sbml_model: libsbml.Model) -> None:
    db_to_resource = {
        "BIGG": "bigg.metabolite",
        "BRENDA-COMPOUND": "brenda",
        "CAS": "cas",
        "CHEBI": "CHEBI",
        "CHEMSPIDER": "CHEMSPIDER",
        "DRUGBANK": "drugbank",
        # "ECOCYC": None,
        "HMDB": "HMDB",
        "KEGG": "kegg.compound",
        "KEGG-GLYCAN": "kegg.glycan",
        "KNAPSACK": "knapsack",
        # "LIGAND-CPD": None,
        # "LIPID_MAPS": None,
        # "MEDIADB": None,
        "METABOLIGHTS": "metabolights",
        "METANETX": "metanetx.chemical",
        # "NCI": None,
        "PUBCHEM": "pubchem.compound",
        "PUBCHEM-SID": "pubchem.substance",
        "REACTOME-CPD": "reactome",
        # "REFMET": None,
        "SEED": "seed.compound",
        "UM-BBD-CPD": "umbbd.compound",
    }

    for cpd in model.compounds.values():
        specie: libsbml.Species = sbml_model.createSpecies()
        id_ = _format_name_to_sbml(cpd.id, "M_")
        if not specie.setId(id_) == libsbml.LIBSBML_OPERATION_SUCCESS:  # str
            warnings.warn(f"Could not export name of specie {id_}")
        specie.setMetaId(f"meta_{cpd.id}")  # str, needed for annotations
        if (name := cpd.name) is not None:
            specie.setName(name)  # str
        specie.setConstant(False)  # bool
        specie.setBoundaryCondition(False)  # bool
        specie.setHasOnlySubstanceUnits(False)  # bool
        specie.setCompartment(model.compartments[cpd.compartment])  # str

        s_fbc: libsbml.FbcSpeciesPlugin = specie.getPlugin("fbc")
        if cpd.charge is not None:
            s_fbc.setCharge(int(cpd.charge))  # int
        if cpd.formula is not None:
            s_fbc.setChemicalFormula(cpd.formula_to_string())  # str

        # database links
        _add_identifier_annotation(element=cpd, sbml_element=specie, db_to_resource=db_to_resource)

        # SBO
        specie.setSBOTerm("SBO:0000247")  # general metabolite


def export_genes(model: "Model", sbml_model: libsbml.Model) -> None:
    db_to_resource = {
        # "AGROCYC": None,
        # "ANTHRACYC": None,
        # "ARAPORT": None,
        "ARRAYEXPRESS": "arrayexpress",
        "ASAP": "asap",
        # "AUREOWIKI": None,
        # "CAULOCYC": None,
        "CGD": "cgd",
        "CGSC": "cgsc",
        # "CHLAMYCYC1": None,
        # "DBTBS-GENES": None,
        "ECHOBASE": "echobase",
        # "ECOCYC": None,
        # "ECOL199310CYC": None,
        # "ECOLIHUB": None,
        # "ECOO157CYC": None,
        "ENSEMBL": "ensembl",
        "ENSEMBLGENOMES-GN": "ensembl",
        "ENSEMBLGENOMES-TR": "ensembl",
        # "ENTREZ": None,
        # "ENZYME-DB": None,
        # "FLYBASE": None,
        # "FRANTCYC": None,
        "GENECARDS": "genecards",
        # "GI": None,
        "GO": "GO",
        "GOA": "goa",
        "GRAMENE": "gramene.gene",
        # "HPYCYC": None,
        "IMG": "img.gene",
        "INTERPRO": "interpro",
        "KEGG": "kegg.genes",
        "MAIZEGDB": "maizegdb.locus",
        "MGI": "MGI",
        "MIM": "mim",
        # "MTBCDCCYC": None,
        # "MTBRVCYC": None,
        # "MYCOBROWSER": None,
        "NCBI-GENE": "ncbigene",
        # "OU-MICROARRAY": None,
        "PDB": "pdb",
        "PHYTOZOME": "phytozome.locus",
        "PID": "pid.pathway",
        # "PYLORIGENE": None,
        "REFSEQ": "refseq",
        # "REGULONDB": None,
        # "SAVCYC": None,
        # "SCABCYC": None,
        # "SCODB": None,
        "SGD": "sgb",
        "SGN": "sgn",
        # "SHIGELLACYC": None,
        "STRING": "string",
        "SUBTILIST": "subtilist",
        "SUBTIWIKI": "subtiwiki",
        "TAIR": "tair.gene",
        # "UCSC": None,
        "UNIGENE": "unigene",
        "UNIPROT": "uniprot",
        # "VCHOCYC": None,
    }
    model_fbc: libsbml.FbcModelPlugin = sbml_model.getPlugin("fbc")
    genes: Set[str] = set()
    for reaction in model.reactions.values():
        genes.update(reaction.sequences.keys())

    for name in genes:
        gene_id = _format_name_to_sbml(name, "G_")
        gp: libsbml.GeneProduct = model_fbc.createGeneProduct()
        gp.setId(gene_id)
        gp.setLabel(gene_id)
        gp.setMetaId(f"meta_{name}")
        if (link := model._monomer_links.get(name)) is not None:
            _add_identifier_annotation(element=link, sbml_element=gp, db_to_resource=db_to_resource)

        # SBO
        gp.setSBOTerm("SBO:0000243")  # general gene


def export_objective(model: "Model", sbml_model: libsbml.Model) -> None:
    model_fbc: libsbml.FbcModelPlugin = sbml_model.getPlugin("fbc")
    objective: libsbml.Objective = model_fbc.createObjective()
    objective.setId("obj")  # str
    objective.setType("maximize")  # str
    model_fbc.setActiveObjectiveId("obj")  # str

    for rid, coef in model.objective.items():
        flux_obj: libsbml.FluxObjective = objective.createFluxObjective()
        if (
            not flux_obj.setReaction(_format_name_to_sbml(rid, "R_")) == libsbml.LIBSBML_OPERATION_SUCCESS
        ):  # str
            warnings.warn(f"Could not add reaction {rid} to objective")
        if not flux_obj.setCoefficient(float(coef)) == libsbml.LIBSBML_OPERATION_SUCCESS:  # float
            warnings.warn(f"Could not set objective coefficient for reaction {rid}")


def _create_bound_parameter(
    reaction_id: str,
    sbml_model: libsbml.Model,
    bound: float,
    lower: bool,
    r_fbc: libsbml.FbcReactionPlugin,
) -> None:
    par: libsbml.Parameter = sbml_model.createParameter()
    par.setValue(bound)  # float
    par.setConstant(True)  # bool
    par.setSBOTerm("SBO:0000625")  # str
    if lower:
        pid = f"{reaction_id}_lower"
        par.setId(pid)  # str
        r_fbc.setLowerFluxBound(pid)  # str
    else:
        pid = f"{reaction_id}_upper"
        par.setId(pid)  # str
        r_fbc.setUpperFluxBound(pid)  # str


def export_reactions(model: "Model", sbml_model: libsbml.Model) -> None:
    db_to_resource = {
        "BIGG": "bigg.reaction",
        "METANETX-RXN": "metanetx.reaction",
        "RHEA": "rhea",
        "PIR": "pirsf",
        "UNIPROT": "uniprot",
        "SEED": "seed.reaction",
        # "LIGAND": None,
        # "LIGAND-RXN": None,
    }

    for reaction in model.reactions.values():
        sbml_rxn: libsbml.Reaction = sbml_model.createReaction()
        sbml_rxn_id = _format_name_to_sbml(reaction.id, "R_")
        sbml_rxn.setId(sbml_rxn_id)  # str
        sbml_rxn.setMetaId(f"meta_{sbml_rxn_id}")  # str
        if (name := reaction.name) is not None:
            sbml_rxn.setName(name)  # str
        sbml_rxn.setFast(False)  # bool
        if (reversible := reaction.reversible) is not None:
            sbml_rxn.setReversible(reversible)  # bool
        r_fbc: libsbml.FbcReactionPlugin = sbml_rxn.getPlugin("fbc")

        # Stoichiometries
        for species, stoichiometry in reaction.stoichiometries.items():
            if stoichiometry < 0:
                sref: libsbml.SpeciesReference = sbml_rxn.createReactant()
                sref.setStoichiometry(-float(stoichiometry))  # float
            else:
                sref = sbml_rxn.createProduct()
                sref.setStoichiometry(float(stoichiometry))  # float
            sref.setSpecies(_format_name_to_sbml(species, "M_"))  # str
            sref.setConstant(True)  # bool

        # Bounds
        if (bounds := reaction.bounds) is not None:
            _create_bound_parameter(
                reaction_id=sbml_rxn_id,
                sbml_model=sbml_model,
                r_fbc=r_fbc,
                bound=bounds[0],
                lower=True,
            )
            _create_bound_parameter(
                reaction_id=sbml_rxn_id,
                sbml_model=sbml_model,
                r_fbc=r_fbc,
                bound=bounds[1],
                lower=False,
            )

        # GPR
        for genes in reaction.monomers.values():
            gpr = " ".join([_format_name_to_sbml(name, "G_") for name in genes if name in reaction.monomers])
            gpa: libsbml.GeneProductAssociation = r_fbc.createGeneProductAssociation()
            gpa.setAssociation(gpr, True, False)

        # Database Links
        _add_identifier_annotation(element=reaction, sbml_element=sbml_rxn, db_to_resource=db_to_resource)

        # SBO
        if reaction.transmembrane:
            sbml_rxn.setSBOTerm("SBO:0000185")  # transport reaction
        elif reaction.id.startswith("EX_"):
            sbml_rxn.setSBOTerm("SBO:0000627")  # exchange reaction
        else:
            sbml_rxn.setSBOTerm("SBO:0000176")  # general reaction


def export_model(model: "Model") -> libsbml.SBMLDocument:
    sbml_ns = libsbml.SBMLNamespaces(3, 1)  # SBML L3V1
    sbml_ns.addPackageNamespace("fbc", 2)  # fbc-v2

    doc: libsbml.SBMLDocument = libsbml.SBMLDocument(sbml_ns)
    doc.setPackageRequired("fbc", False)
    doc.setSBOTerm("SBO:0000624")

    sbml_model: libsbml.Model = doc.createModel()
    model_fbc: libsbml.FbcModelPlugin = sbml_model.getPlugin("fbc")
    model_fbc.setStrict(True)  # bool

    export_model_name(model, sbml_model)
    # export_model_annotations(model, sbml_model)
    # export_model_notes(model, sbml_model)
    # export_model_meta_data(model, sbml_model)
    export_units(model, sbml_model)
    export_compartments(model, sbml_model)
    export_compounds(model, sbml_model)
    export_genes(model, sbml_model)
    export_reactions(model, sbml_model)
    export_objective(model, sbml_model)
    return doc
