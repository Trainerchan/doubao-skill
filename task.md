我现在要做一个skill，叫doubao-skill。
这个skill的目录处于E:\doubao-skill\目录下面。
这个skill的目标是帮助agent，提供调用豆包接口的能力。
这个skill包含三个子skill
1. 通用skill
配置通用类型的模型id，配置好apikey，模型id类似 doubao-seed之类的，这类通用模型，使用场景，比如分析图片，识别图片，识别文档，提取文档，识别pdf，xlsx，pptx之类的通用使用场景，正常的对话，多模态使用场景。

2. 生成图片skill - generate-image
配置图片的模型id，豆包的有doubao-seedream,这类模型是豆包专门用于创作图像的模型，这个skill就是调用这个模型，配合apikey

3. 生成视频skill - generate-video
配置视频的模型id，豆包有doubao-seedance,这个skill专门用于创作视频，调用对应的接口。


使用这个skill需要配置对应的apikey，以及对应的每个skill需要的模型。

这个skill，需要去查询文档，豆包的接口文档，也就是火山引擎的接口文档，https://www.volcengine.com/docs/82379/1541594?lang=zh。可以使用context7的mcp工具，查找最新的文档，获取文档内容，然后完善三个skill。
每个skill都要根据文档，目的是告诉调用skill的agent，如何进行调用豆包对应的接口，达成对应的目的。

这个整个skill，agent调用的时候，需要进行配置或者环境变量，每次调用获取对应的配置或者环境变量，然后进行调用接口。
