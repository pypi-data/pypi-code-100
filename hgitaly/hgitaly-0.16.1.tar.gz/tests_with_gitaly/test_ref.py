# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import pytest
import time

from hgext3rd.heptapod.special_ref import (
    write_gitlab_special_ref,
    special_refs,
)
from hgitaly.stub.shared_pb2 import (
    PaginationParameter,
)
from hgitaly.stub.ref_pb2 import (
    FindBranchRequest,
    FindLocalBranchesRequest,
    FindRefNameRequest,
    DeleteRefsRequest,
)
from hgitaly.stub.ref_pb2_grpc import RefServiceStub

from . import skip_comparison_tests
from .comparison import (
    normalize_commit_message,
)
if skip_comparison_tests():  # pragma no cover
    pytestmark = pytest.mark.skip


def test_compare_find_branch(gitaly_comparison):
    fixture = gitaly_comparison
    git_repo = fixture.git_repo

    fixture.hg_repo_wrapper.write_commit('foo', message="Some foo")
    gl_branch = b'branch/default'

    # mirror worked
    assert git_repo.branch_titles() == {gl_branch: b"Some foo"}

    def normalize_response(rpc_helper, resp, **kw):
        normalize_commit_message(resp.branch.target_commit)

    rpc_helper = fixture.rpc_helper(
        stub_cls=RefServiceStub,
        method_name='FindBranch',
        request_cls=FindBranchRequest,
        response_sha_attrs=['branch.target_commit.id'],
        normalizer=normalize_response,
    )

    rpc_helper.assert_compare(name=gl_branch)


def test_compare_find_local_branches(gitaly_comparison):
    fixture = gitaly_comparison
    wrapper = fixture.hg_repo_wrapper

    # make three branches with the 3 possible orderings differ
    now = time.time()
    commit_ages = {0: 30, 1: 40, 2: 20}
    for i in range(3):
        wrapper.commit_file('foo', branch='br%02d' % i, return_ctx=False,
                            utc_timestamp=now - commit_ages[i])
    # mirror worked
    assert set(fixture.git_repo.branch_titles().keys()) == {
        b'branch/br%02d' % i for i in range(3)}

    def normalize_response(rpc_helper, resp, **kw):
        for chunk in resp:
            for branch in chunk.branches:
                normalize_commit_message(branch.commit)

    rpc_helper = fixture.rpc_helper(
        stub_cls=RefServiceStub,
        method_name='FindLocalBranches',
        request_cls=FindLocalBranchesRequest,
        streaming=True,
        response_sha_attrs=['branches[].commit_id',
                            'branches[].commit.id',
                            'branches[].commit.parent_ids[]',
                            ],
        normalizer=normalize_response,
    )

    def assert_compare(limit=0, page_token='', pagination=True, **kw):
        if pagination:
            pagination_params = PaginationParameter(limit=limit,
                                                    page_token=page_token)
        else:
            pagination_params = None

        rpc_helper.assert_compare(pagination_params=pagination_params, **kw)

    for limit in (0, 3, 8, -1):
        assert_compare(limit=limit)

    # case without any pagination parameters
    assert_compare(123, pagination=False)

    assert_compare(10, page_token='refs/heads/branch/br01')

    # sort options
    for sort_by in FindLocalBranchesRequest.SortBy.values():
        assert_compare(10, sort_by=sort_by)


def test_delete_refs(gitaly_comparison):
    fixture = gitaly_comparison
    git_repo = fixture.git_repo
    hg_wrapper = fixture.hg_repo_wrapper

    base_hg_ctx = hg_wrapper.commit_file('foo')
    hg_sha = base_hg_ctx.hex()

    rpc_helper = fixture.rpc_helper(stub_cls=RefServiceStub,
                                    method_name='DeleteRefs',
                                    request_cls=DeleteRefsRequest)
    git_sha = rpc_helper.hg2git(hg_sha)

    mr_ref_name = b'merge-requests/2/train'
    mr_ref_path = b'refs/' + mr_ref_name

    def setup_mr_ref():
        git_repo.write_ref(mr_ref_path.decode(), git_sha)
        write_gitlab_special_ref(hg_wrapper.repo, mr_ref_name, hg_sha)
        hg_wrapper.reload()
        assert mr_ref_path in git_repo.all_refs()
        assert mr_ref_name in special_refs(hg_wrapper.repo)

    setup_mr_ref()

    assert_compare = rpc_helper.assert_compare
    assert_compare_errors = rpc_helper.assert_compare_errors

    assert_compare_errors(refs=[b'xy'], except_with_prefix=[b'refs/heads'])
    assert_compare(refs=[mr_ref_path])

    # unknown refs dont create errors
    unknown = b'refs/environments/imaginary'
    assert_compare(refs=[unknown])

    # also mixing unknown with known is ok
    setup_mr_ref()
    assert_compare(refs=[unknown, mr_ref_path])

    assert git_repo.all_refs() == {b'refs/heads/branch/default': git_sha}
    hg_wrapper.reload()
    assert special_refs(hg_wrapper.repo) == {}

    # using except_with_prefix
    env_ref_name = b'environments/2877'
    env_ref_path = b'refs/' + env_ref_name

    def setup_env_ref():
        git_repo.write_ref(env_ref_path.decode(), git_sha)
        write_gitlab_special_ref(hg_wrapper.repo, env_ref_name, hg_sha)
        hg_wrapper.reload()
        assert env_ref_path in git_repo.all_refs()
        assert env_ref_name in special_refs(hg_wrapper.repo)

    # on the Mercurial side, we'll consider the special ref only,
    # but on the Git side, the `refs/heads` prefix has to be ignored.
    # This is similar to what the current actual caller,
    # `Projects::AfterImportService`, does.
    for except_prefixes in (
            [b'refs/environments/', b'refs/heads/'],
            [b'refs/environments', b'refs/heads/'],
            [b'refs/envir', b'refs/heads/'],
            ):
        setup_mr_ref()
        setup_env_ref()

        assert_compare(except_with_prefix=except_prefixes)
        assert git_repo.all_refs() == {b'refs/heads/branch/default': git_sha,
                                       env_ref_path: git_sha}
        hg_wrapper.reload()
        assert special_refs(hg_wrapper.repo) == {env_ref_name: hg_sha}


def test_find_ref_name(gitaly_comparison):
    fixture = gitaly_comparison
    git_repo = fixture.git_repo
    wrapper = fixture.hg_repo_wrapper

    gl_default = b'branch/default'
    base_hg_ctx = wrapper.write_commit('foo', message="base")
    base_hg_sha = base_hg_ctx.hex()
    # TODO get_branch_sha does not work because of PosixPath not having
    # the join method (py.path.local does)
    git_sha0 = git_repo.branches()[gl_default]['sha']

    default_hg_sha = wrapper.write_commit('foo', message="default").hex()
    git_sha1 = git_repo.branches()[gl_default]['sha']

    assert git_sha0 != git_sha1

    other_hg_sha = wrapper.write_commit('foo', message="other",
                                        branch="other",
                                        parent=base_hg_ctx).hex()

    rpc_helper = fixture.rpc_helper(stub_cls=RefServiceStub,
                                    method_name='FindRefName',
                                    request_cls=FindRefNameRequest,
                                    request_sha_attrs=['commit_id'],
                                    )

    assert_compare = rpc_helper.assert_compare

    # Git returns the first ref in alphabetic order, hence not branch/default
    # for the base commit because 'default' < 'other'
    for prefix in (b'refs/heads',
                   b'refs/heads/',
                   b'refs/heads/branch',
                   b'refs/heads/branch/',
                   b'refs/heads/branch/default',
                   ):

        assert_compare(commit_id=base_hg_sha, prefix=prefix)
        assert_compare(commit_id=default_hg_sha, prefix=prefix)

    for prefix in (b'refs/heads',
                   b'refs/heads/',
                   b'refs/heads/branch',
                   b'refs/heads/branch/',
                   b'refs/heads/branch/other',
                   ):
        assert_compare(commit_id=other_hg_sha, prefix=prefix)

    # cases where response should be empty
    for prefix in (b'refs/heads/bra',
                   b'refs/heads/branch/def',
                   ):
        assert_compare(commit_id=base_hg_sha, prefix=prefix)
        assert_compare(commit_id=default_hg_sha, prefix=prefix)
