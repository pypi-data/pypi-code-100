def get_bits(x):
    num_bits = int(10* int(x/3))+ int(4* int(int(x % 3)% 2))+int(7 * int(int(x % 3) /2))
    return num_bits
