red_ball = []
bule_ball = []
r_index =1
b_index =1
print('\033[0;31;40mWelcome double ball\033[0m')
while True:
    if len(red_ball) == 6 and len(bule_ball) == 2:
        print("Red Ball:", red_ball)
        print("Blue Ball:", bule_ball)
        print("Good luck")
        break
    if len(red_ball) == 6:

        try:
            num = int(input('\033[34m[{}]Please input blue ball\033[0m'.format(b_index)))
        except Exception as e:
            print('\033[34myour input num error\033[0m')
        if num <= 16 and num >= 1:
            if num in bule_ball:
                print('\033[34mnum is exit\033[0m')
                continue
            bule_ball.append(num)
            b_index += 1

        else:
            print("\033[34mnum must bo in 1-16\033[0m")

    else:

        try:
            num = int(input('\033[31m[{}]please input red ball\033[0m'.format(r_index)))
        except Exception as e:
            print('\033[31m对不起！您输入的内容有误～\033[0m')
        if num<=32 and num >=1:
            if num in red_ball:
                print('\033[31mnum is exit\033[0m')
                continue
            red_ball.append(num)
            r_index += 1

        else:
            print("\033[31mnum must be in 1-32\033[0m")
