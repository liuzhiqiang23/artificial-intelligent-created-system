# -*- coding: utf-8 -*-
# 2-zvec-minilm-search：打开 zvec 库 + 交互问答（老师 Mac 代码 Windows 适配版）
# 前置：先运行 2-zvec-minilm-save.py 建库；本脚本必须用与建库相同的嵌入模型！
import os
import warnings

# 1. 准备文档数据（与 save 脚本相同的 9 段，用于按 id 取回原文）
docs = [
    "黑神话悟空的战斗如同武侠小说活过来一般，当金箍棒与妖魔碰撞时，火星四溅，招式行云流水。悟空可随心切换狂猛或灵动的战斗风格，一棒横扫千军，或是腾挪如蝴蝶戏花。",
    "72变神通不只是变化形态，更是开启新世界的钥匙。化身飞鼠可以潜入妖魔巢穴打探军情，变作金鱼能够探索深海遗迹的秘密，每一种变化都是一段独特的冒险。",
    "每场BOSS战都是一场惊心动魄的较量。或是与身躯庞大的九头蟒激战于瀑布之巅，或是在雷电交织的云海中与雷公电母比拼法术，招招险象环生。",
    "驾着筋斗云翱翔在这片神话世界，瑰丽的场景令人屏息。云雾缭绕的仙山若隐若现，古老的妖兽巢穴中藏着千年宝物，月光下的古寺钟声回荡在山谷。",
    "这不是你熟悉的西游记。当悟空踏上寻找身世之谜的旅程，他将遇见各路神仙妖魔。有的是旧识，如同样桀骜不驯的哪吒；有的是劲敌，如手持三尖两刃刀的二郎神。",
    "作为齐天大圣，悟空的神通不止于金箍棒。火眼金睛可洞察妖魔真身，一个筋斗便是十万八千里。而这些能力还可以通过收集天外陨铁、悟道石等材料来强化升级。",
    "世界的每个角落都藏着故事。你可能在山洞中发现上古大能的遗迹，云端天宫里寻得昔日天兵的宝库，或是在凡间集市偶遇卖人参果的狐妖。",
    "故事发生在大唐之前的蛮荒世界，那时天庭还未定鼎三界，各路妖王割据称雄。这是一个神魔混战、群雄逐鹿的动荡年代，也是悟空寻找真相的起点。",
    "游戏的音乐如同一首跨越千年的史诗。古琴与管弦交织出战斗的激昂，笛萧与木鱼谱写禅意空灵。而当悟空踏入重要场景时，古风配乐更是让人仿佛穿越回那个神话的年代。"
    ]

# 2.设置嵌入模型
from sentence_transformers import SentenceTransformer
# 老师 Mac 路径: '/Users/will/.cache/modelscope/hub/models/sentence-transformers/all-MiniLM-L6-v2' → 改本机 HF 缓存快照
script_dir = os.path.dirname(__file__)
model = SentenceTransformer(r"C:\Users\Lenovo\.cache\huggingface\hub\models--sentence-transformers--all-MiniLM-L6-v2\snapshots\1110a243fdf4706b3f48f1d95db1a4f5529b4d41")

import zvec
# 3.打开使用同一嵌入模型存储的向量数据库
coll = zvec.open(path=os.path.join(script_dir, 'zvec', 'coll'))
while True:
    question = input("请输入问题（exit表示退出）：")
    if question == "exit":
        break
    # 4.将问题转换为向量
    # question = "黑神话悟空的战斗系统有什么特点?"
    query_embedding = model.encode([question])[0]

    # 5.然后再在集合中查询结果
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # 屏蔽 VectorQuery 的弃用警告（未来版本将改名 Query）
        result = coll.query(
            zvec.VectorQuery(
                field_name="embedding",
                vector=query_embedding,
            ),
            topk=3,
        )
    # print(result)

    # 6.将查询结果转为对应doc
    context = [docs[idx.fields['id']] for idx in result]
    print("\n检索到的相关文档:")
    for i, doc in enumerate(context, 1):
        print(f"[{i}] {doc}")

    # 7.构建提示词
    prompt = f"""根据以下参考信息回答问题，并给出信息源编号。
    如果无法从参考信息中找到答案，请说明无法回答。
    参考信息:
    {chr(10).join(f"[{i+1}] {doc}" for i, doc in enumerate(context))}
    问题: {question}
    答案:"""

    # 8.使用Ollama生成答案
    # 老师示例模型 openbmb/minicpm5-2b 本机未拉取，按 0910 惯例用 deepseek-r1:latest
    from ollama import chat
    response = chat(
        model="deepseek-r1:latest",
        messages=[{
            "role": "user",
            "content": prompt
        }],
    )
    print(f"\n生成的答案: {response.message.content}")
