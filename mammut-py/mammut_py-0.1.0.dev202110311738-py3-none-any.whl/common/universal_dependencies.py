# coding=utf-8

from collections import *
import itertools

spanish_venezuela_code = 'sp-ve'
base_free_morpheme_type = 'Base-Free'

lexical_def_type = 'Lexical'
limited_def_type = 'Limited'
definition_types = [lexical_def_type, limited_def_type]

verb_pos_tag = 'VERB'
noun_pos_tag = 'NOUN'
propn_pos_tag = 'PROPN'
adj_pos_tag = 'ADJ'
adv_pos_tag = 'ADV'
intj_pos_tag = 'INTJ'
det_pos_tag = 'DET'
adp_pos_tag = 'ADP'
cconj_pos_tag = 'CCONJ'
sconj_pos_tag = 'SCONJ'
part_pos_tag = 'PART'
pron_pos_tag = 'PRON'
aux_pos_tag = 'AUX'
num_pos_tag = 'NUM'
punct_pos_tag = 'PUNCT'
sym_pos_tag = 'SYM'
x_pos_tag = 'X'
pos_tags = [verb_pos_tag,noun_pos_tag,propn_pos_tag,adj_pos_tag,adv_pos_tag,intj_pos_tag,det_pos_tag,adp_pos_tag,cconj_pos_tag,
            sconj_pos_tag,part_pos_tag,pron_pos_tag,aux_pos_tag,num_pos_tag,punct_pos_tag,sym_pos_tag,x_pos_tag]
pos_tags_description_sites = {}
pos_tags_description_sites[verb_pos_tag] = 'http://universaldependencies.org/u/pos/VERB.html'
pos_tags_description_sites[noun_pos_tag] = 'http://universaldependencies.org/u/pos/NOUN.html'
pos_tags_description_sites[propn_pos_tag] = 'http://universaldependencies.org/u/pos/PROPN.html'
pos_tags_description_sites[adj_pos_tag] = 'http://universaldependencies.org/u/pos/ADJ.html'
pos_tags_description_sites[adv_pos_tag] = 'http://universaldependencies.org/u/pos/ADV.html'
pos_tags_description_sites[intj_pos_tag] = 'http://universaldependencies.org/u/pos/INTJ.html'
pos_tags_description_sites[det_pos_tag] = 'http://universaldependencies.org/u/pos/DET.html'
pos_tags_description_sites[adp_pos_tag] = 'http://universaldependencies.org/u/pos/ADP.html'
pos_tags_description_sites[cconj_pos_tag] = 'http://universaldependencies.org/u/pos/CCONJ.html'
pos_tags_description_sites[sconj_pos_tag] = 'http://universaldependencies.org/u/pos/SCONJ.html'
pos_tags_description_sites[part_pos_tag] = 'http://universaldependencies.org/u/pos/PART.html'
pos_tags_description_sites[pron_pos_tag] = 'http://universaldependencies.org/u/pos/PRON.html'
pos_tags_description_sites[aux_pos_tag] = 'http://universaldependencies.org/u/pos/AUX_.html'
pos_tags_description_sites[num_pos_tag] = 'http://universaldependencies.org/u/pos/NUM.html'
pos_tags_description_sites[punct_pos_tag] = 'http://universaldependencies.org/u/pos/PUNCT.html'
pos_tags_description_sites[sym_pos_tag] = 'http://universaldependencies.org/u/pos/SYM.html'
pos_tags_description_sites[x_pos_tag] = 'http://universaldependencies.org/u/pos/X.html'
pos_tags_stats_sites_es = {}
pos_tags_stats_sites_es[verb_pos_tag] = 'http://universaldependencies.org/es/pos/VERB.html'
pos_tags_stats_sites_es[noun_pos_tag] = 'http://universaldependencies.org/es/pos/NOUN.html'
pos_tags_stats_sites_es[propn_pos_tag] = 'http://universaldependencies.org/es/pos/PROPN.html'
pos_tags_stats_sites_es[adj_pos_tag] = 'http://universaldependencies.org/es/pos/ADJ.html'
pos_tags_stats_sites_es[adv_pos_tag] = 'http://universaldependencies.org/es/pos/ADV.html'
pos_tags_stats_sites_es[intj_pos_tag] = 'http://universaldependencies.org/es/pos/INTJ.html'
pos_tags_stats_sites_es[det_pos_tag] = 'http://universaldependencies.org/es/pos/DET.html'
pos_tags_stats_sites_es[adp_pos_tag] = 'http://universaldependencies.org/es/pos/ADP.html'
pos_tags_stats_sites_es[cconj_pos_tag] = 'http://universaldependencies.org/es/pos/CONJ.html'
pos_tags_stats_sites_es[sconj_pos_tag] = 'http://universaldependencies.org/es/pos/SCONJ.html'
pos_tags_stats_sites_es[part_pos_tag] = 'http://universaldependencies.org/es/pos/PART.html'
pos_tags_stats_sites_es[pron_pos_tag] = 'http://universaldependencies.org/es/pos/PRON.html'
pos_tags_stats_sites_es[aux_pos_tag] = 'http://universaldependencies.org/es/pos/AUX_.html'
pos_tags_stats_sites_es[num_pos_tag] = 'http://universaldependencies.org/es/pos/NUM.html'
pos_tags_stats_sites_es[punct_pos_tag] = 'http://universaldependencies.org/es/pos/PUNCT.html'
pos_tags_stats_sites_es[sym_pos_tag] = 'http://universaldependencies.org/es/pos/SYM.html'
pos_tags_stats_sites_es[x_pos_tag] = 'http://universaldependencies.org/es/pos/X.html'

FeatureDescriptor = namedtuple('FeatureDescriptor', ['id', 'name', 'description', 'url_doc', 'url_stats_es', 'values'])
feature_descriptor_per_feature = {}
word_features_per_pos_tag = {}
for tag in pos_tags:
    word_features_per_pos_tag[tag] = []

feature_types_descriptor_per_id = {}

pronominal_types_descriptor = FeatureDescriptor('PronType', 'pronominal type',
                                                'applies to pronouns, pronominal adjectives (determiners), pronominal numerals (quantifiers) and pronominal adverbs.',
                                                'http://universaldependencies.org/u/feat/PronType.html', 'http://universaldependencies.org/es/feat/PronType.html',
                                                ['PronType_Prs', 'PronType_Rcp', 'PronType_Art', 'PronType_Int', 'PronType_Rel', 'PronType_Exc',
                                                 'PronType_Dem', 'PronType_Emp', 'PronType_Tot', 'PronType_Neg', 'PronType_Ind'])
for f in pronominal_types_descriptor.values:
    feature_descriptor_per_feature[f] = pronominal_types_descriptor
word_features_per_pos_tag[propn_pos_tag].append(pronominal_types_descriptor.values)
word_features_per_pos_tag[det_pos_tag].append(pronominal_types_descriptor.values)
word_features_per_pos_tag[num_pos_tag].append(pronominal_types_descriptor.values)
word_features_per_pos_tag[adv_pos_tag].append(pronominal_types_descriptor.values)
word_features_per_pos_tag[pron_pos_tag].append(pronominal_types_descriptor.values)
feature_types_descriptor_per_id[pronominal_types_descriptor.id] = pronominal_types_descriptor


numeral_types_descriptor = FeatureDescriptor('NumType', 'numeral type',
                                             'applies to [NUM: cardinal numerals], [DET: quantifiers], [ADJ: definite adjectival, e.g. ordinal numerals], [ADV: adverbial (e.g. ordinal and multiplicative) numerals, both definite and pronominal]',
                                             'http://universaldependencies.org/u/feat/NumType.html', 'http://universaldependencies.org/es/feat/NumType.html',
                                             ['NumType_Card','NumType_Dist','NumType_Frac','NumType_Mult','NumType_Ord','NumType_Range',
                                              'NumType_Sets'])
for f in numeral_types_descriptor.values:
    feature_descriptor_per_feature[f] = numeral_types_descriptor
word_features_per_pos_tag[num_pos_tag].append(numeral_types_descriptor.values)
word_features_per_pos_tag[det_pos_tag].append(numeral_types_descriptor.values)
word_features_per_pos_tag[adj_pos_tag].append(numeral_types_descriptor.values)
word_features_per_pos_tag[adv_pos_tag].append(numeral_types_descriptor.values)
word_features_per_pos_tag[pron_pos_tag].append(numeral_types_descriptor.values)
feature_types_descriptor_per_id[numeral_types_descriptor.id] = numeral_types_descriptor


possessives_descriptor = FeatureDescriptor('Poss', 'possessive',
                                           'Boolean feature of pronouns, determiners or adjectives. It tells whether the word is possessive.',
                                           'http://universaldependencies.org/u/feat/Poss.html', 'http://universaldependencies.org/es/feat/Poss.html',
                                           ['Poss_Yes'])
for f in possessives_descriptor.values:
    feature_descriptor_per_feature[f] = possessives_descriptor
word_features_per_pos_tag[pron_pos_tag].append(possessives_descriptor.values)
word_features_per_pos_tag[det_pos_tag].append(possessives_descriptor.values)
word_features_per_pos_tag[adj_pos_tag].append(possessives_descriptor.values)
feature_types_descriptor_per_id[possessives_descriptor.id] = possessives_descriptor


reflexives_descriptor = FeatureDescriptor('Reflex', 'reflexive',
                                          'Boolean feature, typically of pronouns or determiners. It tells whether the word is reflexive, i.e. refers to the subject of its clause.',
                                          'http://universaldependencies.org/u/feat/Reflex.html', 'http://universaldependencies.org/es/feat/Reflex.html',
                                          ['Reflex_Yes'])
for f in reflexives_descriptor.values:
    feature_descriptor_per_feature[f] = reflexives_descriptor
word_features_per_pos_tag[pron_pos_tag].append(reflexives_descriptor.values)
word_features_per_pos_tag[det_pos_tag].append(reflexives_descriptor.values)
feature_types_descriptor_per_id[reflexives_descriptor.id] = reflexives_descriptor


foreigns_descriptor = FeatureDescriptor('Foreign', 'foreign word',
                                 'Boolean feature. Is this a foreign word? Not a loan word and not a foreign name but a genuinely foreign word appearing inside native text, e.g. inside direct speech, titles of books etc. This feature would apply either to the X part of speech (unanalyzable token), or to other parts of speech',
                                 'http://universaldependencies.org/u/feat/Foreign.html', 'http://universaldependencies.org/es/feat/Foreign.html',
                                 ['Foreign_Yes'])
for f in foreigns_descriptor.values:
    feature_descriptor_per_feature[f] = foreigns_descriptor
word_features_per_pos_tag[x_pos_tag].append(foreigns_descriptor.values)
word_features_per_pos_tag[noun_pos_tag].append(foreigns_descriptor.values)
word_features_per_pos_tag[verb_pos_tag].append(foreigns_descriptor.values)
word_features_per_pos_tag[propn_pos_tag].append(foreigns_descriptor.values)
word_features_per_pos_tag[adj_pos_tag].append(foreigns_descriptor.values)
word_features_per_pos_tag[adv_pos_tag].append(foreigns_descriptor.values)
feature_types_descriptor_per_id[foreigns_descriptor.id] = foreigns_descriptor


abbreviations_descriptor = FeatureDescriptor('Abbr', 'abbreviation word',
                                 'Boolean feature. Is this an abbreviation? Note that the abbreviated word(s) typically belongs to a part of speech other than X.',
                                 'http://universaldependencies.org/u/feat/Abbr.html', 'http://universaldependencies.org/u/feat/Abbr.html',
                                 ['Abbr_Yes'])
for f in abbreviations_descriptor.values:
    feature_descriptor_per_feature[f] = abbreviations_descriptor
word_features_per_pos_tag[x_pos_tag].append(abbreviations_descriptor.values)
feature_types_descriptor_per_id[abbreviations_descriptor.id] = abbreviations_descriptor


genders_descriptor = FeatureDescriptor('Gender', 'gender',
                                 'Gender is usually a lexical feature of nouns and inflectional feature of other parts of speech (pronouns, adjectives, determiners, numerals, verbs) that mark agreement with nouns. ',
                                 'http://universaldependencies.org/u/feat/Gender.html', 'http://universaldependencies.org/es/feat/Gender.html',
                                 ['Gender_Com','Gender_Fem','Gender_Masc','Gender_Neut'])
for f in genders_descriptor.values:
    feature_descriptor_per_feature[f] = genders_descriptor
word_features_per_pos_tag[noun_pos_tag].append(genders_descriptor.values)
word_features_per_pos_tag[propn_pos_tag].append(genders_descriptor.values)
word_features_per_pos_tag[adj_pos_tag].append(genders_descriptor.values)
word_features_per_pos_tag[det_pos_tag].append(genders_descriptor.values)
word_features_per_pos_tag[num_pos_tag].append(genders_descriptor.values)
word_features_per_pos_tag[verb_pos_tag].append(genders_descriptor.values)
word_features_per_pos_tag[pron_pos_tag].append(genders_descriptor.values)
word_features_per_pos_tag[aux_pos_tag].append(genders_descriptor.values)
word_features_per_pos_tag[x_pos_tag].append(genders_descriptor.values)
word_features_per_pos_tag[sym_pos_tag].append(genders_descriptor.values)
feature_types_descriptor_per_id[genders_descriptor.id] = genders_descriptor


animacys_descriptor = FeatureDescriptor('Animacy', 'animacy',
                                        'NA Spanish. Similarly to Gender (and to the African noun classes), animacy is usually a lexical feature of nouns and inflectional feature of other parts of speech (pronouns, adjectives, determiners, numerals, verbs) that mark agreement with nouns.',
                                        'http://universaldependencies.org/u/feat/Animacy.html', 'http://universaldependencies.org/es/feat/Animacy.html',
                                        ['Animacy_Anim','Animacy_Hum','Animacy_Inan','Animacy_Nhum'])
for f in animacys_descriptor.values:
    feature_descriptor_per_feature[f] = animacys_descriptor
#word_features_per_pos_tag[noun_pos_tag].append(animacys_descriptor.values)
#word_features_per_pos_tag[propn_pos_tag].append(animacys_descriptor.values)
#word_features_per_pos_tag[adj_pos_tag].append(animacys_descriptor.values)
#word_features_per_pos_tag[det_pos_tag].append(animacys_descriptor.values)
#word_features_per_pos_tag[num_pos_tag].append(animacys_descriptor.values)
#word_features_per_pos_tag[verb_pos_tag].append(animacys_descriptor.values)
feature_types_descriptor_per_id[animacys_descriptor.id] = animacys_descriptor


numbers_descriptor = FeatureDescriptor('Number', ' type',
                                       'Number is usually an inflectional feature of nouns and, depending on language, other parts of speech (pronouns, adjectives, determiners, numerals, verbs) that mark agreement with nouns.',
                                       'http://universaldependencies.org/u/feat/Number.html', 'http://universaldependencies.org/es/feat/Number.html',
                                       ['Number_Coll','Number_Count','Number_Dual','Number_Grpa','Number_Grpl','Number_Inv','Number_Pauc',
                                        'Number_Plur','Number_Ptan','Number_Sing','Number_Tri'])
for f in numbers_descriptor.values:
    feature_descriptor_per_feature[f] = numbers_descriptor
word_features_per_pos_tag[noun_pos_tag].append(numbers_descriptor.values)
word_features_per_pos_tag[propn_pos_tag].append(numbers_descriptor.values)
word_features_per_pos_tag[adj_pos_tag].append(numbers_descriptor.values)
word_features_per_pos_tag[det_pos_tag].append(numbers_descriptor.values)
word_features_per_pos_tag[num_pos_tag].append(numbers_descriptor.values)
word_features_per_pos_tag[verb_pos_tag].append(numbers_descriptor.values)
word_features_per_pos_tag[pron_pos_tag].append(numbers_descriptor.values)
word_features_per_pos_tag[aux_pos_tag].append(numbers_descriptor.values)
word_features_per_pos_tag[x_pos_tag].append(numbers_descriptor.values)
word_features_per_pos_tag[sym_pos_tag].append(numbers_descriptor.values)
feature_types_descriptor_per_id[numbers_descriptor.id] = numbers_descriptor


cases_descriptor = FeatureDescriptor('Case', 'case',
                                     'Case is usually an inflectional feature of nouns and, depending on language, other parts of speech (pronouns, adjectives, determiners, numerals, verbs) that mark agreement with nouns. In some tagsets it is also valency feature of adpositions.',
                                     'http://universaldependencies.org/u/feat/Case.html', 'http://universaldependencies.org/es/feat/Case.html',
                                     ['Case_Abs','Case_Acc','Case_Erg','Case_Nom','Case_Abe','Case_Ben','Case_Cau','Case_Cmp','Case_Com','Case_Dat',
                                      'Case_Dis','Case_Equ','Case_Gen','Case_Ins','Case_Par','Case_Tem','Case_Tra','Case_VocAbl','Case_Add',
                                      'Case_Ade','Case_All','Case_Del','Case_Ela','Case_Ess','Case_Ill','Case_Ine','Case_Lat','Case_Loc','Case_Sub',
                                      'Case_Sup','Case_Ter'])
for f in cases_descriptor.values:
    feature_descriptor_per_feature[f] = cases_descriptor
#word_features_per_pos_tag[pron_pos_tag].append(cases_descriptor.values)
#word_features_per_pos_tag[noun_pos_tag].append(cases_descriptor.values)
#word_features_per_pos_tag[propn_pos_tag].append(cases_descriptor.values)
#word_features_per_pos_tag[adj_pos_tag].append(cases_descriptor.values)
#word_features_per_pos_tag[det_pos_tag].append(cases_descriptor.values)
#word_features_per_pos_tag[num_pos_tag].append(cases_descriptor.values)
#word_features_per_pos_tag[verb_pos_tag].append(cases_descriptor.values)
feature_types_descriptor_per_id[cases_descriptor.id] = cases_descriptor


definiteness_descriptor = FeatureDescriptor('Definite', 'definiteness or state',
                                            'Definiteness is typically a feature of nouns, adjectives and articles. Its value distinguishes whether we are talking about something known and concrete, or something general or unknown.',
                                            'http://universaldependencies.org/u/feat/Definite.html', 'http://universaldependencies.org/es/feat/Definite.html',
                                            ['Definite_Com','Definite_Cons','Definite_Def','Definite_Ind','Definite_Spec'])
for f in definiteness_descriptor.values:
    feature_descriptor_per_feature[f] = definiteness_descriptor
word_features_per_pos_tag[det_pos_tag].append(definiteness_descriptor.values)
word_features_per_pos_tag[noun_pos_tag].append(definiteness_descriptor.values)
word_features_per_pos_tag[adj_pos_tag].append(definiteness_descriptor.values)
word_features_per_pos_tag[det_pos_tag].append(definiteness_descriptor.values)
feature_types_descriptor_per_id[definiteness_descriptor.id] = definiteness_descriptor


degrees_descriptor = FeatureDescriptor('Degree', 'degree of comparison',
                                       'Degree of comparison is typically an inflectional feature of some adjectives and adverbs.',
                                       'http://universaldependencies.org/u/feat/Degree.html', 'http://universaldependencies.org/es/feat/Degree.html',
                                       ['Degree_Abs','Degree_Cmp','Degree_Equ','Degree_Pos','Degree_Sup'])
for f in degrees_descriptor.values:
    feature_descriptor_per_feature[f] = degrees_descriptor
word_features_per_pos_tag[adj_pos_tag].append(degrees_descriptor.values)
word_features_per_pos_tag[adv_pos_tag].append(degrees_descriptor.values)
word_features_per_pos_tag[pron_pos_tag].append(degrees_descriptor.values)
word_features_per_pos_tag[det_pos_tag].append(degrees_descriptor.values)
feature_types_descriptor_per_id[degrees_descriptor.id] = degrees_descriptor


verb_forms_descriptor = FeatureDescriptor('VerbForm', 'form of verb or deverbative',
                                          'Even though the name of the feature seems to suggest that it is used exclusively with verbs, it is not the case. Some verb forms in some languages actually form a gray zone between verbs and other parts of speech (nouns, adjectives and adverbs).',
                                          'http://universaldependencies.org/u/feat/VerbForm.html', 'http://universaldependencies.org/es/feat/VerbForm.html',
                                          ['VerbForm_Conv','VerbForm_Fin','VerbForm_Gdv','VerbForm_Ger','VerbForm_Inf','VerbForm_Part',
                                           'VerbForm_Sup','VerbForm_Vnoun'])
for f in verb_forms_descriptor.values:
    feature_descriptor_per_feature[f] = verb_forms_descriptor
word_features_per_pos_tag[verb_pos_tag].append(verb_forms_descriptor.values)
word_features_per_pos_tag[aux_pos_tag].append(verb_forms_descriptor.values)
word_features_per_pos_tag[adj_pos_tag].append(verb_forms_descriptor.values)
word_features_per_pos_tag[noun_pos_tag].append(verb_forms_descriptor.values)
word_features_per_pos_tag[propn_pos_tag].append(verb_forms_descriptor.values)
word_features_per_pos_tag[x_pos_tag].append(verb_forms_descriptor.values)
word_features_per_pos_tag[sym_pos_tag].append(verb_forms_descriptor.values)
feature_types_descriptor_per_id[verb_forms_descriptor.id] = verb_forms_descriptor


moods_descriptor = FeatureDescriptor('Mood', 'mood',
                                     'Mood is a feature that expresses modality and subclassifies finite verb forms.',
                                     'http://universaldependencies.org/u/feat/Mood.html', 'http://universaldependencies.org/es/feat/Mood.html',
                                     ['Mood_Adm','Mood_Cnd','Mood_Des','Mood_Imp','Mood_Ind','Mood_Jus','Mood_Nec','Mood_Opt','Mood_Pot','Mood_Prp',
                                      'Mood_Qot','Mood_Sub'])
for f in moods_descriptor.values:
    feature_descriptor_per_feature[f] = moods_descriptor
word_features_per_pos_tag[verb_pos_tag].append(moods_descriptor.values)
word_features_per_pos_tag[aux_pos_tag].append(moods_descriptor.values)
feature_types_descriptor_per_id[moods_descriptor.id] = moods_descriptor


tenses_descriptor = FeatureDescriptor('Tense', 'tense',
                                      'Tense is typically a feature of verbs. It may also occur with other parts of speech (nouns, adjectives, adverbs), depending on whether borderline word forms such as gerunds and participles are classified as verbs or as the other category.',
                                      'http://universaldependencies.org/u/feat/Tense.html', 'http://universaldependencies.org/es/feat/Tense.html',
                                      ['Tense_Fut','Tense_Imp','Tense_Past','Tense_Pqp','Tense_Pres'])
for f in tenses_descriptor.values:
    feature_descriptor_per_feature[f] = tenses_descriptor
word_features_per_pos_tag[verb_pos_tag].append(tenses_descriptor.values)
word_features_per_pos_tag[adv_pos_tag].append(tenses_descriptor.values)
word_features_per_pos_tag[adj_pos_tag].append(tenses_descriptor.values)
word_features_per_pos_tag[noun_pos_tag].append(tenses_descriptor.values)
word_features_per_pos_tag[aux_pos_tag].append(tenses_descriptor.values)
feature_types_descriptor_per_id[tenses_descriptor.id] = tenses_descriptor


aspects_descriptor = FeatureDescriptor('Aspect', 'aspect',
                                 'Aspect is typically a feature of verbs. It may also occur with other parts of speech (nouns, adjectives, adverbs), depending on whether borderline word forms such as gerunds and participles are classified as verbs or as the other category.',
                                 'http://universaldependencies.org/u/feat/Aspect.html', 'http://universaldependencies.org/es/feat/Aspect.html',
                                 ['Aspect_Hab','Aspect_Imp','Aspect_Iter','Aspect_Perf','Aspect_Prog','Aspect_Prosp'])
for f in aspects_descriptor.values:
    feature_descriptor_per_feature[f] = aspects_descriptor
word_features_per_pos_tag[verb_pos_tag].append(aspects_descriptor.values)
word_features_per_pos_tag[adv_pos_tag].append(aspects_descriptor.values)
word_features_per_pos_tag[adj_pos_tag].append(aspects_descriptor.values)
word_features_per_pos_tag[noun_pos_tag].append(aspects_descriptor.values)
feature_types_descriptor_per_id[aspects_descriptor.id] = aspects_descriptor


voices_descriptor = FeatureDescriptor('Voice', 'voice',
                                      'Voice is typically a feature of verbs. It may also occur with other parts of speech (nouns, adjectives, adverbs), depending on whether borderline word forms such as gerunds and participles are classified as verbs or as the other category.',
                                      'http://universaldependencies.org/u/feat/Voice.html', 'http://universaldependencies.org/es/feat/Voice.html',
                                      ['Voice_Act','Voice_Antip','Voice_Cau','Voice_Dir','Voice_Inv','Voice_Mid','Voice_Pass','Voice_Rcp'])
for f in voices_descriptor.values:
    feature_descriptor_per_feature[f] = voices_descriptor
word_features_per_pos_tag[verb_pos_tag].append(voices_descriptor.values)
word_features_per_pos_tag[adv_pos_tag].append(voices_descriptor.values)
word_features_per_pos_tag[adj_pos_tag].append(voices_descriptor.values)
word_features_per_pos_tag[noun_pos_tag].append(voices_descriptor.values)
feature_types_descriptor_per_id[voices_descriptor.id] = voices_descriptor


evidentialitys_descriptor = FeatureDescriptor('Evident', 'evidentiality',
                                              'Evidentiality is the morphological marking of a speaker’s source of information (Aikhenvald, 2004). It is sometimes viewed as a category of mood and modality.',
                                              'http://universaldependencies.org/u/feat/Evident.html', 'http://universaldependencies.org/u/feat/Evident.html',
                                              ['Evident_Fh','Evident_Nfh'])
for f in evidentialitys_descriptor.values:
    feature_descriptor_per_feature[f] = evidentialitys_descriptor
feature_types_descriptor_per_id[evidentialitys_descriptor.id] = evidentialitys_descriptor


polaritys_descriptor = FeatureDescriptor('Polarity', 'polarity',
                                         'Polarity is typically a feature of verbs, adjectives, sometimes also adverbs and nouns in languages that negate using bound morphemes. In languages that negate using a function word, Polarity is used to mark that function word, unless it is a pro-form already marked with PronType=Neg (see below).',
                                         'http://universaldependencies.org/u/feat/Polarity.html', 'http://universaldependencies.org/u/feat/Polarity.html',
                                         ['Polarity_Neg','Polarity_Pos'])
for f in polaritys_descriptor.values:
    feature_descriptor_per_feature[f] = polaritys_descriptor
word_features_per_pos_tag[verb_pos_tag].append(polaritys_descriptor.values)
word_features_per_pos_tag[adv_pos_tag].append(polaritys_descriptor.values)
word_features_per_pos_tag[adj_pos_tag].append(polaritys_descriptor.values)
word_features_per_pos_tag[noun_pos_tag].append(polaritys_descriptor.values)
feature_types_descriptor_per_id[polaritys_descriptor.id] = polaritys_descriptor


persons_descriptor = FeatureDescriptor('Person', 'person',
                                       'Person is typically feature of personal and possessive pronouns / determiners, and of verbs. On verbs it is in fact an agreement feature that marks the person of the verb’s subject (some languages, e.g. Basque, can also mark person of objects). Person marked on verbs makes it unnecessary to always add a personal pronoun as subject and thus subjects are sometimes dropped (pro-drop languages).',
                                       'http://universaldependencies.org/u/feat/Person.html', 'http://universaldependencies.org/es/feat/Person.html',
                                       ['Person_0','Person_1','Person_2','Person_3','Person_4'])
for f in persons_descriptor.values:
    feature_descriptor_per_feature[f] = persons_descriptor
word_features_per_pos_tag[pron_pos_tag].append(persons_descriptor.values)
word_features_per_pos_tag[det_pos_tag].append(persons_descriptor.values)
word_features_per_pos_tag[verb_pos_tag].append(persons_descriptor.values)
word_features_per_pos_tag[aux_pos_tag].append(persons_descriptor.values)
word_features_per_pos_tag[x_pos_tag].append(persons_descriptor.values)
word_features_per_pos_tag[sym_pos_tag].append(persons_descriptor.values)
feature_types_descriptor_per_id[persons_descriptor.id] = persons_descriptor


politeness_descriptor = FeatureDescriptor('Polite', 'politeness',
                                 'Various languages have various means to express politeness or respect; some of the means are morphological. Three to four dimensions of politeness are distinguished in linguistic literature. The Polite feature currently covers (and mixes) two of them',
                                 'http://universaldependencies.org/u/feat/Polite.html', 'http://universaldependencies.org/es/feat/Polite.html',
                                 ['Polite_Elev','Polite_Form','Polite_Humb','Polite_Infm'])
word_features_per_pos_tag[pron_pos_tag].append(politeness_descriptor.values)
for f in politeness_descriptor.values:
    feature_descriptor_per_feature[f] = politeness_descriptor
feature_types_descriptor_per_id[politeness_descriptor.id] = politeness_descriptor

for tag in pos_tags:
    word_features_per_pos_tag[tag] = list(itertools.chain.from_iterable(word_features_per_pos_tag[tag]))

