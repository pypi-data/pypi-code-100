# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2021-07-15
#


from pyzentao import Zentao


if "__main__" == __name__:
    zentao = Zentao({
        # zentao root url
        "url": "http://0.0.0.0:30080/zentao",
        "version": "15",

        # authentication
        "username": "admin",
        "password": "Lton2008@",
    })

    response = zentao.user_task(
        userID=1,
        type="assignedTo",
        # raw=True
    )

    if response.status == "success":
        tasks = sorted(response.data["tasks"].values(),
                       key=lambda x: int(x.get("id")))

        print(">" * 30)
        print(tasks)
        print("<" * 30)

# end
