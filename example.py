from ContentGenerators.Essay import Document

Essay = Document(pictures=True, topic="World War II")
Essay.Generate()
Essay.Assemble(watermark=True)
