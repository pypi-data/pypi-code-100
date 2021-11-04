import os
import sneaky
import sneaky.helper
import traceback
from undetected_chromedriver.v2 import ChromeOptions


def test_recaptcha(driver: sneaky.Chrome, vpncmd: sneaky.vpncmd):
    driver.get("https://www.google.com/recaptcha/api2/demo")

    driver.execute_script('''
    var div = document.createElement("div");
    div.id = "test_move";
    var style = "top:0;left:0;position: absolute;width:10px;height:10px;background:green;z-index:99999999999;border: 2px solid blue;pointer-events:none;opacity: 0.666;";
    div.style = style;
    document.body.appendChild(div);
    window.addEventListener("mousemove", function(e){
        div.style = style+"top: "+e.pageY+"px;left: "+e.pageX+"px;";
    });
    ''')

    recaptcha_iframe1 = driver.xpath("//iframe[@title]")[0]
    recaptcha_iframe1_pos = [recaptcha_iframe1.rect["x"], recaptcha_iframe1.rect["y"]]
    driver.print_element(recaptcha_iframe1)
    print("recaptcha_iframe1", recaptcha_iframe1_pos, recaptcha_iframe1.rect)

    driver.switch_to.frame(recaptcha_iframe1)
    recaptcha_btn = driver.xpath("//*[@id='recaptcha-anchor']")[0]
    recaptcha_btn_pos = [recaptcha_btn.rect["x"], recaptcha_btn.rect["y"]]
    driver.print_element(recaptcha_btn)
    print("recaptcha_btn", recaptcha_btn_pos, recaptcha_btn.rect)

    click_x = recaptcha_iframe1_pos[0]+recaptcha_btn_pos[0]+(recaptcha_btn.rect["width"])/2
    click_y = recaptcha_iframe1_pos[1]+recaptcha_btn_pos[1]+(recaptcha_btn.rect["height"])/2
    print("recaptcha_btn click_x click_y", click_x, click_y)
    driver.switch_to.default_content()
    driver.execute_script('''arguments[0].style.pointerEvents = "none";''', recaptcha_iframe1)
    driver.mimic_move_to_random_xy()
    driver.execute_script('''arguments[0].style.pointerEvents = "all";''', recaptcha_iframe1)
    while "hidden" in driver.xpath("//iframe[@title]/../..")[1].get_attribute("style"):
        driver.wait(1)
        driver.execute_script('''arguments[0].style.pointerEvents = "none";''', recaptcha_iframe1)
        driver.mimic_move_to_xy(click_x, click_y)
        driver.execute_script('''arguments[0].style.pointerEvents = "all";''', recaptcha_iframe1)
        driver.mimic_click()
        driver.wait(1)
        print("recaptcha_btn click loop", driver.xpath("//iframe[@title]/../..")[1].get_attribute("style"))
        driver.wait(1)
        driver.execute_script('''arguments[0].style.pointerEvents = "none";''', recaptcha_iframe1)
        driver.mimic_move_to_random_xy()
        driver.execute_script('''arguments[0].style.pointerEvents = "all";''', recaptcha_iframe1)

    recaptcha_iframe2 = driver.xpath("//iframe[@title]")[1]
    recaptcha_iframe2_pos = [recaptcha_iframe2.rect["x"], recaptcha_iframe2.rect["y"]]
    driver.print_element(recaptcha_iframe2)
    print("recaptcha_iframe2", recaptcha_iframe2_pos, recaptcha_iframe2.rect)

    driver.switch_to.frame(recaptcha_iframe2)
    solver_btn = driver.xpath("//*[contains(@class, 'help-button-holder')]")[0]
    solver_btn_pos = [solver_btn.rect["x"], solver_btn.rect["y"]]
    driver.print_element(solver_btn)
    print("solver_btn", solver_btn_pos, solver_btn.rect)
    
    click_x = recaptcha_iframe2_pos[0]+solver_btn_pos[0]+solver_btn.rect["width"]/2
    click_y = recaptcha_iframe2_pos[1]+solver_btn_pos[1]+solver_btn.rect["height"]/2
    print("solver_btn click_x click_y", click_x, click_y)
    driver.switch_to.default_content()
    driver.execute_script('''arguments[0].style.pointerEvents = "none";''', recaptcha_iframe2)
    driver.mimic_move_to_random_xy()
    driver.execute_script('''arguments[0].style.pointerEvents = "all";''', recaptcha_iframe2)
    while True:
        driver.wait(1)
        recaptcha_iframe2 = driver.xpath("//iframe[@title]")[1]
        driver.execute_script('''arguments[0].style.pointerEvents = "none";''', recaptcha_iframe2)
        driver.mimic_move_to_xy(click_x, click_y)
        driver.execute_script('''arguments[0].style.pointerEvents = "all";''', recaptcha_iframe2)
        driver.mimic_click()
        driver.wait(1)
        print("solver_btn click loop", driver.xpath("//iframe[@title]/../..")[1].get_attribute("style"))
        driver.wait(1)
        driver.execute_script('''arguments[0].style.pointerEvents = "none";''', recaptcha_iframe2)
        driver.mimic_move_to_random_xy()
        driver.execute_script('''arguments[0].style.pointerEvents = "all";''', recaptcha_iframe2)
        print("solving please wait")
        driver.wait(10)
        if "visible" not in driver.xpath("//iframe[@title]/../..")[1].get_attribute("style"):
            break
        driver.switch_to.frame(driver.xpath("//iframe[@title]")[1])
        try:
            if driver.xpath("//*[contains(text(), 'sending automated queries')]"):
                print("bot detected")
                break
        except:
            print("solver probably failed")
            return
        driver.switch_to.default_content()

    driver.mimic_click("//*[@id='recaptcha-demo-submit']")
    driver.wait(5*6)
    print("done")


def setup_profile(driver: sneaky.Chrome, vpncmd: sneaky.vpncmd):
    driver.get("https://chrome.google.com/webstore/detail/buster-captcha-solver-for/mpbjkejclgfgadiemmefgebjfooflfhl")
    input("setup done? ")
    input("sure? ")


def main():
    print("~ SNEAKY sneaky ~")
    print()
    print("Mode: ")
    print("1. setup default profile")
    print("2. test solving recaptcha")
    print("3. exit")
    print()
    mode = input("Enter mode: ")
    if mode == "1":
        job = setup_profile
    elif mode == "2":
        job = test_recaptcha
    else:
        exit(0)


    capabilities = sneaky.helper.DesiredCapabilities.CHROME
    options = ChromeOptions()
    options.add_argument("--user-data-dir={}".format(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "ChromeProfile")
    ))
    options.add_argument("--profile-directory=Default")
    web = sneaky.SNEAKY(
        executable_path=r"C:\chromedriver.exe",
        options=options,
        # capabilities=capabilities,
        # capabilities=options.to_capabilities(),
        open_developer_tools=True,
        browsermobproxy_server_init={
            "path": r"C:\browsermob-proxy\bin\browsermob-proxy.bat"
        },
        browsermobproxy_create_proxy_kwargs={
            "params": {
                "trustAllServers": "true",
                "port": 8009
            }
        },
        browsermobproxy_new_har_kwargs={
            "options": {
                "captureHeaders": True,
                "captureContent": True
            }
        },
        vpncmd_init={
            "vpncmd_fp": r"C:\Program Files\SoftEther VPN Client\vpncmd_x64.exe",
            "debug": True
        },
        vpncmd_setup_cmd_args=[
            "/client",
            "localhost",
        ],
        vpncmd_connect_known_vpn_kwargs={
            "_NICNAME": "VPN2"
        },
        debug=True
    )
    driver = web.driver
    vpncmd = web.vpncmd

    driver.get("chrome://extensions")
    driver.wait(1)

    try:
        job(driver, vpncmd)
    except:
        traceback.print_exc()

    driver.wait(5*1)
    web.quit()

    print("__main__ is finished.")
    print("Console is safe to close.")


if __name__ == "__main__":
    main()


