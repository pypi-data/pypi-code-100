NIL_PTR = "NIL"
CPVCS_DIR = ".cpvcs"
DEFAULT_POD_DIR = "cpvcs-pod"
OBJ_STORE_DIR = "objects"
REV_SUB_DIR = "rev"
VER_SUB_DIR = "ver"
DELTA_LOG_DIR = "deltas"
HEAD_FILE = "HEAD"
VER_LOG_FILE = "VER_LOG"
MAX_VER_FILE = "MAX_VER"
KNOWN_VER_FILE = "KNOWN_VER"
REFS_DIR = "refs"
VER_SYMLINK = "{ver_no}"
REV_SYMLINK = "{rid}_{rev_no}"
META_ZIP = "version_{version_no}_meta"
COMMIT_FILE = "commit_no_{commit_no}.json"
COMPRESSION_FORMAT = "zip"
STATE_TXT_LAYOUT = "size:{size}, service:{service}, region:{region}, key:{hash},file_name:{file_name}, rel_path:{rel_path}"
STATE_TXT_METADATA = "size: {size}, service:{service}, region: {region}"
COMMIT_TXT_LAYOUT = (
    "tail:{tail_ptr}, head:{head_ptr}, message:{message}, timestamp:{timestamp}, log_key:{log_hash}"
)
VER_TXT_LAYOUT = """parent_ptr={parent}
hash_ref={hash}
creator={creator}
comment={comment}
version_number={version_number}
active_revision_ptr={active_revision}
outgoing_revision_ptrs={outgoing_revisions}
incoming_revision_ptr={incoming_revision}
state_files={state_files}
"""
REV_TXT_LAYOUT = """parent_ptr={parent}
hash_ref={hash}
creator={creator}
rid={rid}
revision_number={rev_no}
state_files={state_files}
assoc_commit={assoc_commit}
"""
VER_LOG_STRUCTURE = "{author};{ver_no};{rev_rid_no}"
