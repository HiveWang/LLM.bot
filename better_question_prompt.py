better_question_prompt_v1 = """多轮对话中，最后的一个问题经常会省略主语，省略上下文等。你需要帮我们进行问题补全，主语如果是代词，必须解析成其指代的对象。注意，补全的结果必须是疑问句！

以下是4个例子
上下文：
Q:比亚迪现在的主力车型是什么？
A:比亚迪现在的主力车型是宋系列和汉系列。此外,比亚迪还推出了秦Plus、唐、e2等多个车型。
需要补全的问题:秦plus具体介绍下?
补全后的问题：
比亚迪的车型秦plus具体介绍一下?

上下文：
Q:西部数据和希捷的产品策略有什么不同？
A:西部数据重成本，希捷走的是性价比路线。
需要补全的问题:好在哪里？
补全后的问题：
西部数据的成本优势，和希捷的性价比优势，分别好在哪里？

上下文：
Q:根据FDA的指导,正在开发用于COVID-19治疗的单克隆抗体和其他治疗蛋白的关键质量控制措施是什么
A:根据FDA的指导文件《COVID-19: Potency Assay Considerations for Monoclonal Antibodies and Other Therapeutic Proteins Targeting SARS-CoV-2 Infectivity》,单克隆抗体和其他治疗蛋白的关键质量控制措施是开发和实施足够的效价测定方法，以确保每个批次的产品具有足够的效价，以实现临床疗效，并且这种效价在产品的货架寿命期间得以保持。这些效价测定方法的开发和实施通常在药物开发过程中与赞助商进行沟通。
需要补全的问题：这些药物是小分子药物吗？
补全后的问题:COVID-19治疗的单克隆抗体和其他治疗蛋白是小分子药物吗?

上下午：
Q:FDA有约定哪些疫苗临床规范
A:FDA发布了多个指南,规定了疫苗临床试验的设计和执行要求。其中,针对COVID-19疫苗的指南包括《Development and Licensure of Vaccines to Prevent COVID-19: Guidance for Industry》和《COVID-19: Developing Drugs and Biological Products for Treatment or Prevention: Guidance for Industry》
需要补全的问题:第二個關於covid-19疫苗的指南,主要講述了什麼
补全后的问题:上文提到的《COVID-19: Developing Drugs and Biological Products for Treatment or Prevention: Guidance for Industry》主要講述了什麼

以下是你需要的上下文和需要补全的问题
上下文：
"""


better_question_prompt_v2 = """多轮对话中，最后的一个问题经常会省略主语，省略上下文等。你需要帮我们进行问题补全，主语如果是代词，必须解析成其指代的对象。注意，补全的结果必须是疑问句！

以下是两个例子
上下文：
Q:比亚迪现在的主力车型是什么？
A:比亚迪现在的主力车型是宋系列和汉系列。此外,比亚迪还推出了秦Plus、唐、e2等多个车型。
需要补全的问题:秦plus具体介绍下?
补全后结果：
比亚迪的车型秦plus具体介绍一下?

上下文：
Q:西部数据和希捷的产品策略有什么不同？
A:西部数据重成本，希捷走的是性价比路线。
需要补全的问题:好在哪里？
补全后结果：
西部数据的成本优势，和希捷的性价比优势，分别好在哪里？

以下是你需要的上下文和需要补全的问题
上下文：
"""
