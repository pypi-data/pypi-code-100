import numpy as np
import torch.nn as nn
import torch
import torch.nn.functional as F

class Circuit(object):
    def __init__(self, N):
        self._U = None
        self.n_qubits = N  # 总QuBit的个数
        self.gate_list = []  # 顺序保存门结构
        self.u = []    # 顺序保存酉矩阵

#   内置函数 添加分拆资源
    def _add_gate(self, gate_name: str, target_qubit, gate_params):
        """add gate and its feature to the circuit by sequence.

        """
        # assert gate_name in list[]  #todo 创建一个可信池子
        self.gate_list.append({'gate': gate_name, 'theta': gate_params, 'which_qubit': target_qubit})

    def _add_u(self, u_matrix):
        """add u_matrix to the circuit by sequence.

        """
        # assert u_name in list[]  #todo 创建一个可信池子
        self.u.append(u_matrix)

#   内置操作函数：张量积、  1toN、  两比特控制门toN、 两比特旋转门toN、  多比特控制门toN、 计算列表最终的酉矩阵
    def multi_kron(self, x_list):
        """
        kron the data in the list in order
        """
        x_k = torch.ones(1)
        for x in x_list:
            x_k = torch.kron(x_k, x)
        return x_k

    def gate_expand_1toN(self, U, N, target):
        """
        representing a one-qubit gate that act on a system with N qubits.

        """

        if N < 1:
            raise ValueError("integer N must be larger or equal to 1")

        if target >= N:
            raise ValueError("target must be integer < integer N")

        return self.multi_kron([torch.eye(2)] * target + [U] + [torch.eye(2)] * (N - target - 1))

    def gate_expand_2toN(self, U, N, targets):
        """
        representing a two-qubit gate that act on a system with N qubits.

        """

        if N < 2:
            raise ValueError("integer N must be larger or equal to 2")

        if targets[1] >= N:
            raise ValueError("target must be integer < integer N")

        return self.multi_kron([torch.eye(2)] * targets[0] + [U] + [torch.eye(2)] * (N - targets[1] - 1))

    def gate_sequence_product(self, left_to_right=True):
        """
        Calculate the overall unitary matrix for a given list of unitary operations.
        return: Unitary matrix corresponding to U_list.
        """

        U_overall = torch.eye(2 ** self.n_qubits, 2 ** self.n_qubits) + 0j
        for U in self.u:
            if left_to_right:
                U_overall = U @ U_overall
            else:
                U_overall = U_overall @ U
        self._U = U_overall
        return U_overall

    def two_qubit_control_gate(self, U, N, control, target):
        if N < 1:
            raise ValueError("integer N must be larger or equal to 1")
        if control >= N:
            raise ValueError("control must be integer < integer N")
        if target >= N:
            raise ValueError("target must be integer < integer N")
        if target == control:
            raise ValueError("control cannot be equal to target")

        zero_zero = torch.tensor([[1, 0], [0, 0]]) + 0j
        one_one = torch.tensor([[0, 0], [0, 1]]) + 0j
        list1 = [torch.eye(2)] * N
        list2 = [torch.eye(2)] * N
        list1[control] = zero_zero
        list2[control] = one_one
        list2[target] = U

        return self.multi_kron(list1) + self.multi_kron(list2)

    def two_qubit_rotation_gate(self, theta, N, qbit1, qbit2, way):
        # if type(theta) != type(torch.tensor(0.1)):
        #     theta = torch.tensor(theta)
        if N < 1:
            raise ValueError("number of qubits N must be >= 1")
        if qbit1 < 0 or qbit1 > N - 1 or qbit2 < 0 or qbit2 > N - 1:
            raise ValueError("index must between 0~N-1")
        if qbit1 == qbit2:
            raise ValueError("qbit1 cannot be equal to qbit2")
        lst1 = [torch.eye(2, 2)] * self.n_qubits
        lst2 = [torch.eye(2, 2)] * self.n_qubits
        if way == 'rxx':
            lst2[qbit1] = self._x_gate()
            lst2[qbit2] = self._x_gate()
        elif way == 'ryy':
            lst2[qbit1] = self._y_gate()
            lst2[qbit2] = self._y_gate()
        elif way == 'rzz':
            lst2[qbit1] = self._z_gate()
            lst2[qbit2] = self._z_gate()
        else:
            raise ValueError("Error gate")
        rst = torch.cos(theta / 2) * self.multi_kron(lst1) - 1j * torch.sin(theta / 2) * self.multi_kron(lst2)
        return rst + 0j

    def multi_control_gate(self, U, N, control_lst, target):
        '''
        多控制比特受控门，比如典型的toffoli gate就是2个控制1个受控
        control_lst:一个列表，内部是控制比特的索引号
        '''
        if N < 1:
            raise ValueError("number of qubits(interger N) must be >= 1")

        if max(max(control_lst), target) > N - 1:
            raise ValueError("control&target must <= number of qubits - 1")

        if min(min(control_lst), target) < 0:
            raise ValueError("control&target must >= 0")

        for each in control_lst:
            if each == target:
                raise ValueError("control cannot be equal to target")

        U = U + 0j
        one_one = torch.tensor([[0, 0], [0, 1]]) + 0j

        lst1 = [torch.eye(2, 2)] * N
        for each in control_lst:
            lst1[each] = one_one
        lst1[target] = U

        lst2 = [torch.eye(2, 2)] * N

        lst3 = [torch.eye(2, 2)] * N
        for each in control_lst:
            lst3[each] = one_one
        # multi_kron(lst2) - multi_kron(lst3)对应不做操作的哪些情况
        return self.multi_kron(lst2) - self.multi_kron(lst3) + self.multi_kron(lst1)

#   实例调用部分可使用的函数 添加门、run线路
    def rx(self, target_qubit, phi):
        assert isinstance(target_qubit, int), \
            "target qubit is not integer"
        assert 0 <= target_qubit < self.n_qubits, \
            "target qubit is not available"
        self._add_gate('rx', target_qubit, phi)
        if type(phi) == float or type(phi) == int:
            phi = torch.tensor(phi)
            self._add_u(self.gate_expand_1toN(self._rx(phi), self.n_qubits, target_qubit))
        else:
            self._add_u(self.gate_expand_1toN(self._rx(phi), self.n_qubits, target_qubit))

    def ry(self, target_qubit, phi):
        assert isinstance(target_qubit, int), \
            "target qubit is not integer"
        assert 0 <= target_qubit < self.n_qubits, \
            "target qubit is not available"
        self._add_gate('ry', target_qubit, phi)
        if type(phi) == float or type(phi) == int:
            phi = torch.tensor(phi)
            self._add_u(self.gate_expand_1toN(self._ry(phi), self.n_qubits, target_qubit))
        else:
            self._add_u(self.gate_expand_1toN(self._ry(phi), self.n_qubits, target_qubit))

    def rz(self, target_qubit, phi):
        assert isinstance(target_qubit, int), \
            "target qubit is not integer"
        assert 0 <= target_qubit < self.n_qubits, \
            "target qubit is not available"
        self._add_gate('rz', target_qubit, phi)
        if type(phi) == float or type(phi) == int:
            phi = torch.tensor(phi)
            self._add_u(self.gate_expand_1toN(self._rz(phi), self.n_qubits, target_qubit))
        else:
            self._add_u(self.gate_expand_1toN(self._rz(phi), self.n_qubits, target_qubit))

    def cnot(self, control_qubit: int, target_qubit: int):
        assert isinstance(target_qubit, int), \
            "target qubit is not integer"
        assert isinstance(control_qubit, int), \
            "control qubit is not integer"
        assert control_qubit <= self.n_qubits
        assert 0 <= target_qubit < self.n_qubits, \
            "target qubit is not available"
        self._add_gate('cnot', control_qubit, target_qubit)
        self._add_u(self.two_qubit_control_gate(self._x_gate(), self.n_qubits, control_qubit, target_qubit))

    def x_gate(self, target_qubit):
        assert isinstance(target_qubit, int), \
            "target qubit is not integer"
        assert 0 <= target_qubit < self.n_qubits, \
            "target qubit is not available"
        self._add_gate('X', target_qubit, None)
        self._add_u(self.gate_expand_1toN(self._x_gate(), self.n_qubits, target_qubit))

    def z_gate(self, target_qubit):
        assert isinstance(target_qubit, int), \
            "target qubit is not integer"
        assert 0 <= target_qubit < self.n_qubits, \
            "target qubit is not available"
        self._add_gate('Z', target_qubit, None)
        self._add_u(self.gate_expand_1toN(self._z_gate(), self.n_qubits, target_qubit))

    def y_gate(self, target_qubit):
        assert isinstance(target_qubit, int), \
            "target qubit is not integer"
        assert 0 <= target_qubit < self.n_qubits, \
            "target qubit is not available"
        self._add_gate('Y', target_qubit, None)
        self._add_u(self.gate_expand_1toN(self._y_gate(), self.n_qubits, target_qubit))

    def Hcz(self, control_qubit, target_qubit):
        assert isinstance(target_qubit, int), \
            "target qubit is not integer"
        assert isinstance(control_qubit, int), \
            "control qubit is not integer"
        assert control_qubit <= self.n_qubits
        assert 0 <= target_qubit < self.n_qubits, \
            "target qubit is not available"

        self._add_gate('cz', control_qubit, target_qubit)
        self._add_u(self.two_qubit_control_gate(self._z_gate(), self.n_qubits, control_qubit, target_qubit))

    def Hadamard(self, target_qubit):
        assert isinstance(target_qubit, int), \
            "target qubit is not integer"
        assert 0 <= target_qubit < self.n_qubits, \
            "target qubit is not available"
        self._add_gate('H', target_qubit, None)
        self._add_u(self.gate_expand_1toN(self._Hadamard(), self.n_qubits, target_qubit))

    def rxx(self, target_qubit01, target_qubit02, phi):
        assert isinstance(target_qubit01, int), \
            "target qubit is not integer"
        assert isinstance(target_qubit02, int), \
            "target qubit is not integer"
        if not target_qubit02:
            target_qubit02 = target_qubit01 + 1
        assert target_qubit01 <= self.n_qubits
        assert target_qubit02 <= self.n_qubits

        self._add_gate('rxx', target_qubit01, phi)
        self._add_gate('rxx', target_qubit02, phi)
        if type(phi) == float or type(phi) == int:
            phi = torch.tensor(phi)
            self._add_u(self.two_qubit_rotation_gate(phi, self.n_qubits, target_qubit01, target_qubit02, way='rxx'))
        else:
            self._add_u(self.two_qubit_rotation_gate(phi, self.n_qubits, target_qubit01, target_qubit02, way='rxx'))

    def ryy(self, target_qubit01, target_qubit02, phi):
        assert isinstance(target_qubit01, int), \
            "target qubit is not integer"
        assert isinstance(target_qubit02, int), \
            "target qubit is not integer"

        if not target_qubit02:
            target_qubit02 = target_qubit01 + 1
        assert target_qubit01 <= self.n_qubits
        assert target_qubit02 <= self.n_qubits
        assert target_qubit01 != target_qubit02, \
            "target qubit should not be the same"

        self._add_gate('ryy', target_qubit01, phi)
        self._add_gate('ryy', target_qubit02, phi)
        if type(phi) == float or type(phi) == int:
            phi = torch.tensor(phi)
            self._add_u(self.two_qubit_rotation_gate(phi, self.n_qubits, target_qubit01, target_qubit02, way='ryy'))
        else:
            self._add_u(self.two_qubit_rotation_gate(phi, self.n_qubits, target_qubit01, target_qubit02, way='ryy'))

    def rzz(self, target_qubit01, target_qubit02, phi):
        assert isinstance(target_qubit01, int), \
            "target qubit is not integer"
        assert isinstance(target_qubit02, int), \
            "target qubit is not integer"
        if not target_qubit02:
            target_qubit02 = target_qubit01 + 1
        assert target_qubit01 <= self.n_qubits
        assert target_qubit02 <= self.n_qubits

        self._add_gate('rzz', target_qubit01, phi)
        self._add_gate('rzz', target_qubit02, phi)
        if type(phi) == float or type(phi) == int:
            phi = torch.tensor(phi)
            self._add_u(self.two_qubit_rotation_gate(phi, self.n_qubits, target_qubit01, target_qubit02, way='rzz'))
        else:
            self._add_u(self.two_qubit_rotation_gate(phi, self.n_qubits, target_qubit01, target_qubit02, way='rzz'))

    def multi_control_cnot(self, control_lst, target):
        self._add_u(self.multi_control_gate(self._x_gate(), self.n_qubits, control_lst, target))

    def U(self):
        return self.gate_sequence_product()

#   内置函数
    def _I(self):
        """Single-qubit Identification gate
        -------
        result : torch.tensor for operator describing Identity matrix.
        """

        return torch.eye(2) + 0j

    def _rx(self, phi):
        """Single-qubit rotation for operator sigmax with angle phi.
        -------
        result : torch.tensor for operator describing the rotation.
        """

        return torch.cat((torch.cos(phi / 2).unsqueeze(dim=0), -1j * torch.sin(phi / 2).unsqueeze(dim=0),
                          -1j * torch.sin(phi / 2).unsqueeze(dim=0), torch.cos(phi / 2).unsqueeze(dim=0)),
                         dim=0).reshape(2,
                                        -1)

    def _ry(self, phi):
        """Single-qubit rotation for operator sigmay with angle phi.
        -------
        result : torch.tensor for operator describing the rotation.
        """

        return torch.cat((torch.cos(phi / 2).unsqueeze(dim=0), -1 * torch.sin(phi / 2).unsqueeze(dim=0),
                          torch.sin(phi / 2).unsqueeze(dim=0), torch.cos(phi / 2).unsqueeze(dim=0)), dim=0).reshape(2,
                                                                                                                    -1) + 0j

    def _rz(self, phi):
        """Single-qubit rotation for operator sigmaz with angle phi.
        -------
        result : torch.tensor for operator describing the rotation.
        """
        return torch.cat((torch.exp(-1j * phi / 2).unsqueeze(dim=0), torch.zeros(1),
                          torch.zeros(1), torch.exp(1j * phi / 2).unsqueeze(dim=0)), dim=0).reshape(2, -1)

    def _z_gate(self):
        """
        Pauli z
        """
        return torch.tensor([[1, 0], [0, -1]]) + 0j

    def _x_gate(self):
        """
        Pauli x
        """
        return torch.tensor([[0, 1], [1, 0]]) + 0j

    def _y_gate(self):
        """
        Pauli x
        """
        return torch.tensor([[0,-1j],[1j,0]]) + 0j

    def _Hadamard(self):
        H = torch.sqrt(torch.tensor(0.5)) * torch.tensor([[1, 1], [1, -1]]) + 0j
        return H


def multi_kron(x_list):
        """
        kron the data in the list in order
        """
        x_k = torch.ones(1)
        for x in x_list:
            x_k = torch.kron(x_k, x)
        return x_k

def gate_expand_1toN(U, N, target):
        """
        representing a one-qubit gate that act on a system with N qubits.

        """

        if N < 1:
            raise ValueError("integer N must be larger or equal to 1")

        if target >= N:
            raise ValueError("target must be integer < integer N")

        return multi_kron([torch.eye(2)] * target + [U] + [torch.eye(2)] * (N - target - 1))

def z_gate():
        """
        Pauli z
        """
        return torch.tensor([[1, 0], [0, -1]]) + 0j

def dag(x):
    """
    compute conjugate transpose of input matrix
    """
    x_conj = torch.conj(x)
    x_dag = x_conj.permute(1, 0)
    return x_dag

def expecval_ZI(state, nqubit, target):
    """
    state为nqubit大小的密度矩阵，target为z门放置位置

    """
    zgate = z_gate()
    H = gate_expand_1toN(zgate, nqubit, target)
    expecval = (state @ H).trace()  # [-1,1]
    expecval_real = (expecval.real + 1) / 2  # [0,1]

    return expecval_real

def measure(self, state, nqubit):
    """
        测量nqubit次期望

    """
    measure = torch.zeros(nqubit, 1)
    for i in range(nqubit):
        measure[i] = self.expecval_ZI(state, nqubit, list(range(nqubit))[i])

    return measure

def IsUnitary(in_matrix):
    '''
    判断一个矩阵是否是酉矩阵
    '''
    if (in_matrix.shape)[0] != (in_matrix.shape)[1]:  # 验证是否为方阵
        raise ValueError("not square matrix!")
        return False

    n = in_matrix.shape[0]  # 行数

    for i in range(n):  # 每行是否归一
        summ = 0.0
        for j in range(n):
            summ += (abs(in_matrix[i][j])) ** 2
        if abs(summ - 1) > 1e-6:
            print("not unitary")
            return False

    for j in range(n):  # 每列是否归一
        summ = 0.0
        for i in range(n):
            summ += (abs(in_matrix[i][j])) ** 2
        if abs(summ - 1) > 1e-6:
            print("not unitary")
            return False

    for i in range(n - 1):  # 行之间是否正交
        for k in range(i + 1, n):
            summ = 0.0 + 0.0 * 1j
            for j in range(n):
                summ += in_matrix[i][j] * (in_matrix[k][j]).conj()
            if abs(abs(summ) - 0) > 1e-6:
                print("not orthogonal")
                return False

    for j in range(n - 1):  # 列之间是否正交
        for k in range(j + 1, n):
            summ = 0.0 + 0.0 * 1j
            for i in range(n):
                summ += in_matrix[i][j] * (in_matrix[i][k]).conj()
            if abs(abs(summ) - 0) > 1e-6:
                print("not orthogonal")
                return False
    return True

def ptrace(rhoAB, dimA, dimB):
    """
    rhoAB : density matrix
    dimA: n_qubits A keep
    dimB: n_qubits B trash
    """
    mat_dim_A = 2 ** dimA
    mat_dim_B = 2 ** dimB

    id1 = torch.eye(mat_dim_A, requires_grad=True) + 0.j
    id2 = torch.eye(mat_dim_B, requires_grad=True) + 0.j

    pout = 0
    for i in range(mat_dim_B):
        p = torch.kron(id1, id2[i]) @ rhoAB @ torch.kron(id1, id2[i].reshape(mat_dim_B, 1))
        pout += p
    return pout

def encoding(x):
    """
    input: n*n matrix
    perform L2 regularization on x, x为complex
    """

    # if x.norm() != 1 :
    #     # print('l2norm:', x.norm())
    #     x = x / (x.norm() + 1e-10)
    # x = x.type(dtype=torch.complex64)
    # return x
    # from sklearn.preprocessing import normalize
    # xn = normalize(x, norm='l2', axis=0)
    with torch.no_grad():
        # x = x.squeeze()
        if x.norm() != 1:
            xd = x.diag()
            xds = (xd.sqrt()).unsqueeze(1)
            xdsn = xds / (xds.norm() + 1e-12)
            xdsn2 = xdsn @ dag(xdsn)
            xdsn2 = xdsn2.type(dtype=torch.complex64)
        else:
            xdsn2 = x.type(dtype=torch.complex64)
    # if x.norm() != 1:
    #     with torch.no_grad():
    #         xd = x.diag()
    #         xds = (xd.sqrt()).unsqueeze(1)
    #         xdsn = xds / (xds.norm() + 1e-12)
    #         xdsn2 = xdsn @ dag(xdsn)
    #         xdsn2 = xdsn2.type(dtype=torch.complex64)
    # else:
    #     xdsn2 = x.type(dtype=torch.complex64)
    return xdsn2



# 例子
class QEqualizedConv0(nn.Module):
    """
    Quantum Conv layer with equalized learning rate and custom learning rate multiplier.
    """

    def __init__(self, n_qubits,
                 gain=2 ** 0.5, use_wscale=True, lrmul=1):
        super().__init__()

        he_std = gain * 5 ** (-0.5)  # He init
        if use_wscale:
            init_std = 1.0 / lrmul
            self.w_mul = he_std * lrmul
        else:
            init_std = he_std / lrmul
            self.w_mul = lrmul
        self.weight = nn.Parameter(nn.init.uniform_(torch.empty(5), a=0.0, b=2 * np.pi) * init_std)

        self.n_qubits = n_qubits

    def qconv0(self):
        w = self.weight * self.w_mul
        # 新增线路实例申明
        cir = Circuit(self.n_qubits)

        # 新添加门写法
        for which_q in range(0, self.n_qubits, 2):
            cir.rx(which_q, w[0])
            cir.rx(which_q, w[1])
            cir.ryy(which_q, which_q + 1, w[2])
            cir.rz(which_q, w[3])
            cir.rz(which_q + 1, w[4])
        U = cir.U()

        # #旧写法
        # cir = []
        # for which_q in range(0, self.n_qubits, 2):
        #     cir.append(gate_expand_1toN(rx(w[0]), self.n_qubits, which_q))
        #     cir.append(gate_expand_1toN(rx(w[1]), self.n_qubits, which_q + 1))
        #     cir.append(gate_expand_2toN(ryy(w[2]), self.n_qubits, [which_q, which_q + 1]))
        #     cir.append(gate_expand_1toN(rz(w[3]), self.n_qubits, which_q))
        #     cir.append(gate_expand_1toN(rz(w[4]), self.n_qubits, which_q + 1))
        # U = gate_sequence_product(cir, self.n_qubits)

        return U

    def forward(self, x):
        E_qconv0 = self.qconv0()
        qconv0_out = dag(E_qconv0) @ x @ E_qconv0
        return qconv0_out
