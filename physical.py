
import glob, logging
from slugify import slugify

from helpers import *
from db import *


def parse(substance, path):
    def step(d, data, file):
        adm = save_data(data, ECHA_PHYSCHEM_ADM,
                        [("SUBST_ID", substance),
                         ("esr", get_esr(d))],
                        make_fields([("reliability", ".reliability:first"),
                                      ("glp", ".GLP_COMPLIANCE_STATEMENT"),
                                      ("org_solvents_stability", ".STABLE"),
                                      ("org_solvents_degrad",
                                       ".DEGRAD_PRODUCTS_INDICATOR"),
                                      ("datawaiving", ".dataWaiving")],
                                    ["method_type",
                                     "partcoeff_type",
                                     "testtype",
                                     "testmat_indicator",
                                     "interpretation_results",
                                     "dissociation_indicator",
                                     "distribution_type"]))
        adm = adm[0]

        save_guidelines(data, ECHA_PHYSCHEM_GUIDELINES,
                        ("PHYSCHEM_ID", adm))

        save_refs(data, ECHA_PHYSCHEM_REF,
                  ("PHYSCHEM_ID", adm))

        if key(file):
            parser(key(file), adm)(data)

    parse_files(path,
                ["physical and chemical properties", "SSS", "SSS"],
                step)

def key(file):
    candidate = [k for k in ["appearance", "melting point", "boiling point", "density",
                             "vapour pressure", "partition coefficient",
                             "water solubility", "surface tension", "flash point",
                             "auto flammability", "flammability",
                             "oxidising properties", "stability in organic solvents",
                             "dissociation constant", "ph", "viscosity",
                             "particle size distribution",
                             "solubility in organic solvents"]
                 if "__%s" % slugify(k) in file]

    return candidate[0] if candidate else None

def parser(key, adm):
    return {
        "appearance": lambda data: save_data(
            data.find("#GEN_RESULTS_HD"), ECHA_PHYSCHEM_APPEARANCE,
            ("PHYSCHEM_ID", adm),
            make_fields([("physical_state", ".SUBSTANCE_PHYSICAL_STATE"),
                         ("colour", ".SUBSTANCE_COLOUR"),
                         ("type", ".SUBSTANCE_TYPE")],
                        ["form", "odour"])),

        "melting point": lambda data: save_data(
            data.find("#GEN_RESULTS_HD .MELTINGPT"), ECHA_PHYSCHEM_MELTING,
            ("PHYSCHEM_ID", adm),
            make_fields([("pressure", ".PRESSURE_LOQUALIFIER")],
                        ["loqualifier", "decomp_indicator",
                         "sublimation_indicator"])),

        "boiling point": lambda data: save_data(
            data.find("#GEN_RESULTS_HD .BOILINGPT"), ECHA_PHYSCHEM_BOILING,
            ("PHYSCHEM_ID", adm),
            make_fields([("pressure", ".PRESSURE_LOQUALIFIER")],
                        ["loqualifier", "decomp_indicator",
                         "sublimation_indicator"])),

        "density": lambda data: save_data(
            data.find("#GEN_RESULTS_HD .DENSITY"), ECHA_PHYSCHEM_DENSITY,
            ("PHYSCHEM_ID", adm),
            make_fields([],
                        ["type", "loqualifier", "temp_value"])),

        "vapour pressure": lambda data: save_data(
            data.find("#GEN_RESULTS_HD .VAPOURPR"), ECHA_PHYSCHEM_VPRESSURE,
            ("PHYSCHEM_ID", adm),
            make_fields([],
                        ["loqualifier", "temp_value", "pressure_loqualifier"])),

        "partition coefficient": lambda data: save_data(
            data.find("#GEN_RESULTS_HD .PARTCOEFF"), ECHA_PHYSCHEM_PARTC,
            ("PHYSCHEM_ID", adm),
            make_fields([],
                        ["type", "loqualifier", "temp_value", "ph_loqualifier"])),

        "water solubility": lambda data: save_data(
            data.find("#GEN_RESULTS_HD .WATERSOL"), ECHA_PHYSCHEM_WSOLUBILITY,
            ("PHYSCHEM_ID", adm),
            make_fields([],
                        ["loqualifier", "temp_value", "ph_loqualifier"])),

        "surface tension": lambda data: save_data(
            data.find("#GEN_RESULTS_HD .TENSION"), ECHA_PHYSCHEM_STENSION,
            ("PHYSCHEM_ID", adm),
            make_fields([],
                        ["loqualifier", "temp_value", "conc_value"])),

        "flash point": lambda data: save_data(
            data.find("#GEN_RESULTS_HD .FLASHPT"), ECHA_PHYSCHEM_FPOINT,
            ("PHYSCHEM_ID", adm),
            make_fields([],
                        ["loqualifier", "press_loqualifier"])),

        "auto flammability": lambda data: save_data(
            data.find("#GEN_RESULTS_HD .AUTOFLAM"), ECHA_PHYSCHEM_AUTOFLAM,
            ("PHYSCHEM_ID", adm),
            make_fields([],
                        ["loqualifier", "press_loqualifier"])),

        "flammability": lambda data: save_data(
            data.find("#GEN_RESULTS_HD"), ECHA_PHYSCHEM_FLAMMABILITY,
            ("PHYSCHEM_ID", adm),
            make_fields([("interpret_results_subm", ".INTERPRET_RESULTS_SUBM"),
                         ("pyrophoric_ignition_contact", ".PYROPHORIC_PROPERTIES .IGNITION_CONTACT"),
                         ("pyrophoric_rem", ".PYROPHORIC_PROPERTIES .REM"),
                         ("loexplos_limit", ".LOEXPLOS_LIMIT .LOQUALIFIER"),
                         ("loexplos_rem", ".LOEXPLOS_LIMIT .REM"),
                         ("upexplos_limit", ".UPEXPLOS_LIMIT .LOQUALIFIER"),
                         ("upexplos_rem", ".UPEXPLOS_LIMIT .REM")],
                        [])),

        "oxidising properties": lambda data: save_data(
            data.find("#GEN_RESULTS_HD .RESULT"), ECHA_PHYSCHEM_OXIDIZING_PROP,
            ("PHYSCHEM_ID", adm),
            make_fields([("remarks", ".REM")],
                        ["parameter", "loqualifier"])),

        "stability in organic solvents": lambda data: save_data(
            data.find("#GEN_RESULTS_HD .STABLE"), ECHA_PHYSCHEM_ORG_SOL_DEGRADATION,
            ("PHYSCHEM_ID", adm),
            make_fields([("identity", ".ID")],
                        ["no", "identifier"])),

        "dissociation constant": lambda data: save_data(
            data.find("#GEN_RESULTS_HD .PKA"), ECHA_PHYSCHEM_DISSCO,
            ("PHYSCHEM_ID", adm),
            make_fields([("remarks", ".REM")],
                        ["no", "value_loqualifier", "temp_value"])),

        "ph": lambda data: save_data(
            data.find("#GEN_RESULTS_HD"), ECHA_PHYSCHEM_PH,
            ("PHYSCHEM_ID", adm),
            make_fields([("remarks", ".REM")],
                        ["loqualifier", "temp_value", "conc_loqualifier"])),

        "viscosity": lambda data: save_data(
            data.find("#GEN_RESULTS_HD .VISCOS"), ECHA_PHYSCHEM_VISCOSITY,
            ("PHYSCHEM_ID", adm),
            make_fields([("remarks", ".REM")],
                        ["loqualifier", "temp_value"])),

        "particle size distribution": lambda data: granulometry(data, adm),

        "solubility in organic solvents": lambda data: save_data(
            data.find("#GEN_RESULTS_HD .FATSOL"), ECHA_PHYSCHEM_FATSOL,
            ("PHYSCHEM_ID", adm),
            make_fields([], ["organic_medium", "loqualifier", "temp_value"]))
    }[key]


def granulometry(data, adm):
    save_data(
        data.find(".set.DIAMETER"),
        ECHA_PHYSCHEM_GRANULOMETRY_MMD,
        ("PHYSCHEM_ID", adm),
        make_fields([("remarks", ".REM")],
                    ["loqualifier"])),

    save_data(
        data.find(".set.PARTICLESIZE"),
        ECHA_PHYSCHEM_GRANULOMETRY_PS,
        ("PHYSCHEM_ID", adm),
        make_fields([("remarks", ".REM")],
                    ["percentile", "loqualifier"])),

    save_data(
        data.find(".set.DISTRIBUTION"),
        ECHA_PHYSCHEM_GRANULOMETRY_DIST,
        ("PHYSCHEM_ID", adm),
        make_fields([("remarks", ".REM"),
                     ("dist_loqualifier", ".DIST_LOQUALIFIER")],
                    ["size_loqualifier", "loqualifier"]))
