import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Iterable, Union

import libsbml

if TYPE_CHECKING:
    from .. import Compound, Model, Reaction


@dataclass
class Unit:
    kind: libsbml.UnitDefinition
    scale: int
    multiplier: int
    exponent: int


@dataclass
class UnitDefinition:
    name: str
    units: Iterable[Unit]


def export_model_name(model: "Model", sbml_model: libsbml.Model) -> None:
    if model.name is not None:
        sbml_model.setId(model.name)
        sbml_model.setMetaId(f"meta_{model.name}")
        sbml_model.setName(model.name)
    else:
        sbml_model.setMetaId("meta_model")


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
            Unit(kind=libsbml.UNIT_KIND_MOLE, scale=-3, multiplier=1, exponent=1),
            Unit(kind=libsbml.UNIT_KIND_GRAM, scale=0, multiplier=1, exponent=-1),
            Unit(kind=libsbml.UNIT_KIND_SECOND, scale=0, multiplier=3600, exponent=-1),
        ],
    )

    flux_udef: libsbml.UnitDefinition = sbml_model.createUnitDefinition()
    flux_udef.setId(default.name)
    for u in default.units:
        unit: libsbml.Unit = flux_udef.createUnit()
        unit.setKind(u.kind)
        unit.setExponent(u.exponent)
        unit.setScale(u.scale)
        unit.setMultiplier(u.multiplier)


def export_compartments(model: "Model", sbml_model: libsbml.Model) -> None:
    for name, suffix in model.compartments.items():
        compartment: libsbml.Compartment = sbml_model.createCompartment()

        if compartment.setId(suffix) != libsbml.LIBSBML_OPERATION_SUCCESS:
            warnings.warn(f"Could not set compartment id {suffix}")

        if compartment.setName(name) != libsbml.LIBSBML_OPERATION_SUCCESS:
            warnings.warn(f"Could not set compartment name {name}")

        compartment.setConstant(True)


def _add_identifier_annotation(
    element: Union["Compound", "Reaction"],
    sbml_element: Union[libsbml.Species, libsbml.Reaction],
    db_to_resource: Dict[str, str],
) -> None:
    for db, data in element.database_links.items():
        if (resource := db_to_resource.get(db)) is not None:
            for item in data:
                cv: libsbml.CVTerm = libsbml.CVTerm()
                cv.setQualifierType(libsbml.BIOLOGICAL_QUALIFIER)
                cv.setBiologicalQualifierType(libsbml.BQB_IS)
                cv.addResource(f"https://identifiers.org/{resource}:{item}")
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
        specie.setId(cpd.id)
        specie.setMetaId(f"meta_{cpd.id}")  # needed for annotations
        if (name := cpd.name) is not None:
            specie.setName(name)
        specie.setConstant(False)
        specie.setBoundaryCondition(False)
        specie.setHasOnlySubstanceUnits(False)
        specie.setCompartment(model.compartments[cpd.compartment])

        s_fbc: libsbml.FbcSpeciesPlugin = specie.getPlugin("fbc")
        if cpd.charge is not None:
            s_fbc.setCharge(cpd.charge)
        if cpd.formula is not None:
            s_fbc.setChemicalFormula(cpd.formula_to_string())

        _add_identifier_annotation(element=cpd, sbml_element=specie, db_to_resource=db_to_resource)


def export_genes(model: "Model", sbml_model: libsbml.Model) -> None:
    raise NotImplementedError


def export_objective(model: "Model", sbml_model: libsbml.Model) -> None:
    model_fbc: libsbml.FbcModelPlugin = sbml_model.getPlugin("fbc")
    objective: libsbml.Objective = model_fbc.createObjective()
    objective.setId("obj")
    objective.setType("maximize")
    model_fbc.setActiveObjectiveId("obj")

    for rid, coef in model.objective.items():
        flux_obj: libsbml.FluxObjective = objective.createFluxObjective()
        flux_obj.setReaction(rid)
        flux_obj.setCoefficient(coef)


def _create_bound_parameter(
    reaction_id: str,
    sbml_model: libsbml.Model,
    bound: float,
    lower: bool,
    r_fbc: libsbml.FbcReactionPlugin,
) -> None:
    par: libsbml.Parameter = sbml_model.createParameter()
    par.setValue(bound)
    par.setConstant(True)
    par.setSBOTerm("SBO:0000625")
    if lower:
        pid = f"{reaction_id}_lower"
        par.setId(pid)
        r_fbc.setLowerFluxBound(pid)
    else:
        pid = f"{reaction_id}_upper"
        par.setId(pid)
        r_fbc.setUpperFluxBound(pid)


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
        sbml_rxn.setId(reaction.id)
        sbml_rxn.setMetaId(f"meta_{reaction.id}")
        if (name := reaction.name) is not None:
            sbml_rxn.setName(name)
        sbml_rxn.setFast(False)
        if (reversible := reaction.reversible) is not None:
            sbml_rxn.setReversible(reversible)

        # Stoichiometries
        for species, stoichiometry in reaction.stoichiometries.items():
            if stoichiometry < 0:
                sref: libsbml.SpeciesReference = sbml_rxn.createReactant()
                sref.setStoichiometry(-stoichiometry)
            else:
                sref = sbml_rxn.createProduct()
                sref.setStoichiometry(stoichiometry)
            sref.setSpecies(species)
            sref.setConstant(True)

        # Bounds
        if (bounds := reaction.bounds) is not None:
            r_fbc: libsbml.FbcReactionPlugin = sbml_rxn.getPlugin("fbc")
            _create_bound_parameter(
                reaction_id=reaction.id, sbml_model=sbml_model, r_fbc=r_fbc, bound=bounds[0], lower=True
            )
            _create_bound_parameter(
                reaction_id=reaction.id, sbml_model=sbml_model, r_fbc=r_fbc, bound=bounds[1], lower=False
            )

        _add_identifier_annotation(element=reaction, sbml_element=sbml_rxn, db_to_resource=db_to_resource)


def export_model(model: "Model") -> libsbml.SBMLDocument:
    sbml_ns = libsbml.SBMLNamespaces(3, 1)  # SBML L3V1
    sbml_ns.addPackageNamespace("fbc", 2)  # fbc-v2

    doc: libsbml.SBMLDocument = libsbml.SBMLDocument(sbml_ns)
    doc.setPackageRequired("fbc", False)
    doc.setSBOTerm("SBO:0000624")

    sbml_model: libsbml.Model = doc.createModel()
    model_fbc: libsbml.FbcModelPlugin = sbml_model.getPlugin("fbc")
    model_fbc.setStrict(True)

    export_model_name(model, sbml_model)
    # export_model_annotations(model, sbml_model)
    # export_model_notes(model, sbml_model)
    # export_model_meta_data(model, sbml_model)
    export_units(model, sbml_model)
    export_compartments(model, sbml_model)
    export_compounds(model, sbml_model)
    # export_genes(model, sbml_model)
    export_reactions(model, sbml_model)
    export_objective(model, sbml_model)
    return doc
