# -*- coding: utf-8 -*-
# 2-zvec-minilm-save：MiniLM 嵌入 + zvec 建库存储（老师 Mac 代码 Windows 适配版）
# 注意：必须先跑本脚本建库，再跑 2-zvec-minilm-search.py 查询（两脚本必须用同一个嵌入模型！）
import os
import shutil
import warnings

# 1. 准备文档数据
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
# 3.嵌入文档
doc_embeddings = model.encode(docs)
print(f"文档向量维度: {doc_embeddings.shape}")

# 4.使用zvec：创建Schema
import zvec
from zvec import FieldSchema, VectorSchema, DataType
dimension = doc_embeddings.shape[1]
id_field = FieldSchema("id", DataType.INT64)
# 创建Schema对象，类似于数据库的表
emb_field = VectorSchema("embedding", dimension=dimension, data_type=DataType.VECTOR_FP32)
schema = zvec.CollectionSchema(
     name="Wukong",        # "表名"
     fields=id_field,      # "字段"
     vectors=emb_field     # "数据结构"
)
# 5.使用zvec：根据"表"结构创建数据集合
# Windows 适配：create 要求路径不存在，重跑前先清掉上次残留
coll_path = os.path.join(script_dir, 'zvec', 'coll')
if os.path.exists(coll_path):
    shutil.rmtree(coll_path)
collection = zvec.create_and_open(
    path=coll_path,
    schema=schema,
)
# 6.使用zvec：将文档的向量数据存入集合
with warnings.catch_warnings():
    warnings.simplefilter("ignore")  # 屏蔽 insert 的弃用警告
    for i, emb in enumerate(doc_embeddings):
        collection.insert(
            zvec.Doc(
                id="txt_"+str(i),  # Unique document ID
                vectors={"embedding": emb},
                fields={"id": i},
            )
        )
print(f"已存入 {len(doc_embeddings)} 条向量到 {coll_path}")
