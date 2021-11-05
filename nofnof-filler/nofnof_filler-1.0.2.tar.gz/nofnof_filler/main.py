from nofnof_filler.src import NoFillNoFuture

""" THIS CODE IS OUR ORIGINAL!!!!!!!!!!
DO YOU UNDERSTAND THIS MEAN?????
YOU ARE REALLY LEARN PYTHON?????????
WRITE CODE YOURSELF!!!!!!!!!!!!!!!!!!!!!!
DO NOT COPYYYYYYYYY!!!!
*********************
**No Fill No Future**
*********************
"""

def main():
    nfnf = NoFillNoFuture()
    while True:
        nfnf.search()
        # print(nfnf.evaluated_list)
        # print(nfnf.coordinate_list)
        max_index = nfnf.evaluated_list.index(max(nfnf.evaluated_list))
        print(f"{nfnf.coordinate_list[max_index][0]} {nfnf.coordinate_list[max_index][1]}")


if __name__ == '__main__':
    main()

