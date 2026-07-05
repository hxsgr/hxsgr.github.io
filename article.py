"""
hxsgr.github.io — 文章编辑脚本

用法:
  python article.py            → 运行预置测试（添加示例内容）
  python article.py --reset    → 清空文章重新开始

也可在其他脚本中引入:
  from article import appendText, appendImage, appendHeading, appendDivider
"""

import json
import os
import re
import sys

# 强制 UTF-8 输出，避免 Windows GBK 终端编码错误
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'article.json')


# ─── 内部工具 ───────────────────────────────────────────

def read_article():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_article(blocks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(blocks, f, ensure_ascii=False, indent=2)


def get_caption(filename):
    """从文件名提取图片说明：null.xxx → None，否则去扩展名"""
    name = os.path.basename(filename)
    # 以 "null." 开头 → 无注释（不区分大小写）
    if re.match(r'^null\.', name, re.IGNORECASE):
        return None
    # 去掉扩展名作为注释
    root, _ = os.path.splitext(name)
    return root if root else None


# ─── 四个公开函数 ───────────────────────────────────────

def append_text(text):
    """追加一段文字"""
    article = read_article()
    article.append({'type': 'paragraph', 'text': text})
    write_article(article)
    preview = text[:40] + ('...' if len(text) > 40 else '')
    print(f'  [+] 已追加段落: {preview}')
    return article


def append_image(filename):
    """追加一张图片。文件名以 null. 开头则无注释，否则用文件名作注释"""
    article = read_article()
    caption = get_caption(filename)
    article.append({
        'type': 'image',
        'src': f'images/{os.path.basename(filename)}',
        'caption': caption
    })
    write_article(article)
    label = f'注释: "{caption}"' if caption else '无注释'
    print(f'  [+] 已追加图片: {filename} ({label})')
    return article


def append_heading(text, level=2):
    """追加标题，默认二级标题"""
    article = read_article()
    article.append({'type': 'heading', 'level': level, 'text': text})
    write_article(article)
    print(f'  [+] 已追加 H{level} 标题: {text}')
    return article


def append_divider():
    """追加分割线"""
    article = read_article()
    article.append({'type': 'divider'})
    write_article(article)
    print('  [+] 已追加分割线')
    return article


# ─── 预置测试 ───────────────────────────────────────────

if __name__ == '__main__':
    args = sys.argv[1:]

    if '--reset' in args:
        write_article([])
        print('[OK] 文章已清空。')
        sys.exit(0)

    print('[TEST] 开始预置测试…\n')

   
    print('append_heading:')
    append_heading('深挖Zihui Song，天才少女还是诬告惯犯？', 1)
    append_heading('第一节', 2)

   
    print('append_text:')
    append_text('以下简称Zs，如果要看重大转折请翻到第二节。')
    append_text('笔者是25年中旬了解到Zs的。那时在“深度学习研讨班2”群聊里有大佬提到过Zs的一些学术探讨，然后讲了一些山东中学生AI研究员之类的故事。笔者在网上随手搜了一下，铺天盖地的新闻。')



    
    print('append_image:')
    append_image('有关山东中学生人工智能天才的新闻.jpg')


    print('append_text:')
    append_text('笔者的技术也是实在有限，没有能力参与大佬们的讨论。后来Zs亲自进了群，笔者随手加了，然后莫名被拉进一个群聊里，名称似乎是“月之森”之类。笔者没看过日漫这类细糠，当初还以为是独创的名称。')


    print('append_image:')
    append_image('群聊概况.jpg')



    print('append_text:')
    append_text('之后群聊似乎总因为各种各样的原因被解散，笔者也误打误撞连续加入后续群聊。尽管笔者没什么实力，但凭借话多还是让部分群友记住，期间也向一些群友讨教过。')
    append_text('过了几个月，群主似乎因为一些劳务原因和情感原因与其他人产生了矛盾，自称“服药自杀”过（暂时没有查证）这段时间的聊天记录恰巧被那时爱护手机的笔者删了，不过在网上搜“AlphaGPT”可以搜到当事人的自述。查证什么的确实比较困难。大体意思是认为一个老板的待遇不公然后冲突。')
    append_text('在这之后Zs在群里发了一个QQ账号，名字是“Cuscuta”，称是前女友，认为她疑似伙同了老板来反对她，还出轨并冷暴力了她一段时间，并欢迎群友去盒人。')


    print('append_image:')
    append_image('挂人示例.jpg')

    print('append_text:')
    append_text('笔者前阵子刚被某不知名税务所泄露过个人信息（私事按下不表），对盒人一事有点本能的反感，但由于Zs的光辉导致不敢产生质疑，自然而然地认为Zs果真受了不小的委屈。笔者自视甚低不敢在群里提问，就加了下这个账号打算听听故事。')

    print('append_image:')
    append_image('初见cu.jpg')

    print('append_text:')
    append_text('笔者确实短暂地产生了”中二”之类的印象，不过这种误会也在所难免。总之笔者试着聊了几句，或许是因为一直没有表现什么立场，Cuscuta也同意给我讲故事了.')

    print('append_image:')
    append_image('cu的故事.jpg')

    print('append_text')
    append_text('聊天记录太长笔者暂时不放全了，后续可能会开个百度网盘存一下。大致意思是说有个老板雇佣了Zs并过度压榨，Cuscuta劝Zs为了身体离开，而自己因为精神原因休息了一段时间，并在此期间和精神上虚构的女友聊天。后续Zs和老板发生冲突后顺手把Cuscuta也盒了，查到了其和tulpa的聊天，并发了点威胁。')

    print('append_image:')
    append_image('Zs威胁示例.jpg')

    print('append_text:')
    append_text('这些当然都是一面之词，笔者也确实没什么能力查证，不过”让Zs离开老板”这一点Zs以前也提及过，而且在别的事情上看好像没什么利益纠纷，也不至于达到盒的程度。')

    append_image('双方验证.jpg')


    append_text('笔者后来转述了一下双方意见，然后Zs说“对不起，不要再加Cuscuta了”，Cuscuta则说“她又被我拉回来了”，笔者误以为两人消除误会达成了和解，也就离开了这段故事。')
    append_text('大概一个月后，Zs对Cuscuta的叙事似乎仍然是负面且怀疑的，并提出了一些看起来不切实际的指控。鉴于笔者之前与Cuscuta有过联系，好奇是否是有了新证据之类（但这似乎一直没出现过），而且盒人确实也不好。')



    append_image('在前文已提到Cuscuta让Zs离开shao的情况，因此笔者认为Zs因仇恨产生了无端的指控）.jpg')

    append_text('劝阻无效后，笔者被认为过度偏袒Cuscuta而遭到了严厉打击。')

    append_image('初次严厉打击.jpg')


    append_text('从这以后笔者也确实产生了点情绪（毕竟深度学习研讨班2跟Zs没有强利益关联，笔者还想在里面接受点熏陶），不过也确实没有太多能发泄的地方。过段时间开了个小号进群，发现自己也享受了同等待遇')


    append_image('公平起见还是说明一下，所谓出户口似乎尚未实现，因为Zs展示的盒能力似乎仍局限在社工库级别，笔者本人也暂未受到法律意义上的影响.jpg')


    append_text('笔者把群聊号放在了空间里，也确实有人进去捣乱了。不出意外被归因于笔者。')

    append_image('意味深的言语.jpg')

    append_text('然后Zs开启了诉打击，不过其法律意识让该诉打击的威慑力度降到了0。')


    append_image('注：Zs已经年满十四不属于幼女，Cuscuta并不在规定内的特殊职业人群中，控诉的结果为图屏幕前的各位一笑.jpg')

    append_image('即便是诬大生也不会这么早就给对面留下不利证据，并且在我与不知名税务所的缠斗中对非法拉屎有了初步了解，对线只靠转屎而非拉屎.jpg')


    append_image('注：Zs在心理学上并无真正成果，此指控源于其自学的&quot;Quantitative Psychology&quot;，群聊中一位心理学本科同志明确表示“考虑过少”.jpg')



    append_text('不过好在哪怕是Zs阵营也有懂法律的人在，及时挽救了Zs的50元诉讼费和几千块钱的取证费')


    append_image('大律师.jpg')


    append_text('自此之后笔者保留了这个群聊，想搜集更多有趣的内容。然后一件趣事发生了：Zs全体先遭到了某成员家长的严厉打击，事后谈论走私相关内容又被状告公安')



    append_image('为保护涉事的其他人，不单独展示清晰的家长方聊天记录.jpg')



    append_image('不明意义的价格展示.jpg')


    append_image('注：这里仅为自爆，至于是否有真实行动，是否有行动的能力未经证实.jpg')


    append_image('不明意义的指控.jpg')


    append_text('更有意思的来了，Zs认为是我把东西交给了上海公安，上海公安转交给了山东公安，山东公安派发给下属派出所并找到了其团队成员进行约谈')


    append_image('注：笔者不同意此文的任何指控，包括对笔者以外个人或组织的指控.jpg')


    append_text('原因是我在此前的聊天记录')


    append_image('注：当时为周日晚，笔者作为一名在读高中生有整整五天的冷却时间。笔者的确想在五天后去邮局寄信，但不至于为与我个人利益无关的事情牺牲正常课时.jpg')



    append_text('于是笔者别无他路，为了给Zs一个台阶只好真的在周末找了网警。不过网警的办理比接受要晚不少，毕竟互联网傻福实在太多了，可以体谅。')

    append_text('鉴于好奇，笔者在课时基本结束以后读了读Zs的有关信息。')

    append_heading('第二节')



    append_text('这是转折的开始。')

    append_text('最初，一个群友为我发了gemini所找到的部分信息。由于笔者遭遇过gemini的谄媚残害，并没有重视。')


    append_image('注：此处的手机号为上文提到的”家长”所有.jpg')


    append_text('这位网友明智地退出了纷争（尽管对他的严厉打击也快要开始），因此也没跟笔者解释信息内容。笔者事后补全了一些链条。')

    append_image('注：此处的多玩并非官方多玩，是多玩暴毙后自封的“多玩2nd”。曾有人怀疑为蹭热度而故意进行混淆，详见hack.chat非官方史料.jpg')

    append_image('同上注释.jpg')


    append_text('不难注意到此jankie与上文群友搜集的信息相似。')
    append_text('同时，笔者注意到Zs在被删的知乎文章里发表过一系列指控，首当其冲的是有关IKCEST主办方的，认为自己没上新闻不公平')

    append_image('Zs原文.jpg')

    append_text('而我们可以打开Zs所说的这篇新闻')


    append_image('小声BB：他们排名似乎比一些大专还低一点，里面说的“打破纪录”好像也是指年龄记录.jpg')


    append_text('可以看到获奖者里与“香港中学生”合作的是Shihao Ji(以下简称Sj)')

    append_text('这引出第一个疑点：Sj与Zs是否为同一人？')

    append_text('（Sj上过不少新闻，而Zs则处处与Sj绑定且无露脸等强证据，公开展示的个人经历几乎与Sj一模一样。倘若真如知乎文章里那样注重名誉，这谦虚的不真实了。）假设Zihui Song一名造假，或许其学术道德问题比Zs所指控的任何一项都大不少')


    append_text('与此类似的还有一件')
    append_image('收款手机号.jpg')

    append_text('这是Zs发布的收款用手机号。值得注意的是，根据企查查等信息，会发现这是一位注册了一些超市和批发用品商店的某兰。而某兰的另一些企业里受益人为某侠，某侠与Sj合资开过一所企业')

    append_text('（上述调查过程完全不涉及非法行为，笔者声明绝非开盒）')
    append_text('以及某些不知名网站上有aloongqwq(某家长的手机号对应Q号）为Jankie别称的说法。')


    append_text('按下不表')

    append_text('https://gist.github.com/xjzh123 这个网页更让我大为震撼')

    append_image('诬毒事件1.jpg')
    append_image('诬毒事件2.jpg')
    append_image('诬毒事件3.jpg')

    append_text('无论怎么看，这都像一起精心策划的诬告。当然，代码仓库被jankie删了，但这似乎让其可能性高了不少')

    append_text('以及，搜香港同学与Zs时，浏览器为我弹出了狗维')
    append_text('香港同学被设为25年年度人物')

    append_image('注：笔者反对狗维，不提倡读者访问，且不支持其中所有观点.jpg')

    append_text('当然，狗维不是什么好东西真实性也确实存疑，但结合此前对Jankie的多方指控，以及Zs在此后的几次冲突里熟练地靠情绪输出与几乎零证据掌控舆论一事来看…')
    append_text('细思极恐')

    append_image('自爆2.jpg')


    append_text('再想想HK中学生被挂成年度人物的事…')

    append_text('笔者不愿展开描述，是否存在嫌疑各位自行推断')

    append_text('此前alphagpt,credal transformer都引起过一段舆论，而某些人在控制舆论上又似乎的确有经验')


    append_image('自爆3.jpg')
    append_text('这似乎解释了为什么在各大顶会正会都常有中学生出现的情况下，一篇workshop成为了大新闻。而对Zs相关项目大加称赞的有不少AI稿件')

    append_image('图文无关.jpg')
    append_text('笔者没有权力把自己的猜想写在文中')
    append_text('就此搁笔吧')


    append_text('https://pan.baidu.com/s/1gKedy_RunAOJyiXDayqOmA?pwd=jn8e ')

    append_image('难蚌记录.png')
