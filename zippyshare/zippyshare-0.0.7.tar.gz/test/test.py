import zippyshare
import zippyshare.utils
import traceback


# zippyshare.utils.generate_account_info()
# create accounts manually or bypass captcha yourself


credentials = zippyshare.utils.read_account_info(open("zippy.txt", "rb").read().decode())


zs = zippyshare.zippyshare(
    vpncmd_option={
        "vpncmd_fp": r"C:\Program Files\SoftEther VPN Client\vpncmd_x64.exe"
    },
    vpncmd_setup_cmd_option=[
        "/client",
        "localhost",
    ],
    debug=True
)


zs.login(credentials=credentials[0][2:4])


try:
    # print(zs.s.get("https://httpbin.org/get").content.decode())
    print(zs.remote_upload("https://pastebin.com/raw/sViuU9AN"))
except:
    traceback.print_exc()


zs.logout()

