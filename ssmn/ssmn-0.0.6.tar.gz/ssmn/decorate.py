def plb():
    print("Loading bar")

    return 0

def loading(전체, 번째):
    entire1 = int(전체)  # 전체 개수
    th1 = int(번째)
    loadingv1 = entire1 - th1
    text1 = "□" * loadingv1
    loadingv2 = entire1 - loadingv1
    text2 = "■" * loadingv2
    print("-----[" + text2 + text1 + "]-----")

    return 0

def howd():
    print("Hello, World!")