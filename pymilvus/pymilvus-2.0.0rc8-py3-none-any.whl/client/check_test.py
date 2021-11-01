from .check import check_pass_param

if __name__ == "__main__":
    a = [[i * j for i in range(20)] for j in range(20)]

    check_pass_param(search_data=a)
