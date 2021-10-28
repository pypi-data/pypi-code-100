from collections import defaultdict


def docs2stream(docs, doc2pt, doc2time=None, meta_requirements={}, entity_type_column='tuis'):
    r''' Convert the `docs` output of medcat multiprocessing
    to a stream of concepts for each patient.

    Args:
        docs
        doc2pt
        doc2time
        meta_requirements:
            Values for meta_annotaitons that must exist e.g. = {'Presence': True}
    '''
    cui2pt2cnt = defaultdict(lambda: defaultdict(int))
    pt2stream = defaultdict(list)

    # Frequency for each each entity given a patient
    for doc in docs:
        for ent in docs[doc]['entities'].values():
            # Must match all meta meta_anns
            if not meta_requirements or all([ent['meta_anns'][name]['value'] == value for name, value in meta_requirements.items()]):
                cui = ent['cui']
                pt = doc2pt[doc]
                cui2pt2cnt[cui][pt] += 1

    for doc in docs:
        for ent in docs[doc]['entities'].values():
            if not meta_requirements or all([ent['meta_anns'][name]['value'] == value for name, value in meta_requirements.items()]):
                cui = ent['cui']
                pt = doc2pt[doc]
                if doc2time is not None:
                    timestamp = doc2time[doc]
                else:
                    timestamp = ent['document_timestamp']
                cnt = cui2pt2cnt[cui][pt]
                if ent[entity_type_column]: # This can be none in some cases
                    token_type = ent[entity_type_column][0]
                else:
                    raise Exception("Entity type must be set")

                pt2stream[pt].append((cui, cnt, timestamp, token_type))

    return dict(pt2stream) # Convert into a standard dict, we do not need the functionality anymore
