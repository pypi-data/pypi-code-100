from omnitools import debug_info
def main():
    print(debug_info(indent=1)[0])


    print()


    print(debug_info(info="0"*80, indent=2, indent_scale=3)[0])


    print()


    try:
        print(debug_info(info=obj)[0])
    except:
        print(debug_info()[0])
        print(debug_info()[1])


if __name__ == "__main__":
    main()
