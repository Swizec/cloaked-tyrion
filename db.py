
from pony.orm import *

db = Database('sqlite', 'db.sqlite', create_db=True)
MAX_LENGTH=6000

# since all our fields have the same properties anyway we can just make them
# with a function, wish I started using this earlier"
def make_model(parent, id, fields):
    def inner(future_class_name, future_class_parents, future_class_attr):
        for name in fields:
            future_class_attr[name.upper()] = Optional(unicode, MAX_LENGTH)

        name, table = parent
        future_class_attr[name] = Required(table)
        future_class_attr[id] = PrimaryKey(int, auto=True)

        return type(future_class_name, future_class_parents, future_class_attr)

    return inner

def make_ref(parent, id):
    return make_model(parent, id,
                      ["reference_type", "reference_author", "reference_year",
                       "reference_title", "reference_source"])


class Substance(db.Entity):
    DOSSIER_ID = PrimaryKey(unicode)
    CAS = Optional(unicode)
    EC = Optional(unicode)
    PNECS = Set("ECHA_ECOTOX_PNEC")
    TOXICITIES = Set("ECHA_ECOTOX_TOX_ADM")
    DNELS = Set("ECHA_TOX_DNEL")
    TOXIKINETICSES = Set("ECHA_TOX_BTK_ADM")
    DERMALS = Set("ECHA_TOX_DA_ADM")
    ACUTES = Set("ECHA_TOX_ACUTE_ADM")
    ICS = Set("ECHA_TOX_IC_ADM")
    #SENSS = Set("ECHA_TOX_SENS_ADM")


class ECHA_ECOTOX_PNEC(db.Entity):
    SUBST_ID = Required(Substance)
    PNEC_ID = PrimaryKey(int, auto=True)
    SOURCE = Optional(unicode, MAX_LENGTH)
    COMPARTMENT = Optional(unicode, MAX_LENGTH)
    TARGET = Optional(unicode, MAX_LENGTH)
    HAC = Optional(unicode, MAX_LENGTH)
    VALUE = Optional(unicode, MAX_LENGTH)
    ASS_FAC = Optional(unicode, MAX_LENGTH)
    EXTR_METH = Optional(unicode, MAX_LENGTH)

class ECHA_ECOTOX_TOX_ADM(db.Entity):
    SUBST_ID = Required(Substance)
    TOX_ID = PrimaryKey(int, auto=True)
    TOX_TYPE = Required(unicode) # AQUATIC, TERRESTRIAL, SEDIMENT
    ESR = Optional(unicode, MAX_LENGTH)
    RELIABILITY = Optional(unicode, MAX_LENGTH)
    GUIDELINE = Optional(unicode, MAX_LENGTH)
    QUALIFIER = Optional(unicode, MAX_LENGTH)
    GLP = Optional(unicode, MAX_LENGTH)
    ORGANISM = Optional(unicode, MAX_LENGTH*3)
    TESTMAT_INDICATOR = Optional(unicode, MAX_LENGTH)
    REFS = Set("ECHA_ECOTOX_TOX_REF")
    DATAS = Set("ECHA_ECOTOX_TOX_DATA")

class ECHA_ECOTOX_TOX_REF(db.Entity):
    TOX_ID = Required(ECHA_ECOTOX_TOX_ADM)
    TOX_REF_ID = PrimaryKey(int, auto=True)
    REFERENCE_TYPE = Optional(unicode, MAX_LENGTH)
    REFERENCE_AUTHOR = Optional(unicode, MAX_LENGTH)
    REFERENCE_YEAR = Optional(unicode, MAX_LENGTH)
    REFERENCE_TITLE = Optional(unicode, MAX_LENGTH)
    REFERENCE_SOURCE = Optional(unicode, MAX_LENGTH)

class ECHA_ECOTOX_TOX_DATA(db.Entity):
    TOX_ID = Required(ECHA_ECOTOX_TOX_ADM)
    TOX_DATA_ID = PrimaryKey(int, auto=True)
    ORGANISM = Optional(unicode, MAX_LENGTH*3)
    EXP_DURATION_VALUE = Optional(unicode, MAX_LENGTH)
    ENDPOINT = Optional(unicode, MAX_LENGTH)
    EFF_CONC = Optional(unicode, MAX_LENGTH)
    BASIS_CONC = Optional(unicode, MAX_LENGTH)
    EFF_CONC_TYPE = Optional(unicode, MAX_LENGTH)
    BASIS_EFFECT = Optional(unicode, MAX_LENGTH)
    REMARKS = Optional(unicode, MAX_LENGTH)


class ECHA_TOX_DNEL(db.Entity):
    SUBST_ID = Required(Substance)
    DNEL_ID = PrimaryKey(int, auto=True)
    SOURCE = Optional(unicode, MAX_LENGTH)
    TARGET = Optional(unicode, MAX_LENGTH)
    EFFECTS = Optional(unicode, MAX_LENGTH)
    EXPOSURE = Optional(unicode, MAX_LENGTH)
    HAC = Optional(unicode, MAX_LENGTH)
    VALUE = Optional(unicode, MAX_LENGTH)
    SENS_ENDP = Optional(unicode, MAX_LENGTH)
    ROUTE = Optional(unicode, MAX_LENGTH)


class ECHA_TOX_BTK_ADM(db.Entity):
    __metaclass__ = make_model(("SUBST_ID", Substance), "TOX_BTK_ID",
                               ["esr", "reliability", "type_invivo_invitro",
                                "study_objective", "glp", "testmat_indicator"])

    GUIDELINES = Set("ECHA_TOX_BTK_GUIDELINES")
    REFS = Set("ECHA_TOX_BTK_REF")
    DATAS = Set("ECHA_TOX_BTK_DATA")

class ECHA_TOX_BTK_GUIDELINES(db.Entity):
    __metaclass__ = make_model(("TOX_BTK_ID", ECHA_TOX_BTK_ADM), "TOX_BTK_GL_ID",
                               ["guideline", "qualifier"])


class ECHA_TOX_BTK_REF(db.Entity):
    __metaclass__ = make_ref(("TOX_BTK_ID", ECHA_TOX_BTK_ADM), "TOX_BTK_REF_ID")

class ECHA_TOX_BTK_DATA(db.Entity):
    __metaclass__ = make_model(("TOX_BTK_ID", ECHA_TOX_BTK_ADM), "TOX_BTK_DATA_ID",
                               ["organism", "sex", "route", "vehicle_tox", "exp_period",
                                "doses_concetrations", "metabolites", "interpret_rs_submitter"])

class ECHA_TOX_DA_ADM(db.Entity):
    __metaclass__ = make_model(("SUBST_ID", Substance), "TOX_DA_ID",
                               ["esr", "reliability", "type_invivo_invitro", "glp",
                                "testmat_indicator", "organism", "sex", "exp_period",
                                "vehicle_tox", "doses_concentrations",
                                "signs_symptoms_toxicity", "dermal_irritation"])

    GUIDELINES = Set("ECHA_TOX_DA_GUIDELINES")
    REFS = Set("ECHA_TOX_DA_REF")
    DATAS = Set("ECHA_TOX_DA_DATA")

class ECHA_TOX_DA_GUIDELINES(db.Entity):
    __metaclass__ = make_model(("TOX_DA_ID", ECHA_TOX_DA_ADM), "TOX_DA_GL_ID",
                                ["guideline", "qualifier"])

class ECHA_TOX_DA_REF(db.Entity):
    __metaclass__ = make_ref(("TOX_DA_ID", ECHA_TOX_DA_ADM), "TOX_DA_REF_ID")

class ECHA_TOX_DA_DATA(db.Entity):
    __metaclass__ = make_model(("TOX_DA_ID", ECHA_TOX_DA_ADM), "TOX_DA_DATA_ID",
                               ["timepoint", "dose", "loqualifier", "remarks"])

class ECHA_TOX_ACUTE_ADM(db.Entity):
    __metaclass__ = make_model(("SUBST_ID", Substance), "TOX_ACUTE_ID",
                               ["esr", "reliability", "test_type", "glp",
                                "testmat_indicator", "organism", "sex", "route",
                                "vehicle_tox", "exp_period_txt",
                                "interpret_rs_submitter"])

    GUIDELINES = Set("ECHA_TOX_ACUTE_GUIDELINES")
    REFS = Set("ECHA_TOX_ACUTE_REF")
    DATAS = Set("ECHA_TOX_ACUTE_DATA")

class ECHA_TOX_ACUTE_GUIDELINES(db.Entity):
    __metaclass__ = make_model(("TOX_ACUTE_ID", ECHA_TOX_ACUTE_ADM), "TOX_ACUTE_GL_ID",
                               ["guideline", "qualifier"])

class ECHA_TOX_ACUTE_REF(db.Entity):
    __metaclass__ = make_ref(("TOX_ACUTE_ID", ECHA_TOX_ACUTE_ADM), "TOX_ACUTE_REF_ID")

class ECHA_TOX_ACUTE_DATA(db.Entity):
    __metaclass__ = make_model(("TOX_ACUTE_ID", ECHA_TOX_ACUTE_ADM), "TOX_ACUTE_DATA_ID",
                               ["sex", "endpoint", "loqualifier", "exp_period_value",
                                "conf_limits_loqualifier", "remarks"])

class ECHA_TOX_IC_ADM(db.Entity):
    __metaclass__ = make_model(("SUBST_ID", Substance), "TOX_IC_ID",
                               ["esr", "reliability", "type_invivo_invitro", "glp",
                                "testmat_indicator", "organism", "sex", "exp_period",
                                "observ_period", "vehicle_tox", "interpret_rs_submitter",
                                "criteria_submitter", "response_data"])

    GUIDELINES = Set("ECHA_TOX_IC_GUIDELINES")
    REFS = Set("ECHA_TOX_IC_REF")
    DATAS = Set("ECHA_TOX_IC_DATA")

class ECHA_TOX_IC_GUIDELINES(db.Entity):
    __metaclass__ = make_model(("TOX_IC_ID", ECHA_TOX_IC_ADM), "TOX_IC_GL_ID",
                               ["guideline", "qualifier"])

class ECHA_TOX_IC_REF(db.Entity):
    __metaclass__ = make_ref(("TOX_IC_ID", ECHA_TOX_IC_ADM), "TOX_IC_REF_ID")

class ECHA_TOX_IC_DATA(db.Entity):
    __metaclass__ = make_model(("TOX_IC_ID", ECHA_TOX_IC_ADM), "TOX_IC_DATA_ID",
                               ["parameter", "basis", "timepoint", "score_loqualifier",
                                "scale", "reversibility", "remarks"])

# class ECHA_TOX_SENS_ADM(db.Entity):
#     __metaclass__ = make_model(("SUBST_ID", Substance), "TOX_SENS_ID",
#                                [])

#     GUIDELINES = Set("ECHA_TOX_SENS_GUIDELINE")
#     REFS = Set("ECHA_TOX_SENS_REF")
#     DATAS = Set("ECHA_TOX_SENS_DATA")


db.generate_mapping(create_tables=True)



def find_or_create(model, **kwargs):
    obj = model.get(**kwargs)
    if obj == None:
        obj = model(**kwargs)

    return obj
