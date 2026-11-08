import sex

def exchange_timer():
    from apscheduler.schedulers.blocking import BlockingScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(sex.exchange_fish_300star, 'cron', hour=14, minute=0, second=5)
    scheduler.start()  # 启动调度器，它将阻塞当前线程，直到调度器被关闭或程序结束。

if __name__ == "__main__":
    # sex.main("qiqiwo321", 3)
    # sex.process_food()  # 加工
    # sex.harvest_and_sell_new_account_item()
    # sex.shouhuo(1)
    # sex.exec_task()

    exchange_timer() # 交换物品

    # sex.main("qiqiwo321", 10)

    # sex.daily_event(2, 137)  # 商会存储物品
    # from_accounts = ["shifangfozu55"]
    # sex.tansform_item(from_accounts, "qiqiwo321")

    # sex.daily_event(8, 50)  # 查询二星鱼超过300的账号
    # sex.daily_event(9, 138)  # 查看是否完成升级爵位任务
    # print("====================================================")
    # for i in sex.account_list:
    #     print(i)
    # sex.open_box()
    # sex.assign_money()  # 分配金币
    # sex.tansform_nobility_item()
    # sex.to_store_nobility_item()  # 主账号存储加工材料
    # sex.main("shifangfozu227", 11)
    # sex.reg_new_account()
    # sex.main("qiqiwo321", 10) # 获取所有商会物品

    # sex.add_earth_and_cage()

    # sex.tansform_money_item()

    # sex.tansform_seed()  # 转移种子



