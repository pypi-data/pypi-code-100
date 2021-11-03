import numpy as np
import pandas as pd


class TensorFrame:

    def __init__(self, tensor, *dim_name_list):

        assert len(tensor.shape) == len(dim_name_list)

        ndim = len(tensor.shape)
        for i in range(ndim):
            assert isinstance(dim_name_list[i], list)
        for i in range(ndim):
            assert tensor.shape[i] == len(dim_name_list[i])
        for i in range(ndim):
            exec('self.name{}d = dim_name_list[i]'.format(i + 1))

        self.ndim = ndim
        self.tensor = tensor

        self.shape = tensor.shape

    def get_dim_name_list(self):
        dim_name_list = []
        for i in range(self.ndim):
            command_str = 'dim_name_list.append(self.name{}d)'.format(i + 1)
            exec(command_str)
        return dim_name_list

    def to_frame(self, *attr_list):

        n_attr = len(attr_list)
        assert (self.ndim - n_attr) == 2

        dim_name_list = self.get_dim_name_list()

        tindx = [slice(n) for n in self.tensor.shape]
        for i in range(self.ndim):
            dim_name = dim_name_list[i]
            for j in range(n_attr):
                attr = attr_list[j]
                if attr in dim_name:
                    tindx[i] = dim_name.index(attr)
        i_frdim = np.where([not np.isscalar(item) for item in tindx])[0]
        assert len(i_frdim) == 2
        rname = dim_name_list[i_frdim[0]]
        cname = dim_name_list[i_frdim[1]]
        tindx = tuple(tindx)  # avoid warnings
        df = pd.DataFrame(self.tensor[tindx], index=rname, columns=cname)
        return df

    def to_series(self, *attr_list):

        n_attr = len(attr_list)
        assert (self.ndim - n_attr) == 1

        dim_name_list = self.get_dim_name_list()

        tindx = [slice(n) for n in self.tensor.shape]
        for i in range(self.ndim):
            dim_name = dim_name_list[i]
            for j in range(n_attr):
                attr = attr_list[j]
                if attr in dim_name:
                    tindx[i] = dim_name.index(attr)
        i_frdim = np.where([not np.isscalar(item) for item in tindx])[0]
        assert len(i_frdim) == 1
        rname = dim_name_list[i_frdim[0]]
        tindx = tuple(tindx)  # avoid warnings
        sr = pd.Series(self.tensor[tindx], index=rname)
        return sr

    def count_nan(self, axis=None):
        if axis is None:
            return np.sum(np.isnan(self.tensor))
        else:
            return np.sum(np.isnan(self.tensor), axis=axis)

    def subset(self, select):
        # select is dictionary
        # for example: {'2d': ['mean', 'median', 'min7d']}

        dim_name_list = self.get_dim_name_list()

        for key in select:
            i_dim = int(key[:-1]) - 1
            assert i_dim < self.ndim

        for key in select:
            i_dim = int(key[:-1]) - 1
            all_attr = dim_name_list[i_dim]
            sel_attr = select[key]
            assert set(sel_attr).issubset(set(all_attr))

        tensor = self.tensor.copy()
        for key in select:
            i_dim = int(key[:-1]) - 1
            all_attr = dim_name_list[i_dim]
            sel_attr = select[key]
            sel_indx = [all_attr.index(item) for item in sel_attr]
            dim_name_list[i_dim] = sel_attr
            tensor = tensor.take(sel_indx, axis=i_dim)
        return TensorFrame(tensor, *dim_name_list)

    def append(self, new_tframe, axis):

        assert self.ndim == new_tframe.ndim

        dim_name_list_cur = self.get_dim_name_list()
        dim_name_list_add = new_tframe.get_dim_name_list()

        for i in range(self.ndim):
            if i == axis:
                name_list_cur = dim_name_list_cur[i]
                name_list_new = dim_name_list_add[i]
                name_list_dup = set(name_list_cur).intersection(name_list_new)
                assert len(name_list_dup) == 0
            else:
                assert dim_name_list_cur[i] == dim_name_list_add[i]

        dim_name_list = []
        for i in range(self.ndim):
            if i == axis:
                name_list_cur = dim_name_list_cur[i]
                name_list_new = dim_name_list_add[i]
                dim_name_list.append(name_list_cur + name_list_new)
            else:
                dim_name_list.append(dim_name_list_cur[i])
        tensor = np.concatenate([self.tensor, new_tframe.tensor], axis=axis)
        return TensorFrame(tensor, *dim_name_list)

    def transpose(self, new_dim_order):

        assert len(new_dim_order) == self.ndim
        # switch dimension name
        dim_name_list = self.get_dim_name_list()
        dim_name_list = [dim_name_list[i] for i in new_dim_order]

        tensor = self.tensor.transpose(new_dim_order)
        return TensorFrame(tensor, *dim_name_list)

    def sort(self, axis):

        dim_name_list = self.get_dim_name_list()

        dim_name = dim_name_list[axis]
        dim_name_list[axis] = np.sort(dim_name).tolist()

        idx_list = [slice(n) for n in self.shape]
        idx_list[axis] = np.argsort(dim_name)

        tensor = self.tensor[tuple(idx_list)]

        return TensorFrame(tensor, *dim_name_list)


# input must be either DataFrame or TensorFrame
# return False
#   if types are different
#   if names are different
def is_equal_frame(data_list):

    ref_data = data_list[0]
    ref_type = type(ref_data)
    ref_shape = ref_data.shape

    is_equal = False

    if all([type(item) == ref_type for item in data_list]):

        if all([item.shape == ref_shape for item in data_list]):

            is_equal_list = []

            if ref_type == pd.DataFrame:

                ref_index = ref_data.index.tolist()
                ref_columns = ref_data.columns.tolist()

                for data in data_list:

                    target_index = data.index.tolist()
                    target_columns = data.columns.tolist()

                    is_equal_list.append(target_index == ref_index)
                    is_equal_list.append(target_columns == ref_columns)

            else:

                ref_name_list = ref_data.get_dim_name_list()
                n_dim = len(ref_name_list)

                is_equal_list = []
                for data in data_list:
                    target_name_list = data.get_dim_name_list()
                    for i in range(n_dim):
                        is_equal = target_name_list[i] == ref_name_list[i]
                        is_equal_list.append(is_equal)

            is_equal = all(is_equal_list)

    return is_equal


def stack_df_to_tframe(df_list, name3d):

    assert is_equal_frame(df_list)
    assert len(df_list) == len(name3d)

    name1d = df_list[0].index.tolist()
    name2d = df_list[0].columns.tolist()
    tensor = np.dstack([df.values for df in df_list])
    tframe = TensorFrame(tensor, name1d, name2d, name3d)
    return tframe
